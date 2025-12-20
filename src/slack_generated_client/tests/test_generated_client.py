def test_can_import_generated_client() -> None:
    import slack_service_api_client  # noqa: F401


def test_can_create_client() -> None:
    from slack_service_api_client.client import Client

    client = Client(base_url="http://localhost")
    assert client._base_url == "http://localhost"
