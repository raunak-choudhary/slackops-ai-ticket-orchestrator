from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.message_out import MessageOut





T = TypeVar("T", bound="PostMessageResponse")



@_attrs_define
class PostMessageResponse:
    """ Response payload for posting a message to a channel.

    Attributes:
        message: The posted message as returned by the service.

        Attributes:
            message (MessageOut): Public representation of a message returned by the service.

                Attributes:
                    id: Unique message identifier (provider-defined).
                    channel_id: Channel identifier where the message belongs.
                    text: Message content as plain text.
                    sender_id: Identifier of the sender when known.
                    ts: Optional timestamp-like string for UI compatibility. If the backing
                        provider does not supply one, the service may synthesize it.
     """

    message: MessageOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.message_out import MessageOut
        message = self.message.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_out import MessageOut
        d = dict(src_dict)
        message = MessageOut.from_dict(d.pop("message"))




        post_message_response = cls(
            message=message,
        )


        post_message_response.additional_properties = d
        return post_message_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
