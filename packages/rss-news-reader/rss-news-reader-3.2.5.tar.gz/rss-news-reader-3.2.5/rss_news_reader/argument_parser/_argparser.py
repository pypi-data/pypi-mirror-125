"""Module which encompasses console arguments settings and parsing logics."""
import argparse


class ArgParser:
    """Class parsing console arguments."""

    def __init__(self):
        super(ArgParser, self).__init__()
        self.parser = argparse.ArgumentParser(
            prog="rss-news-reader",
            description="Pure Python command-line RSS reader.",
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=30
            ),
            add_help=False,
        )
        self.parser.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="Show this help message and exit.",
        )
        self.parser.add_argument("source", nargs="?", default=None, help="RSS URL")
        self.parser.add_argument(
            "-v",
            "--version",
            help="Print version info.",
            action="version",
            version="3.2.5",
        )
        self.parser.add_argument(
            "--verbose", help="Output verbose status messages.", action="store_true"
        )
        self.parser.add_argument(
            "-c",
            "--colorize",
            help="Print news in colorized mode.",
            action="store_true",
        )
        self.parser.add_argument(
            "--json", help="Print news as JSON.", action="store_true"
        )
        self.parser.add_argument(
            "-l",
            "--limit",
            help="Limit news amount to be processed.",
            type=int,
            default=-2,
        )
        self.parser.add_argument(
            "-d",
            "--date",
            help="Get news published on a specific date from cache for further processing.",
        )
        self.to_html_action = self.parser.add_argument(
            "--to-html",
            nargs="?",
            help="Convert news to .html format and save it by the specified folder path (FOLDER_PATH can be omitted).",
            metavar="FOLDER_PATH",
        )
        self.to_pdf_action = self.parser.add_argument(
            "--to-pdf",
            nargs="?",
            help="Convert news to .pdf format and save it by the specified folder path (FOLDER_PATH can be omitted).",
            metavar="FOLDER_PATH",
        )
        self.to_epub_action = self.parser.add_argument(
            "--to-epub",
            nargs="?",
            help="Convert news to .epub format and save it by the specified folder path (FOLDER_PATH can be omitted).",
            metavar="FOLDER_PATH",
        )
        self.parser.add_argument(
            "--check-urls",
            help="Ensure URL represents an image (requires installation of additional dependency, use: pip install "
            "aiohttp).",
            action="store_true",
        )
        self.parser.add_argument(
            "--clear-cache",
            help="Clear cache file on startup.",
            action="store_true",
        )

    @property
    def args(self) -> argparse.Namespace:
        """Property field to return parsed console arguments."""
        return self.parser.parse_args()
