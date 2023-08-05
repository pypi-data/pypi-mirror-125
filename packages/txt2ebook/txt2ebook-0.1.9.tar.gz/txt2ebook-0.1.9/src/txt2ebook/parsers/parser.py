import logging
import re
from importlib import import_module

from langdetect import detect

logger = logging.getLogger(__name__)


class Parser:
    """
    Module to create different parser by language.
    """

    def __init__(self, lang_parser, content, kwargs):
        self.lang_parser = lang_parser
        self.raw_content = content
        self.kwargs = kwargs

        self.massaged_content = ""
        self.parsed_content = []

    @classmethod
    def from_language(cls, content, kwargs):
        """
        Factory method to create parser by language.
        """
        kwargs["language"] = Parser.detect_language(
            content, kwargs["language"]
        )
        kwargs["author"] = kwargs["author"] or Parser.detect_author(content)
        kwargs["title"] = kwargs["title"] or Parser.detect_book_title(content)

        class_name = Parser.to_classname(kwargs["language"], "Parser")

        try:
            module = import_module("txt2ebook.parsers")
            klass = getattr(module, class_name)
            logger.info("Parsing file using %s", class_name)
        except AttributeError:
            logger.error(
                "No parser found for language: %s", kwargs["language"]
            )
            logger.info("Parsing file using EnParser")
            klass = getattr(module, "EnParser")

        parser = klass(content, kwargs)
        return cls(parser, content, kwargs)

    def parse(self):
        (massaged_content, parsed_content) = self.lang_parser.parse()
        self.massaged_content = massaged_content
        self.parsed_content = parsed_content

    @staticmethod
    def to_classname(words, suffix):
        """
        Generate class name from words.
        """
        return words.replace("-", " ").title().replace(" ", "") + suffix

    @staticmethod
    def detect_language(content, language):
        """
        Detect the language (ISO 639-1) of the content of the txt file.
        """
        language = language or detect(content)
        logger.info("Language detected: '%s'.", language)
        return language

    @staticmethod
    def detect_book_title(content):
        """
        Extract book title from the content of the txt file.
        """
        regex = r"书名：(.*)|【(.*)】|《(.*)》"
        match = re.search(regex, content)
        if match:
            book_title = next(
                (title for title in match.groups() if title is not None)
            )
            logger.info("Found book title: '%s'.", book_title)
            return book_title

        logger.info("No book title found from file!")
        return False

    @staticmethod
    def detect_author(content):
        """
        Extract author from the content of the txt file.
        """
        match = re.search(r"作者：(.*)", content)
        if match:
            author = match.group(1)
            logger.info("Found author: '%s'.", author)
            return author

        logger.info("No author found from file!")
        return False
