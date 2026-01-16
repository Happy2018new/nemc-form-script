# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

from .option import OptionString, OptionInt

PACKET_NAME_MODAL_FORM_REQUEST = "packet.ModalFormRequest"
PACKET_NAME_MODAL_FORM_RESPONSE = "packet.ModalFormResponse"
PACKET_NAME_CLIENT_BOUND_CLOSE_FORM = "packet.ClientBoundCloseForm"
PACKET_NAME_SERVER_BOUND_CLOSE_FORM = "packet.ServerBoundCloseForm"
PACKET_NAME_CUSTOM_FUNCTION_CALL = "packet.CustomFunctionCall"

MODAL_FORM_CANCEL_REASON_USER_CLOSED = 0
MODAL_FORM_CANCEL_REASON_USER_BUSY = 1


class BasePacket:
    """BasePacket is the base class for all packets."""

    def __init__(self):  # type: () -> None
        """Initializes and returns a new BasePacket."""
        pass

    def packet_name(self):  # type: () -> str
        """packet_name returns the name of current packet.

        Returns:
            str: The name of current packet.
        """
        return ""

    def marshal(self):  # type: (Any) -> dict[str, Any]
        """
        marshal encode current packet
        to its JSON representation.

        Returns:
            dict[str, Any]: The JSON representation of current packet.
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> BasePacket
        """
        unmarshal decodes current packet
        from its JSON representation.

        Args:
            data (Any): The given data to decode.
                        Should be a dict.

        Returns:
            BasePacket: The packet itself.
        """
        _ = data
        return self


class ModalFormRequest(BasePacket):
    """
    ModalFormRequest is sent by the server to make the client open a form.
    This form may be either a modal form which has two options,
    a menu form for a selection of options and a custom form for properties.
    """

    form_id = 0  # type: int
    form_data = {}  # type: dict[str, Any]

    def __init__(self, form_id=0, form_data={}):  # type: (int, dict[str, Any]) -> None
        """Returns a new ModalFormRequest packet.

        Args:
            form_id (int, optional):
                form_id is an ID used to identify the form.
                The ID is saved by the client and sent back when the player submits the form,
                so that the server can identify which form was submitted.
                Defaults to 0.
            form_data (dict, optional):
                form_data is a JSON encoded object of form data. The content of the object differs,
                depending on the type of the form sent, which is also set in the JSON.
                Defaults to {}.
        """
        self.form_id = form_id
        self.form_data = form_data if len(form_data) > 0 else {}

    def packet_name(self):  # type: () -> str
        """packet_name returns the name of current packet.

        Returns:
            str: The name of current packet.
        """
        return PACKET_NAME_MODAL_FORM_REQUEST

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encode current packet
        to its JSON representation.

        Returns:
            dict[str, Any]: The JSON representation of current packet.
        """
        return {
            "FormID": self.form_id,
            "FormData": self.form_data,
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormRequest
        """
        unmarshal decodes current packet
        from its JSON representation.

        Args:
            data (Any): The given data to decode.
                        Should be a dict.

        Returns:
            ModalFormRequest: The packet itself.
        """
        self.form_id = 0
        self.form_data = {}
        if not isinstance(data, dict):
            return self

        form_id = data.get("FormID", 0)
        form_data = data.get("FormData", {})

        if not isinstance(form_id, bool) and isinstance(form_id, int):
            self.form_id = form_id
        if isinstance(form_data, dict):
            self.form_data = form_data
        return self


class ModalFormResponse(BasePacket):
    """
    ModalFormResponse is sent by the client in response to a ModalFormRequest,
    after the player has submitted the form sent.

    It contains the options/properties selected by the player,
    or a JSON encoded 'null' if the form was closed by clicking
    the X at the top right corner of the form.
    """

    form_id = 0
    response_data = OptionString()
    cancel_reason = OptionInt()

    def __init__(
        self, form_id=0, response_data=OptionString(), cancel_reason=OptionInt()
    ):  # type: (int, OptionString, OptionInt) -> None
        """Returns a new ModalFormResponse packet.

        Args:
            form_id (int, optional):
                form_id is the form ID of the form the client has responded to.
                It is the same as the ID sent in the ModalFormRequest,
                and may be used to identify which form was submitted.
                Defaults to 0.
            response_data (OptionString, optional):
                response_data is a JSON encoded value representing the response of the player.
                For a modal form, the response is either true or false, for a menu form,
                the response is an integer specifying the index of the button clicked,
                and for a custom form, the response is an array containing a value for each element.
                Defaults to OptionString().
            cancel_reason (OptionInt, optional):
                cancel_reason represents the reason why the form was cancelled.
                It is one of the constants above.
                Defaults to OptionInt().
        """
        if response_data.value() is None:
            response_data = OptionString()
        if cancel_reason.value() is None:
            cancel_reason = OptionInt()

        self.form_id = form_id
        self.response_data = response_data
        self.cancel_reason = cancel_reason

    def packet_name(self):  # type: () -> str
        """packet_name returns the name of current packet.

        Returns:
            str: The name of current packet.
        """
        return PACKET_NAME_MODAL_FORM_RESPONSE

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encode current packet
        to its JSON representation.

        Returns:
            dict[str, Any]: The JSON representation of current packet.
        """
        return {
            "FormID": self.form_id,
            "ResponseData": self.response_data.marshal(),
            "CancelReason": self.cancel_reason.marshal(),
        }

    def unmarshal(self, data):  # type: (Any) -> ModalFormResponse
        """
        unmarshal decodes current packet
        from its JSON representation.

        Args:
            data (Any): The given data to decode.
                        Should be a dict.

        Returns:
            ModalFormResponse: The packet itself.
        """
        self.form_id = 0
        self.response_data = OptionString()
        self.cancel_reason = OptionInt()
        if not isinstance(data, dict):
            return self

        form_id = data.get("FormID", 0)
        if not isinstance(form_id, bool) and isinstance(form_id, int):
            self.form_id = form_id

        self.response_data.unmarshal(data.get("ResponseData", {}))
        self.cancel_reason.unmarshal(data.get("CancelReason", {}))
        return self


class ClientBoundCloseForm(BasePacket):
    """
    ClientBoundCloseForm is sent by the server to clear the entire form stack of the client.
    This means that all forms that are currently open will be closed.
    This does not affect inventories and other containers.
    """

    def __init__(self):  # type: () -> None
        """Returns a new ClientBoundCloseForm packet."""
        return

    def packet_name(self):  # type: () -> str
        """packet_name returns the name of current packet.

        Returns:
            str: The name of current packet.
        """
        return PACKET_NAME_CLIENT_BOUND_CLOSE_FORM

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encode current packet
        to its JSON representation.

        Returns:
            dict[str, Any]: The JSON representation of current packet.
        """
        return {}

    def unmarshal(self, data):  # type: (Any) -> ClientBoundCloseForm
        """
        unmarshal decodes current packet
        from its JSON representation.

        Args:
            data (Any): The given data to decode.
                        Should be a dict.

        Returns:
            ClientBoundCloseForm: The packet itself.
        """
        _ = data
        return self


class ServerBoundCloseForm(BasePacket):
    """
    ServerBoundCloseForm is a custom packet that send by the
    client in response to the request of ClientBoundCloseForm.
    It is used to notify the server which form has been closed.
    """

    form_id = []  # type: list[int]

    def __init__(self, form_id=[]):  # type: (list[int]) -> None
        """
        Returns a new ServerBoundCloseForm packet.

        Args:
            form_id (list[int], optional):
                form_id contains multiple form ID of the form
                the client has responded to.
                It is the same as the ID sent in the ModalFormRequest,
                and used to identify what forms were closed.
                Defaults to [].
        """
        self.form_id = form_id if len(form_id) > 0 else []

    def packet_name(self):  # type: () -> str
        """packet_name returns the name of current packet.

        Returns:
            str: The name of current packet.
        """
        return PACKET_NAME_SERVER_BOUND_CLOSE_FORM

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encode current packet
        to its JSON representation.

        Returns:
            dict[str, Any]: The JSON representation of current packet.
        """
        return {"FormID": self.form_id}

    def unmarshal(self, data):  # type: (Any) -> ServerBoundCloseForm
        """
        unmarshal decodes current packet
        from its JSON representation.

        Args:
            data (Any): The given data to decode.
                        Should be a dict.

        Returns:
            ServerBoundCloseForm: The packet itself.
        """
        self.form_id = []
        if not isinstance(data, dict):
            return self

        form_id = data.get("FormID", [])
        if not isinstance(form_id, list):
            return self
        self.form_id = [
            i for i in form_id if not isinstance(i, bool) and isinstance(i, int)
        ]

        return self


class CustomFunctionCall(BasePacket):
    """
    CustomFunctionCall is a custom packet that send by the client to
    calling a custom function which already registered in server side.
    """

    func_name = ""
    func_args = ""

    def __init__(self, func_name="", func_args=""):  # type: (str, str) -> None
        """
        Returns a new CustomFunctionCall packet.

        Args:
            func_name (str):
                The custom function to call.
            func_args (str):
                The arguments passed to the custom function.
                Must be JSON string that encode from a list.
        """
        self.func_name = func_name
        self.func_args = func_args

    def packet_name(self):  # type: () -> str
        """packet_name returns the name of current packet.

        Returns:
            str: The name of current packet.
        """
        return PACKET_NAME_CUSTOM_FUNCTION_CALL

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encode current packet
        to its JSON representation.

        Returns:
            dict[str, Any]: The JSON representation of current packet.
        """
        return {
            "FuncName": self.func_name,
            "FuncArgs": self.func_args,
        }

    def unmarshal(self, data):  # type: (Any) -> CustomFunctionCall
        """
        unmarshal decodes current packet
        from its JSON representation.

        Args:
            data (Any): The given data to decode.
                        Should be a dict.

        Returns:
            CustomFunctionCall: The packet itself.
        """
        self.func_name = ""
        self.func_args = ""
        if not isinstance(data, dict):
            return self

        func_name = data.get("FuncName", "")
        func_args = data.get("FuncArgs", "")

        if isinstance(func_name, str):
            self.func_name = func_name
        if isinstance(func_args, str):
            self.func_args = func_args
        return self
