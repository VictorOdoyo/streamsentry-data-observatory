from datetime import date

from streamsentry.domain.cost import CostSignal
from streamsentry.domain.enums import CostTrend

from .context import ServiceContext


class CostService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def record(
        self,
        workspace_id: str,
        dataset_id: str,
        period_start: date,
        period_end: date,
        amount_usd: float,
        query_count: int,
        scanned_bytes: int,
        trend: CostTrend,
    ) -> CostSignal:
        self.context.store.get_dataset(workspace_id, dataset_id)
        item = CostSignal(
            id=self.context.ids.new("cost"),
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            period_start=period_start,
            period_end=period_end,
            amount_usd=amount_usd,
            query_count=query_count,
            scanned_bytes=scanned_bytes,
            trend=trend,
            observed_at=self.context.clock.now(),
        )
        self.context.store.put_cost(item)
        return item

    def total(self, workspace_id: str) -> float:
        return round(sum(item.amount_usd for item in self.context.store.list_costs(workspace_id)), 2)
