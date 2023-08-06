from typing import Iterable, Callable, Generator, Any, Union
from dataclasses import dataclass

__all__ = ("lookup", "mw_pageit", "Page")


def lookup(predicate: Callable, iterable: Iterable) -> Union[Any, None]:
    """
    Performs a lookup over the iterable and returns first value
    which meets the predicate.

    Args:

        predicate: The callable which must be called on all elements of iterable.
        iterable: The iterable.

    Returns:

        First element which meets the predicate or None if no element meets
        the  predicate.

    Examples:

        ```py
        print(lookup(lambda p: p.camera_id == 30, listofphotos))
        ```

    *Introduced in [v0.4.0](../changelog.md#v040).*
    """
    obj = [i for i in iterable if predicate(i)]
    return obj[0] if obj else None


@dataclass
class Page:
    """
    A data class representing a Page.

    Attributes:

        pages (list): A list of objects whose length is specified with `per_page` param of `helpers.mw_pageit()`
    """  # noqa: E501

    pages: list


def mw_pageit(
    mwlist: list, per_page: int, no_of_pages: int
) -> Generator[Page, None, None]:
    """
    Divides the `mwlist` into `per_page` number of dataclass `helpers.Page`s.

    Args:

        mwlist: The list to be divided into pages.
        per_page: The number of items per page.
        no_of_pages: Number of pages to return.

    Returns:

        A generator of `helpers.Page`s.

    *Introduced in [v0.4.0](../changelog.md#v040).*
    """
    yield from [
        Page(mwlist[i : i + per_page])  # noqa: E203
        for i in range(0, len(mwlist), per_page)
    ][0:no_of_pages]
