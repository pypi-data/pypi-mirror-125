"""Module contains models for representing parsed XML data structures."""
import re
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel


class Attribute(BaseModel):
    """Represents an attribute inside XML tag."""

    name: str
    # optional, because there may be the following situation: <script async
    # src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>, notice async, it has no value
    value: Optional[str]


class Element(BaseModel):
    """Represents an element of XML dom tree."""

    tag_name: Optional[str]
    attributes: Optional[list[Attribute]] = []
    parent: Optional["Element"]
    children: Optional["list[Element]"] = []
    text: Optional[str]

    def find_all(self, tag_name: str, *, nested: bool = True):
        """
        Generator method yielding all elements having a given tag_name in the subtree of the current element.\n
        By default, nested parameter is equal to True, this means that find_all will traverse the whole subtree of the
        given element.\n
        If nested is set to False, then it is implied that elements to be searched don't contain
        other elements with the same tag_name.\n
        Summing up, if XML structure is rather complicated, and we are acknowledged that searched elements don't
        contain elements with the same tag_name, then providing this option may drastically speed up elements searching.
        """
        for child in self.children:
            if child.tag_name == tag_name:
                yield child
                if not nested:
                    continue
            yield from child.find_all(tag_name)

    def find(self, tag_name: str) -> "Element":
        """Returns the next element with the given tag_name in the subtree relatively to the current one. Returns an
        empty Element if not found."""
        for child in self.children:
            if child.tag_name == tag_name:
                return child
            else:
                next_child = child.find(tag_name)
            try:
                if next_child.tag_name == tag_name:
                    return next_child
            except AttributeError:
                pass
        return Element()

    def _find_all_urls(self):
        """Generator private method yielding all URLs in the subtree of the given element. Element's text for URL
        presence is explored as well as its attributes."""
        for child in self.children:
            if re.match("http", child.text):
                yield child.text
            for attr in child.attributes:
                if attr.value and re.match("http", attr.value):
                    yield attr.value
            yield from child._find_all_urls()

    def find_urls(self):
        """Public method returning a set of URLs in the subtree of the given element. Whenever several URLs having
        different parameters and pointing to the same image encountered, image with higher resolution is chosen."""
        urls_dict = {}
        # splitting URLs by the groups
        for url in self._find_all_urls():
            url_no_params = urlparse(url).path
            if url_no_params not in urls_dict:
                urls_dict[url_no_params] = []
            urls_dict[url_no_params].append(url)
        return {max(similar_urls_group) for similar_urls_group in urls_dict.values()}

    def _find_text(self):
        """Generator method yielding all stripped text occurrences in the subtree of the current element."""
        for child in self.children:
            if not child.tag_name:
                yield child.text.strip()
            yield from child._find_text()

    def get_element_text(self, tag_name: str):
        """Returns concatenated text occurrences in the subtree of the item specified by the given tag_name, which,
        in turn, is situated in the subtree of the current item."""
        try:
            return " ".join(part for part in self.find(tag_name)._find_text() if part)
        except AttributeError:
            return ""

    def __str__(self):
        return f"<{self.tag_name}>"

    def __repr__(self):
        return f"<{self.tag_name}>"

    def __eq__(self, other: "Element"):
        if (
            self.tag_name == other.tag_name
            and self.attributes == other.attributes
            and self.text == other.text
        ):
            for self_child, other_child in zip(self.children, other.children):
                if self_child != other_child:
                    return False
            return True
        else:
            return False
