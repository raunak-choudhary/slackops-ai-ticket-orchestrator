import tickets_api.client as tickets_client
import tickets_adapter  # noqa: F401


def test_adapter_injects_client() -> None:
    client = tickets_client.get_client()
    assert client is not None
