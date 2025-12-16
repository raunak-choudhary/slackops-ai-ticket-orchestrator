from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.members_response import MembersResponse
from typing import cast



def _get_kwargs(
    channel_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/channels/{channel_id}/members".format(channel_id=quote(str(channel_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> HTTPValidationError | MembersResponse | None:
    if response.status_code == 200:
        response_200 = MembersResponse.from_dict(response.json())



        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[HTTPValidationError | MembersResponse]:
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

) -> Response[HTTPValidationError | MembersResponse]:
    """ List Channel Members

     List members of a channel.

    NOTE:
    This endpoint assumes that the injected chat client provides
    a provider-specific extension for retrieving channel members.
    If unavailable, this method should be implemented in `slack_impl`
    and exposed via the injected client.

    Args:
        channel_id: Identifier of the channel.

    Returns:
        MembersResponse containing member identifiers.

    Raises:
        HTTPException: If member listing fails.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MembersResponse]
     """


    kwargs = _get_kwargs(
        channel_id=channel_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> HTTPValidationError | MembersResponse | None:
    """ List Channel Members

     List members of a channel.

    NOTE:
    This endpoint assumes that the injected chat client provides
    a provider-specific extension for retrieving channel members.
    If unavailable, this method should be implemented in `slack_impl`
    and exposed via the injected client.

    Args:
        channel_id: Identifier of the channel.

    Returns:
        MembersResponse containing member identifiers.

    Raises:
        HTTPException: If member listing fails.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MembersResponse
     """


    return sync_detailed(
        channel_id=channel_id,
client=client,

    ).parsed

async def asyncio_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[HTTPValidationError | MembersResponse]:
    """ List Channel Members

     List members of a channel.

    NOTE:
    This endpoint assumes that the injected chat client provides
    a provider-specific extension for retrieving channel members.
    If unavailable, this method should be implemented in `slack_impl`
    and exposed via the injected client.

    Args:
        channel_id: Identifier of the channel.

    Returns:
        MembersResponse containing member identifiers.

    Raises:
        HTTPException: If member listing fails.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MembersResponse]
     """


    kwargs = _get_kwargs(
        channel_id=channel_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    channel_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> HTTPValidationError | MembersResponse | None:
    """ List Channel Members

     List members of a channel.

    NOTE:
    This endpoint assumes that the injected chat client provides
    a provider-specific extension for retrieving channel members.
    If unavailable, this method should be implemented in `slack_impl`
    and exposed via the injected client.

    Args:
        channel_id: Identifier of the channel.

    Returns:
        MembersResponse containing member identifiers.

    Raises:
        HTTPException: If member listing fails.

    Args:
        channel_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MembersResponse
     """


    return (await asyncio_detailed(
        channel_id=channel_id,
client=client,

    )).parsed
