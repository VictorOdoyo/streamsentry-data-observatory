from streamsentry.domain.errors import ConflictError
from streamsentry.domain.lineage import LineageEdge

from .context import ServiceContext


class LineageService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def connect(
        self,
        workspace_id: str,
        upstream_dataset_id: str,
        downstream_dataset_id: str,
        transformation: str,
    ) -> LineageEdge:
        self.context.store.get_dataset(workspace_id, upstream_dataset_id)
        self.context.store.get_dataset(workspace_id, downstream_dataset_id)
        existing = self.context.store.list_lineage(workspace_id)
        if any(
            edge.upstream_dataset_id == upstream_dataset_id
            and edge.downstream_dataset_id == downstream_dataset_id
            for edge in existing
        ):
            raise ConflictError("lineage edge already exists")
        edge = LineageEdge(
            id=self.context.ids.new("lineage"),
            workspace_id=workspace_id,
            upstream_dataset_id=upstream_dataset_id,
            downstream_dataset_id=downstream_dataset_id,
            transformation=transformation.strip(),
            observed_at=self.context.clock.now(),
        )
        self.context.store.put_lineage(edge)
        return edge

    def downstream_impact(self, workspace_id: str, dataset_id: str) -> list[str]:
        edges = self.context.store.list_lineage(workspace_id)
        visited: set[str] = set()
        queue = [dataset_id]
        while queue:
            current = queue.pop(0)
            for edge in edges:
                is_upstream = edge.upstream_dataset_id == current
                is_unvisited = edge.downstream_dataset_id not in visited
                if is_upstream and is_unvisited:
                    visited.add(edge.downstream_dataset_id)
                    queue.append(edge.downstream_dataset_id)
        visited.discard(dataset_id)
        return sorted(visited)
