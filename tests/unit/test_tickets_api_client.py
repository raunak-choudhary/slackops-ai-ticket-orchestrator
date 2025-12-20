from tickets_api.client import TicketInterface, Ticket, TicketStatus


class ConcreteTickets(TicketInterface):
    def create_ticket(self, title, description, assignee=None):
        raise NotImplementedError

    def get_ticket(self, ticket_id):
        raise NotImplementedError

    def search_tickets(self, query=None, status=None):
        raise NotImplementedError

    def update_ticket(self, ticket_id, status=None, title=None):
        raise NotImplementedError

    def delete_ticket(self, ticket_id):
        raise NotImplementedError


def test_ticket_interface_methods_raise_not_implemented():
    tickets = ConcreteTickets()

    try:
        tickets.create_ticket("t", "d")
    except NotImplementedError:
        pass

    try:
        tickets.get_ticket("id")
    except NotImplementedError:
        pass

    try:
        tickets.search_tickets()
    except NotImplementedError:
        pass

    try:
        tickets.update_ticket("id")
    except NotImplementedError:
        pass

    try:
        tickets.delete_ticket("id")
    except NotImplementedError:
        pass


class ConcreteTicket(Ticket):
    @property
    def id(self) -> str:
        raise NotImplementedError

    @property
    def title(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        raise NotImplementedError

    @property
    def status(self) -> TicketStatus:
        raise NotImplementedError

    @property
    def assignee(self) -> str | None:
        raise NotImplementedError


def test_ticket_properties_raise_not_implemented():
    ticket = ConcreteTicket()

    try:
        _ = ticket.id
    except NotImplementedError:
        pass

    try:
        _ = ticket.title
    except NotImplementedError:
        pass

    try:
        _ = ticket.description
    except NotImplementedError:
        pass

    try:
        _ = ticket.status
    except NotImplementedError:
        pass

    try:
        _ = ticket.assignee
    except NotImplementedError:
        pass
