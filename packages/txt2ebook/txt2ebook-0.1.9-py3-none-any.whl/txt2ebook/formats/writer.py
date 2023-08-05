import logging
import sys
from importlib import import_module

logger = logging.getLogger(__name__)


class Writer:
    """
    Module to generate different ebook format.
    """

    def __init__(self, format_writer, content, kwargs):
        self.format_writer = format_writer
        self.content = content
        self.kwargs = kwargs

    @classmethod
    def from_format(cls, content, kwargs, fmt=None):
        """
        Factory method to create ebook generator by format.
        """
        # TODO: kwargs can be overwritten globally.
        if fmt:
            kwargs["format"] = fmt

        class_name = Writer.to_classname(kwargs["format"], "Writer")

        try:
            module = import_module("txt2ebook.formats")
            klass = getattr(module, class_name)
            logger.info("Generating ebook using %s", class_name)

            writer = klass(content, kwargs)
            return cls(writer, content, kwargs)
        except AttributeError:
            logger.error("No writer found for format: %s", kwargs["format"])
            sys.exit(None)

    def write(self):
        """
        Generate the ebook to external file.
        """
        return self.format_writer.write()

    @staticmethod
    def to_classname(words, suffix):
        """
        Generate class name from words.
        """
        return words.replace("-", " ").title().replace(" ", "") + suffix
