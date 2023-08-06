from typing import Any, Optional

import httpx

__all__ = (
    "MarsworksError",
    "BadStatusCodeError",
    "ContentTypeError",
    "BadContentError",
    "BadArgumentError",
)


class MarsworksError(Exception):
    """
    Base class for all marsworks exceptions.

    Attributes:

        error (str): The error message.
    """

    __slots__ = ("headers",)

    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(self.error)


class BadStatusCodeError(MarsworksError):
    """
    Raised when a bad status code is recieved.

    Attributes:

        reason (str): The reason phrase of status.
        status (int): The status code of response.
    """

    __slots__ = ("reason", "status")

    def __init__(self, response: httpx.Response) -> None:
        self.reason = response.reason_phrase
        self.status = response.status_code
        super().__init__(
            f"Encountered Bad status code of <{self.status} "
            f"{self.reason}> from the API."
        )


class ContentTypeError(MarsworksError):
    """
    Raised when content recieved is neither application/json nor image/jpeg.

    Attributes:

        content_type (str): The content type API returned.
    """

    __slots__ = ("content_type",)

    def __init__(self, response: httpx.Response) -> None:
        self.content_type = response.headers["content-type"]
        super().__init__(
            "Expected <application/json; charset=utf-8> or "
            f"<image/jpeg> got <{self.content_type}>."
        )


class BadContentError(MarsworksError):
    """
    Raised when API returns bad or malformed content.
    """

    __slots__ = ("_content", "_message")

    def __init__(
        self, *, content: Optional[Any] = None, message: Optional[str] = None
    ) -> None:
        self._content = content
        self._message = (
            f"Recieved malformed/bad content <{self._content}>."
            if not message
            else message
        )

        super().__init__(self._message)


class BadArgumentError(MarsworksError):
    """
    Raised when bad values are supplied to any method.

    Attributes:

        expected (str): The type of arg this method expected.
        got (str): The type of arg this method got.

    Silently Deprecated in [0.5.0](../changelog.md#v050).
    """

    __slots__ = ("expected", "got")

    def __init__(self, expected: str, got: str) -> None:
        self.expected = expected
        self.got = got

        super().__init__(
            f"Expected arg of type <{self.expected}> " f"but got <{self.got}>."
        )
