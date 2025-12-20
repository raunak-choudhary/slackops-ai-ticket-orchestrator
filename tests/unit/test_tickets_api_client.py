from tickets_api.client import TicketInterface, Ticket, TicketStatus


class ConcreteTickets(TicketInterface):
    def create_ticket(self, title, description, assignee=None):
        return super().create_ticket(title, description, assignee)

    def get_ticket(self, ticket_id):
        return super().get_ticket(ticket_id)

    def search_tickets(self, query=None, status=None):
        return super().search_tickets(query, status)

    def update_ticket(self, ticket_id, status=None, title=None):
        return super().update_ticket(ticket_id, status, title)

    def delete_ticket(self, ticket_id):
        return super().delete_ticket(ticket_id)


def test_ticket_interface_methods_return_none():
    """
    Abstract method bodies using `...` return None at runtime.
    This test validates actual Python behavior.
    """
    tickets = ConcreteTickets()

    assert tickets.create_ticket("t", "d") is None
    assert tickets.get_ticket("id") is None
    assert tickets.search_tickets() is None
    assert tickets.update_ticket("id") is None
    assert tickets.delete_ticket("id") is None


class ConcreteTicket(Ticket):
    @property
    def id(self) -> str:
        return super().id

    @property
    def title(self) -> str:
        return super().title

    @property
    def description(self) -> str:
        return super().description

    @property
    def status(self) -> TicketStatus:
        return super().status

    @property
    def assignee(self) -> str | None:
        return super().assignee


def test_ticket_properties_return_none():
    """
    Abstract property bodies using `...` return None, not exceptions.
    """
    ticket = ConcreteTicket()

    assert ticket.id is None
    assert ticket.title is None
    assert ticket.description is None
    assert ticket.status is None
    assert ticket.assignee is None
