# src/jira_impl/src/jira_impl/impl.py
"""Jira-backed implementation of tickets_api.client.TicketInterface.

This module is responsible for:
- Implementing the OSS TicketInterface contract (sync).
- Mapping JiraIssue -> tickets_api Ticket shape.
- Keeping Jira workflow-specific operations out of the OSS interface.
"""

from __future__ import annotations

from dataclasses import dataclass

from tickets_api.client import Ticket, TicketInterface, TicketStatus

from jira_impl.config import JiraConfig
from jira_impl.jira_client import JiraClient, JiraIssue


def _map_status(jira_status_name: str) -> TicketStatus:
    """Map Jira workflow status name to OSS TicketStatus."""
    name = (jira_status_name or "").strip().lower()
    if name in {"to do", "todo", "open", "backlog"}:
        return TicketStatus.OPEN
    if name in {"in progress", "in_progress", "doing"}:
        return TicketStatus.IN_PROGRESS
    if name in {"done", "closed", "resolved"}:
        return TicketStatus.CLOSED
    return TicketStatus.OPEN


@dataclass(frozen=True, slots=True)
class JiraTicket(Ticket):
    """Concrete Ticket implementation backed by Jira issue data."""

    _id: str
    _title: str
    _description: str
    _status: TicketStatus
    _assignee: str | None

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> TicketStatus:
        return self._status

    @property
    def assignee(self) -> str | None:
        return self._assignee


class JiraTicketClient(TicketInterface):
    """TicketInterface implementation that delegates to JiraClient."""

    def __init__(self) -> None:
        cfg = JiraConfig.from_env()
        self._project_key = cfg.project_key
        self._jira = JiraClient(base_url=cfg.base_url, email=cfg.email, api_token=cfg.api_token)

    def _to_ticket(self, issue: JiraIssue) -> JiraTicket:
        """Convert JiraIssue to JiraTicket."""
        return JiraTicket(
            _id=issue.key,
            _title=issue.summary,
            _description=issue.description,
            _status=_map_status(issue.status_name),
            _assignee=issue.assignee_account_id,
        )

    # -------------------------
    # Required OSS API methods
    # -------------------------

    def create_ticket(self, title: str, description: str, assignee: str | None = None) -> Ticket:
        if not title.strip():
            raise ValueError("title must be non-empty")
        if not description.strip():
            raise ValueError("description must be non-empty")

        issue = self._jira.create_issue(
            project_key=self._project_key,
            summary=title.strip(),
            description=description,
            assignee_account_id=assignee,
        )
        return self._to_ticket(issue)

    def get_ticket(self, ticket_id: str) -> Ticket | None:
        try:
            issue = self._jira.get_issue(ticket_id)
        except KeyError:
            return None
        return self._to_ticket(issue)

    def search_tickets(self, query: str | None = None, status: TicketStatus | None = None) -> list[Ticket]:
        clauses: list[str] = [f'project = "{self._project_key}"']

        if query and query.strip():
            q = query.strip().replace('"', '\\"')
            clauses.append(f'(summary ~ "{q}" OR description ~ "{q}")')

        if status is not None:
            if status == TicketStatus.OPEN:
                clauses.append('statusCategory = "To Do"')
            elif status == TicketStatus.IN_PROGRESS:
                clauses.append('statusCategory = "In Progress"')
            elif status == TicketStatus.CLOSED:
                clauses.append("statusCategory = Done")

        jql = " AND ".join(clauses)
        issues = self._jira.search_issues(jql=jql, max_results=25)
        return [self._to_ticket(i) for i in issues]

    def update_ticket(self, ticket_id: str, status: TicketStatus | None = None, title: str | None = None) -> Ticket:
        # OSS contract allows status/title updates, but Jira status transitions are workflow-specific.
        _ = status  # intentionally accepted but not forced here

        if title is None:
            existing = self._jira.get_issue(ticket_id)
            return self._to_ticket(existing)

        if not title.strip():
            raise ValueError("title must be non-empty when provided")

        issue = self._jira.update_issue_summary(issue_key=ticket_id, summary=title.strip())
        return self._to_ticket(issue)

    def delete_ticket(self, ticket_id: str) -> bool:
        return self._jira.delete_issue(ticket_id)

    # -----------------------------------------
    # Extra helper methods (NOT in tickets_api)
    # -----------------------------------------

    def jira_project_key(self) -> str:
        """Return the configured Jira project key (useful for diagnostics)."""
        return self._project_key
