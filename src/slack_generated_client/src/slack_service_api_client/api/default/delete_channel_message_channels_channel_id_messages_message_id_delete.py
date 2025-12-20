from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_channel_message_channels_channel_id_messages_message_id_delete_response_delete_channel_message_channels_channel_id_messages_message_id_delete import DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete
from ...models.http_validation_error import HTTPValidationError
from typing import cast



def _get_kwargs(
    channel_id: str,
    message_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/channels/{channel_id}/messages/{message_id}".format(channel_id=quote(str(channel_id), safe=""),message_id=quote(str(message_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete.from_dict(response.json())



        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    channel_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError]:
    """ Delete Channel Message

     Delete a message from a channel.

    This endpoint deletes a message via the abstract chat interface.

    Args:
        channel_id: Identifier of the channel.
        message_id: Identifier of the message to delete.

    Returns:
        A confirmation dictionary.

    Raises:
        HTTPException: If deletion fails.

    Args:
        channel_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError]
     """


    kwargs = _get_kwargs(
        channel_id=channel_id,
message_id=message_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    channel_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError | None:
    """ Delete Channel Message

     Delete a message from a channel.

    This endpoint deletes a message via the abstract chat interface.

    Args:
        channel_id: Identifier of the channel.
        message_id: Identifier of the message to delete.

    Returns:
        A confirmation dictionary.

    Raises:
        HTTPException: If deletion fails.

    Args:
        channel_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError
     """


    return sync_detailed(
        channel_id=channel_id,
message_id=message_id,
client=client,

    ).parsed

async def asyncio_detailed(
    channel_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError]:
    """ Delete Channel Message

     Delete a message from a channel.

    This endpoint deletes a message via the abstract chat interface.

    Args:
        channel_id: Identifier of the channel.
        message_id: Identifier of the message to delete.

    Returns:
        A confirmation dictionary.

    Raises:
        HTTPException: If deletion fails.

    Args:
        channel_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError]
     """


    kwargs = _get_kwargs(
        channel_id=channel_id,
message_id=message_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    channel_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError | None:
    """ Delete Channel Message

     Delete a message from a channel.

    This endpoint deletes a message via the abstract chat interface.

    Args:
        channel_id: Identifier of the channel.
        message_id: Identifier of the message to delete.

    Returns:
        A confirmation dictionary.

    Raises:
        HTTPException: If deletion fails.

    Args:
        channel_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteChannelMessageChannelsChannelIdMessagesMessageIdDeleteResponseDeleteChannelMessageChannelsChannelIdMessagesMessageIdDelete | HTTPValidationError
     """


    return (await asyncio_detailed(
        channel_id=channel_id,
message_id=message_id,
client=client,

    )).parsed
