import tickets_api.client as tickets_client

from tickets_adapter.adapter import TicketsServiceAdapter

tickets_client.get_client = lambda: TicketsServiceAdapter()
