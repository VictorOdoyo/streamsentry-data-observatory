from streamsentry.domain.dataset import Dataset
from streamsentry.domain.enums import DatasetStatus, DatasetTier
from streamsentry.domain.errors import ValidationError

from .context import ServiceContext


class DatasetService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def create(
        self,
        workspace_id: str,
        name: str,
        fully_qualified_name: str,
        platform: str,
        tier: DatasetTier,
        owner_id: str,
        description: str = "",
        tags: tuple[str, ...] = (),
    ) -> Dataset:
        self.context.store.get_owner(workspace_id, owner_id)
        if not name.strip() or "." not in fully_qualified_name or not platform.strip():
            raise ValidationError("dataset name, qualified name, and platform are required")
        item = Dataset(
            id=self.context.ids.new("dataset"),
            workspace_id=workspace_id,
            name=name.strip(),
            fully_qualified_name=fully_qualified_name.strip(),
            platform=platform.strip(),
            tier=tier,
            status=DatasetStatus.HEALTHY,
            owner_id=owner_id,
            description=description.strip(),
            tags=tuple(sorted(set(tags))),
            last_observed_at=self.context.clock.now(),
            created_at=self.context.clock.now(),
        )
        self.context.store.put_dataset(item)
        return item

    def set_status(self, workspace_id: str, dataset_id: str, status: DatasetStatus) -> Dataset:
        current = self.context.store.get_dataset(workspace_id, dataset_id)
        updated = current.model_copy(update={"status": status})
        self.context.store.put_dataset(updated)
        return updated
