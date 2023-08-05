"""
Module for generating epub file.
"""
import logging
from pathlib import Path

from ebooklib import epub

SPACE = "\u0020"

logger = logging.getLogger(__name__)


class EpubWriter:
    """
    Module for writing ebook in epub format.
    """

    def __init__(self, content, opts):
        self.content = content
        self.input_file = opts["input_file"]
        self.output_file = opts["output_file"]
        self.title = opts["title"]
        self.language = opts["language"]
        self.author = opts["author"]
        self.cover = opts["cover"]

    def write(self):
        """
        Optionally backup and overwrite the txt file.
        """
        book = epub.EpubBook()

        if self.title:
            book.set_title(self.title)

        if self.language:
            book.set_language(self.language)

        if self.author:
            book.add_author(self.author)

        if self.cover:
            with open(self.cover, "rb") as image:
                book.set_cover("cover.jpg", image.read())
                book.spine += ["cover"]

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine += ["nav"]
        for header, body in self.content:
            if isinstance(body, list):
                logger.debug(header)
                html_chapters = []
                for chapter_title, chapter_body in body:
                    html_chapter = EpubWriter._build_html_chapter(
                        chapter_title, chapter_body, header
                    )
                    book.add_item(html_chapter)
                    book.spine += [html_chapter]
                    html_chapters.append(html_chapter)
                book.toc += [(epub.Section(header), html_chapters)]
            else:
                html_chapter = EpubWriter._build_html_chapter(
                    header, body, None
                )
                book.add_item(html_chapter)
                book.spine += [html_chapter]
                book.toc += [html_chapter]

        output_filename = self._gen_output_filename()
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(output_filename, book, {})
        logger.info("Generating epub file: '%s'.", output_filename)

    def _gen_output_filename(self):
        """
        Determine the output epub filename.
        """
        return Path(
            self.output_file
            or Path(self.title or self.input_file).stem + ".epub"
        )

    @staticmethod
    def _build_html_chapter(title, body, volume=None):
        """
        Generates the whole chapter to HTML.
        """
        if volume:
            filename = f"{volume}_{title}"
            logger.debug("%s%s", SPACE * 2, title)
        else:
            filename = title
            logger.debug(title)

        filename = filename.replace(SPACE, "_")

        html = f"<h2>{title}</h2>"
        for paragraph in body.split("\n\n"):
            paragraph = paragraph.replace(SPACE, "").replace("\n", "")
            html = html + f"<p>{paragraph}</p>"

        return epub.EpubHtml(
            title=title,
            content=html,
            file_name=filename + ".xhtml",
        )
