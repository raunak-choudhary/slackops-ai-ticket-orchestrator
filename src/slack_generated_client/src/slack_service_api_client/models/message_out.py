from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="MessageOut")



@_attrs_define
class MessageOut:
    """ Public representation of a message returned by the service.

    Attributes:
        id: Unique message identifier (provider-defined).
        channel_id: Channel identifier where the message belongs.
        text: Message content as plain text.
        sender_id: Identifier of the sender when known.
        ts: Optional timestamp-like string for UI compatibility. If the backing
            provider does not supply one, the service may synthesize it.

        Attributes:
            id (str): Message identifier
            channel_id (str): Channel identifier
            text (str): Message content
            sender_id (None | str | Unset): Sender identifier
            ts (None | str | Unset): Timestamp-like string
     """

    id: str
    channel_id: str
    text: str
    sender_id: None | str | Unset = UNSET
    ts: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        channel_id = self.channel_id

        text = self.text

        sender_id: None | str | Unset
        if isinstance(self.sender_id, Unset):
            sender_id = UNSET
        else:
            sender_id = self.sender_id

        ts: None | str | Unset
        if isinstance(self.ts, Unset):
            ts = UNSET
        else:
            ts = self.ts


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "channel_id": channel_id,
            "text": text,
        })
        if sender_id is not UNSET:
            field_dict["sender_id"] = sender_id
        if ts is not UNSET:
            field_dict["ts"] = ts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        channel_id = d.pop("channel_id")

        text = d.pop("text")

        def _parse_sender_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sender_id = _parse_sender_id(d.pop("sender_id", UNSET))


        def _parse_ts(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ts = _parse_ts(d.pop("ts", UNSET))


        message_out = cls(
            id=id,
            channel_id=channel_id,
            text=text,
            sender_id=sender_id,
            ts=ts,
        )


        message_out.additional_properties = d
        return message_out

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
