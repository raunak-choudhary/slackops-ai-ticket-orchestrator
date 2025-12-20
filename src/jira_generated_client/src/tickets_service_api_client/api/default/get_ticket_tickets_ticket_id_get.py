from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.ticket_out import TicketOut
from ...types import Response


def _get_kwargs(
    ticket_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/tickets/{ticket_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TicketOut | None:
    if response.status_code == 200:
        response_200 = TicketOut.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | TicketOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticket_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | TicketOut]:
    """Get Ticket

    Args:
        ticket_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TicketOut]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ticket_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | TicketOut | None:
    """Get Ticket

    Args:
        ticket_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TicketOut
    """

    return sync_detailed(
        ticket_id=ticket_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    ticket_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | TicketOut]:
    """Get Ticket

    Args:
        ticket_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TicketOut]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticket_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | TicketOut | None:
    """Get Ticket

    Args:
        ticket_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TicketOut
    """

    return (
        await asyncio_detailed(
            ticket_id=ticket_id,
            client=client,
        )
    ).parsed
