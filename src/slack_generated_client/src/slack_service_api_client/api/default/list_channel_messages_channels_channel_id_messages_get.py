from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.messages_response import MessagesResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    channel_id: str,
    *,
    limit: int | Unset = 10,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/channels/{channel_id}/messages".format(channel_id=quote(str(channel_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> HTTPValidationError | MessagesResponse | None:
    if response.status_code == 200:
        response_200 = MessagesResponse.from_dict(response.json())



        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[HTTPValidationError | MessagesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,

) -> Response[HTTPValidationError | MessagesResponse]:
    """ List Channel Messages

     Retrieve messages from a channel.

    This endpoint fetches messages using the abstract chat interface.
    The underlying provider implementation is injected via
    `slack_impl` at import time.

    Args:
        channel_id: Identifier of the channel to read messages from.
        limit: Maximum number of messages to return (1–100).

    Returns:
        MessagesResponse containing the list of messages.

    Raises:
        HTTPException: If message retrieval fails.

    Args:
        channel_id (str):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MessagesResponse]
     """


    kwargs = _get_kwargs(
        channel_id=channel_id,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,

) -> HTTPValidationError | MessagesResponse | None:
    """ List Channel Messages

     Retrieve messages from a channel.

    This endpoint fetches messages using the abstract chat interface.
    The underlying provider implementation is injected via
    `slack_impl` at import time.

    Args:
        channel_id: Identifier of the channel to read messages from.
        limit: Maximum number of messages to return (1–100).

    Returns:
        MessagesResponse containing the list of messages.

    Raises:
        HTTPException: If message retrieval fails.

    Args:
        channel_id (str):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MessagesResponse
     """


    return sync_detailed(
        channel_id=channel_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,

) -> Response[HTTPValidationError | MessagesResponse]:
    """ List Channel Messages

     Retrieve messages from a channel.

    This endpoint fetches messages using the abstract chat interface.
    The underlying provider implementation is injected via
    `slack_impl` at import time.

    Args:
        channel_id: Identifier of the channel to read messages from.
        limit: Maximum number of messages to return (1–100).

    Returns:
        MessagesResponse containing the list of messages.

    Raises:
        HTTPException: If message retrieval fails.

    Args:
        channel_id (str):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MessagesResponse]
     """


    kwargs = _get_kwargs(
        channel_id=channel_id,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,

) -> HTTPValidationError | MessagesResponse | None:
    """ List Channel Messages

     Retrieve messages from a channel.

    This endpoint fetches messages using the abstract chat interface.
    The underlying provider implementation is injected via
    `slack_impl` at import time.

    Args:
        channel_id: Identifier of the channel to read messages from.
        limit: Maximum number of messages to return (1–100).

    Returns:
        MessagesResponse containing the list of messages.

    Raises:
        HTTPException: If message retrieval fails.

    Args:
        channel_id (str):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MessagesResponse
     """


    return (await asyncio_detailed(
        channel_id=channel_id,
client=client,
limit=limit,

    )).parsed
