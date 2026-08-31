import re

from streamsentry.domain.errors import ValidationError
from streamsentry.domain.workspace import Owner, Workspace

from .context import ServiceContext

SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9-]{1,62}$")


class WorkspaceService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def create_workspace(self, slug: str, name: str) -> Workspace:
        if not SLUG_PATTERN.fullmatch(slug) or not name.strip():
            raise ValidationError("workspace slug or name is invalid")
        item = Workspace(
            id=self.context.ids.new("workspace"),
            slug=slug,
            name=name.strip(),
            created_at=self.context.clock.now(),
        )
        self.context.store.create_workspace(item)
        return item

    def create_owner(self, workspace_id: str, name: str, email: str, team: str) -> Owner:
        if not name.strip() or "@" not in email or not team.strip():
            raise ValidationError("owner name, email, and team are required")
        item = Owner(
            id=self.context.ids.new("owner"),
            workspace_id=workspace_id,
            name=name.strip(),
            email=email.strip().lower(),
            team=team.strip(),
            created_at=self.context.clock.now(),
        )
        self.context.store.put_owner(item)
        return item
