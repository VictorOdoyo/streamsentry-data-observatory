from streamsentry.domain.enums import SLOStatus
from streamsentry.domain.slo import ServiceLevelObjective

from .context import ServiceContext


class SLOService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def create(
        self,
        workspace_id: str,
        dataset_id: str,
        name: str,
        freshness_minutes: int,
        success_rate_target: float,
        window_days: int = 30,
    ) -> ServiceLevelObjective:
        self.context.store.get_dataset(workspace_id, dataset_id)
        item = ServiceLevelObjective(
            id=self.context.ids.new("slo"),
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            name=name.strip(),
            freshness_minutes=freshness_minutes,
            success_rate_target=success_rate_target,
            current_success_rate=1,
            status=SLOStatus.MEETING,
            window_days=window_days,
            evaluated_at=self.context.clock.now(),
        )
        self.context.store.put_slo(item)
        return item

    def evaluate(
        self, workspace_id: str, slo_id: str, current_success_rate: float
    ) -> ServiceLevelObjective:
        current = self.context.store.get_slo(workspace_id, slo_id)
        ratio = current_success_rate / current.success_rate_target
        status = (
            SLOStatus.MEETING
            if ratio >= 1
            else SLOStatus.AT_RISK
            if ratio >= 0.95
            else SLOStatus.BREACHED
        )
        updated = current.model_copy(
            update={
                "current_success_rate": current_success_rate,
                "status": status,
                "evaluated_at": self.context.clock.now(),
            }
        )
        self.context.store.put_slo(updated)
        return updated
