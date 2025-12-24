# -*- coding: utf-8 -*-

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, Type


class OptionBase:
    """
    OptionBase is an optional type in the protocol.

    If not set, marshal
    ```
        {"set": False}
    ```

    Otherwise, marshal
    ```
        {"set": True, "value": ...}
    ```
    """

    _set = False  # type: bool
    _val = None  # type: Any | None
    _cls = None  # type: Type[Any] | None

    def __init__(self, cls, value=None):  # type: (Type[Any], Any) -> None
        """Creates an OptionBase[cls] with the value passed.

        Args:
            cls (Type[Any]):
                The type of the value.
                Used for type checking during runtime.
            value (cls, optional):
                The value passed.
                Defaults to None.
        """
        if not isinstance(value, cls):
            self._set = False
            self._val = None
        else:
            self._set = True if value is not None else False
            self._val = value
        self._cls = cls

    def value(self):  # type: () -> Any | None
        """
        value returns the value set in the OptionBase.
        If no value was set, None is returned.

        Returns:
            cls | None:
                If set, returns the stored cls.
                Otherwise, returns None.
        """
        if not self._set:
            return None
        return self._val

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encodes the OptionBase into a dict.

        Returns:
            dict[str, Any]:
                The dict representation of the OptionBase.
        """
        if not self._set:
            return {"set": False}
        return {
            "set": True,
            "value": self._val,
        }

    def unmarshal(self, data):  # type: (Any) -> OptionBase
        """
        unmarshal decodes the given data into the OptionBase.
        This is the inverse process of `marshal`.
        Please ensure the given data is a dict.

        Args:
            data (Any): Given data to decode.

        Returns:
            OptionBase: The OptionBase itself.
        """
        self._set = False
        self._val = None

        if self._cls is None:
            return self
        if not isinstance(data, dict):
            return self

        is_set = data.get("set", False)
        if not isinstance(is_set, bool):
            return self
        if not is_set:
            return self

        value = data.get("value", None)
        self._set = False if value is None or not isinstance(value, self._cls) else True
        self._val = value if self._set else None
        return self


class OptionString(OptionBase):
    """
    OptionString is OptionBase[str].
    """

    def __init__(self, value=None):  # type: (str | None) -> None
        """Creates an optional string with the value passed.

        Args:
            value (str | None, optional):
                The value passed.
                Defaults to None.
        """
        OptionBase.__init__(self, str, value)

    def value(self):  # type: () -> str | None
        """
        value returns the value set in the OptionString.
        If no value was set, None is returned.

        Returns:
            str | None:
                If set, returns the stored str.
                Otherwise, returns None.
        """
        return OptionBase.value(self)

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encodes the OptionString into a dict.

        Returns:
            dict[str, Any]:
                The dict representation of the OptionString.
        """
        return OptionBase.marshal(self)

    def unmarshal(self, data):  # type: (Any) -> OptionString
        """
        unmarshal decodes the given data into the OptionString.
        This is the inverse process of `marshal`.
        Please ensure the given data is a dict.

        Args:
            data (Any): Given data to decode.

        Returns:
            OptionString: The OptionString itself.
        """
        OptionBase.unmarshal(self, data)
        return self


class OptionInt(OptionBase):
    """
    OptionInt is OptionBase[int].
    """

    def __init__(self, value=None):  # type: (int | None) -> None
        """Creates an optional int with the value passed.

        Args:
            value (int | None, optional):
                The value passed.
                Defaults to None.
        """
        OptionBase.__init__(self, int, value)

    def value(self):  # type: () -> int | None
        """
        value returns the value set in the OptionInt.
        If no value was set, None is returned.

        Returns:
            int | None:
                If set, returns the stored int.
                Otherwise, returns None.
        """
        return OptionBase.value(self)

    def marshal(self):  # type: () -> dict[str, Any]
        """
        marshal encodes the OptionInt into a dict.

        Returns:
            dict[str, Any]:
                The dict representation of the OptionInt.
        """
        return OptionBase.marshal(self)

    def unmarshal(self, data):  # type: (Any) -> OptionInt
        """
        unmarshal decodes the given data into the OptionInt.
        This is the inverse process of `marshal`.
        Please ensure the given data is a dict.

        Args:
            data (Any): Given data to decode.

        Returns:
            OptionInt: The OptionInt itself.
        """
        OptionBase.unmarshal(self, data)
        return self
