"""Module providing the implementation of XML tokenization logics."""
from enum import Enum
from io import StringIO

from ._parser_models import Attribute, Element


class TokenType(Enum):
    """
    Enumeration holding types of tokens.

    Token types:

    Begin of file = 1\n
    Start tag = 2\n
    End tag = 3\n
    Text = 4\n
    End of file = 5\n
    Character data = 6
    """

    BOF = 1
    START_TAG = 2
    END_TAG = 3
    TEXT = 4
    EOF = 5
    CDATA = 6


class XMLError(Exception):
    """There was an ambiguous exception that occurred while parsing your XML."""


class EmptyXMLError(XMLError):
    """Raised if XML document was empty."""


class InvalidTagError(XMLError):
    """Raised if invalid tag was met."""


class UnexpectedCharacterError(XMLError):
    """Raised if invalid character was met in XML document."""


class EmptyAttributeNameError(XMLError):
    """Raised if an empty attribute name was met in XML document."""


class InvalidAttributeError(XMLError):
    """Raised if an invalid attribute was met in XML document."""


class UnexpectedEndOfDocumentError(XMLError):
    """Raised if an unexpected end of XML document was encountered."""


class Tokenizer:
    """Tokenizes given XML document. Supports iterator protocol. Iteration over Tokenizer instance makes it easy to
    obtain parsed tokens of XML tree."""

    def __init__(self, xml: str):
        if len(xml) == 0:
            raise EmptyXMLError("Empty XML document!")
        self.xml_io = StringIO(xml)
        self._skip_head()
        self.attributes = []
        self.token_type = TokenType.BOF
        self.text: str
        self.has_end_tag = False
        self.tag_name: str

    def _skip_head(self) -> None:
        """Skips the leading tags like <?xml version="1.0" encoding="UTF-8"?>"""
        while True:
            current = self.xml_io.tell()
            self._read_char(True)
            suspect = self._read_char()
            if suspect == "?":
                while self._read_char() != ">":
                    pass
            else:
                self.xml_io.seek(current)
                return

    def _skip_comment(self) -> None:
        """Skips commented content: <!-- wp:cgb/block-libsyn-podcasting-gutenberg -->"""
        self.xml_io.read(2)
        while True:
            while self._read_char() != "-":
                pass
            if self._read_char() == "-":
                if self._read_char() == ">":
                    self._parse_text()
                    return

    def __iter__(self):
        """Tokenizer supports iterator protocol."""
        return self

    def __next__(self) -> Element:
        """Every token is represented as Element. Each iteration private method _next_token() is called changing the
        state of Tokenizer instance before construction of another token."""
        self._next_token()
        if self.token_type == TokenType.START_TAG:
            return Element(
                tag_name=self.tag_name, attributes=self.attributes, text=self.text
            )
        elif self.token_type == TokenType.END_TAG:
            return Element(tag_name=self.tag_name)
        elif self.token_type == TokenType.TEXT or self.token_type == TokenType.CDATA:
            return Element(text=self.text)
        elif self.token_type == TokenType.EOF:
            raise StopIteration

    def _next_token(self) -> None:
        """Private method, which specifies logic on how the state of Tokenizer instance changes each iteration before
        construction of another token."""
        # skip leading whitespaces and newline characters
        if self.token_type == TokenType.BOF:
            self._parse_text()

        if (
                self.token_type == TokenType.START_TAG
                or self.token_type == TokenType.END_TAG
        ):
            # if symbol '/' is present in tag
            if self.has_end_tag:
                self._reset(reset_tag_name=False)
                self.token_type = TokenType.END_TAG
                self.has_end_tag = False
            else:
                self._reset(reset_tag_name=True)
                self._parse_text()
                # if tags are going in a row, this will let us skip adding a child with empty text:
                # <people><person /></people>
                if self.token_type == TokenType.TEXT and self.text == "":
                    self._reset(reset_tag_name=True)
                    self._parse_tag()
        elif self.token_type == TokenType.TEXT:
            self._reset(reset_tag_name=True)
            self._parse_tag()
        elif self.token_type == TokenType.CDATA:
            self._parse_text()
        elif self.token_type == TokenType.EOF:
            pass

    def _reset(self, *, reset_tag_name: bool) -> None:
        """Resets the current state of Tokenizer instance."""
        if reset_tag_name:
            self.tag_name = ""
        self.attributes.clear()
        self.text = ""

    def _match_next_chars(self, expected_str: str) -> bool:
        """Checks whether next several chars represent the expected string."""
        current = self.xml_io.tell()
        try:
            for i in range(len(expected_str)):
                if self._read_char() != expected_str[i]:
                    return False
            return True
        finally:
            self.xml_io.seek(current)

    def _match_next_char_any_of(self, chars: str) -> bool:
        """Check whether next char is any char in the given str."""
        current = self.xml_io.tell()
        try:
            if self._read_char() in chars:
                return True
            return False
        finally:
            self.xml_io.seek(current)

    def _match_closing_tag(self, skip_ws: bool) -> None:
        """Reads one char and checks whether it is '>'."""
        char = self._read_char(skip_ws)
        if char != ">":
            raise UnexpectedCharacterError(
                f"Unexpected character: expected '>', got '{char}'!"
            )

    def _read_char(self, skip_ws: bool = False) -> str:
        """Reads one char from xml_io. skip_ws option lets user skip whitespaces following in a row."""
        char = self.xml_io.read(1)
        if skip_ws:
            if char == "":
                raise UnexpectedEndOfDocumentError("Unexpected end of XML document!")
        while True:
            if char != "" and skip_ws and char.isspace():
                char = self.xml_io.read(1)
                continue
            return char

    def _parse_cdata(self) -> None:
        """Parses CDATA in XML. Firstly it extracts pure HTML from CDATA, then adds cdata_tokenizer attribute to the
        instance of the current tokenizer, which is used for recursive tokenization."""
        cdata = "<!"

        while True:
            char = self._read_char()
            cdata += char
            while char != "]":
                char = self._read_char()
                cdata += char
            char = self._read_char()
            cdata += char
            if char == "]":
                char = self._read_char()
                cdata += char
                if char == ">":
                    break

        cdata_html = cdata.removeprefix("<![CDATA[").removesuffix("]]>").strip()
        # sometimes cdata is represented as a pure text, wrap it into <html></html> tag to be sure it is html
        cdata_html = f"<html>{cdata_html}</html>"
        self.cdata_tokenizer = Tokenizer(cdata_html)
        self.token_type = TokenType.CDATA

    def _parse_text(self) -> None:
        """Parses text between tags in XML."""
        text = ""
        char = self._read_char()
        while char != "" and char != "<":
            text += char
            char = self._read_char()
        # check whether '<' is not a part of the opening tag, but a part of text
        if char == "<":
            if self._match_next_char_any_of(" -0123456789:+,'\"\\"):
                text += char
                char = self._read_char()
                while char != "" and char != "<":
                    text += char
                    char = self._read_char()
        # if not end of xml
        if char != "":
            self.token_type = TokenType.TEXT
            self.text = text
        else:
            self.token_type = TokenType.EOF

    def _parse_tag(self) -> None:
        """Parses tag in XML."""
        is_start_tag = True

        char = self._read_char()
        if char == "!":
            if self._match_next_chars("[CDATA["):
                self._parse_cdata()
            elif self._match_next_chars("--"):
                self._skip_comment()
            return

        if char == "/":
            is_start_tag = False
            char = self._read_char()

        tag_name = ""
        while char.isalnum() or char in "-:?":
            tag_name += char
            char = self._read_char()

        self.tag_name = tag_name

        if len(tag_name) == 0:
            raise InvalidTagError("Tag name was empty!")
        else:
            if is_start_tag:
                self.token_type = TokenType.START_TAG
                # end parsing tag after reaching '>' symbol
                if char == ">":
                    pass
                # in a single opening tag the next symbol after '/' must be '>': <person />
                elif char == "/":
                    self._match_closing_tag(False)
                    self.has_end_tag = True
                else:
                    # presence of any character except whitespace after tag name is incorrect: <person@id="1">
                    if not char.isspace():
                        raise InvalidTagError(
                            f"Incorrect char '{char}' encountered after tag name '{tag_name}'!"
                        )
                    # parse attributes if tag is correct: <person id="1"> or <person    id="1">
                    self.has_end_tag = self._parse_attrs()
            else:
                self.token_type = TokenType.END_TAG
                if char == ">":
                    pass
                else:
                    if not char.isspace():
                        raise InvalidTagError(
                            f"Incorrect char '{char}' encountered after tag name '{tag_name}'!"
                        )
                    # this checks if '>' is going after possible multiple whitespaces in a closing tag: </person     >
                    self._match_closing_tag(True)

    def _parse_attrs(self) -> bool:
        """Parses attributes inside XML tag. Returns True, if it is a 'single' tag: <person />, else False."""
        # skip whitespaces and read the first symbol of the name of the first attribute: <person   id="1"> -> 'i'
        char = self._read_char(True)

        while char != ">":
            if char == "/":
                # in a single opening tag the next symbol after '/' must be '>': <person id="1" />
                self._match_closing_tag(False)
                return True

            attr_name = ""

            # read attribute name
            while char.isalnum() or char in ":-":
                attr_name += char
                char = self._read_char()

            if len(attr_name) == 0:
                raise EmptyAttributeNameError(
                    f"Empty attribute name in tag <{self.tag_name}>!"
                )

            # there may be only whitespaces after tag name, we read and skip them:
            # <person id   ="1"> - ok, <person id@="1"> - not ok
            if char.isspace():
                char = self._read_char(True)

            attr_value = None
            # if attribute has value afterwards
            if char == "=":
                # read the delimiter symbol: ' or "
                char = self._read_char(True)
                if char != "'" and char != '"':
                    raise InvalidAttributeError(
                        f"Invalid attribute in tag <{self.tag_name}>!"
                    )

                delimiter = char

                char = self._read_char()

                attr_value = ""

                # read attribute value till the second delimiter
                while char != delimiter:
                    attr_value += char
                    char = self._read_char()

            # skip whitespaces and read the first symbol of the name of the next attribute or '/' if it is a single tag
            # or just '>' symbol and exit the loop
            char = self._read_char(True)
            self.attributes.append(Attribute(name=attr_name, value=attr_value))

        return False
