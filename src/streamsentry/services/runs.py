from streamsentry.domain.enums import DatasetStatus, RunStatus
from streamsentry.domain.run import QualityRun
from streamsentry.evaluation.models import Observation
from streamsentry.evaluation.registry import evaluate_check

from .context import ServiceContext


class RunService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def execute(self, workspace_id: str, check_id: str, observation: Observation) -> QualityRun:
        check = self.context.store.get_check(workspace_id, check_id)
        dataset = self.context.store.get_dataset(workspace_id, check.dataset_id)
        started_at = self.context.clock.now()
        result = evaluate_check(check, observation, started_at)
        finished_at = self.context.clock.now()
        run = QualityRun(
            id=self.context.ids.new("run"),
            workspace_id=workspace_id,
            dataset_id=dataset.id,
            check_id=check.id,
            status=result.status,
            observed_value=result.observed_value,
            expected_value=result.expected_value,
            message=result.message,
            metrics=result.metrics,
            started_at=started_at,
            finished_at=finished_at,
        )
        self.context.store.put_run(run)
        if result.status != RunStatus.SKIPPED:
            status = (
                DatasetStatus.HEALTHY
                if result.status == RunStatus.PASSED
                else DatasetStatus.FAILING
            )
            self.context.store.put_dataset(
                dataset.model_copy(
                    update={
                        "status": status,
                        "last_observed_at": observation.observed_at,
                        "row_count": observation.row_count,
                    }
                )
            )
        return run
