"""
Module for parsing Simplified Chinese language txt file.
"""
import logging
import re

import cjkwrap

IDEOGRAPHIC_SPACE = "\u3000"
SPACE = "\u0020"
ZH_NUMS_WORDS = "零一二三四五六七八九十百千两"
ZH_FULLWIDTH_NUMS = "０１２３４５６７８９"
ZH_WHITESPACES = f"[{SPACE}\t{IDEOGRAPHIC_SPACE}]"
ZH_CHAPTER_SEQ = f"[.0-9{ZH_FULLWIDTH_NUMS}{ZH_NUMS_WORDS}]"
ZH_CHAPTER_REGEX = "|".join(
    [
        f"^{ZH_WHITESPACES}*第{ZH_CHAPTER_SEQ}*[章篇回折][^。\n]*$",
        f"^{ZH_WHITESPACES}*[楔引]子[^，].*$",
        f"^{ZH_WHITESPACES}*序[章幕曲]?.*$",
        f"^{ZH_WHITESPACES}*前言.*$",
        f"^{ZH_WHITESPACES}*[内容]*简介.*$",
        f"^{ZH_WHITESPACES}*[号番]外篇.*$",
        f"^{ZH_WHITESPACES}*尾声$",
    ]
)

logger = logging.getLogger(__name__)


class ZhCnParser:
    """
    Module for parsing txt format in zh-cn.
    """

    def __init__(self, content, opts):
        self.raw_content = content
        self.delete_regex = opts["delete_regex"]
        self.replace_regex = opts["replace_regex"]
        self.delete_line_regex = opts["delete_line_regex"]
        self.no_wrapping = opts["no_wrapping"]
        self.width = opts["width"]

    def parse(self):
        """
        Parse the content into volumes (optional) and chapters.
        """
        massaged_content = self.massage()
        parsed_content = self.parse_content(massaged_content)
        return (massaged_content, parsed_content)

    def massage(self):
        content = self.raw_content

        if self.delete_regex:
            content = self.do_delete_regex(content)

        if self.replace_regex:
            content = self.do_replace_regex(content)

        if self.delete_line_regex:
            content = self.do_delete_regex(content)

        if self.no_wrapping:
            content = self.do_no_wrapping(content)

        if self.width:
            content = self.do_wrapping(content)

        return content

    def do_delete_regex(self, content):
        """
        Remove words/phrases based on regex.
        """
        for delete_regex in self.delete_regex:
            content = re.sub(
                re.compile(rf"{delete_regex}", re.MULTILINE), "", content
            )
        return content

    def do_replace_regex(self, content):
        """
        Replace words/phrases based on regex.
        """
        for search, replace in self.replace_regex:
            content = re.sub(
                re.compile(rf"{search}", re.MULTILINE), rf"{replace}", content
            )
        return content

    def do_delete_line_regex(self, content):
        """
        Delete whole line based on regex.
        """
        for delete_line_regex in self.delete_line_regex:
            content = re.sub(
                re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
                "",
                content,
            )
        return content

    def do_no_wrapping(self, content):
        """
        Remove wrapping. Paragraph should be in one line.
        """
        # Convert to single spacing before we removed wrapping.
        lines = content.split("\n")
        content = "\n\n".join([line.strip() for line in lines if line])

        unwrapped_content = ""
        for line in content.split("\n\n"):
            # if a line contains more opening quote(「) than closing quote(」),
            # we're still within the same paragraph.
            # e.g.:
            # 「...」「...
            # 「...
            if line.count("「") > line.count("」"):
                unwrapped_content = unwrapped_content + line.strip()
            elif (
                re.search(r"[…。？！]{1}」?$", line)
                or re.search(r"」$", line)
                or re.match(r"^[ \t]*……[ \t]*$", line)
                or re.match(r"^「」$", line)
                or re.match(r".*[》：＊\*]$", line)
                or re.match(r".*[a-zA-Z0-9]$", line)
            ):
                unwrapped_content = unwrapped_content + line.strip() + "\n\n"
            elif re.match(ZH_CHAPTER_REGEX, line):
                # replace full-width space with half-wdith space.
                # looks nicer on the output.
                header = line.replace(IDEOGRAPHIC_SPACE * 2, SPACE).replace(
                    IDEOGRAPHIC_SPACE, SPACE
                )
                unwrapped_content = (
                    unwrapped_content + "\n\n" + header.strip() + "\n\n"
                )
            else:
                unwrapped_content = unwrapped_content + line.strip()

        return unwrapped_content

    def do_wrapping(self, content):
        """
        Wrapping and filling CJK text.
        """
        logger.info("Wrapping paragraph to width: %s.", self.width)

        paragraphs = []
        # We don't remove empty line and keep all formatting as it.
        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()

            lines = cjkwrap.wrap(paragraph, width=self.width)
            paragraph = "\n".join(lines)
            paragraphs.append(paragraph)

        wrapped_content = "\n".join(paragraphs)
        return wrapped_content

    def parse_content(self, content):
        """
        Parse the content into volumes (if exists) and chapters.
        """

        spaces = f"[{SPACE}\t{IDEOGRAPHIC_SPACE}]"
        volume_seq = f"[0-9{ZH_FULLWIDTH_NUMS}{ZH_NUMS_WORDS}]"
        volume_regex = f"^{spaces}*第{volume_seq}*[集卷册][^。~\n]*$"
        volume_pattern = re.compile(rf"{volume_regex}", re.MULTILINE)
        volume_headers = re.findall(volume_pattern, content)

        if not volume_headers:
            logger.info("Parsed 0 volumes.")
            parsed_content = self.parse_chapters(content)
            if parsed_content:
                logger.info("Parsed %s chapters.", len(parsed_content))
            else:
                logger.error("Parsed 0 chapters.")
        else:
            logger.info("Parsed %s volumes.", len(volume_headers))
            volume_bodies = re.split(volume_pattern, content)
            volumes = list(zip(volume_headers, volume_bodies[1:]))

            parsed_content = []
            for volume_header, body in volumes:
                parsed_body = self.parse_chapters(body)
                if parsed_body:
                    parsed_content.append((volume_header, parsed_body))
                else:
                    logger.error(
                        "Parsed 0 chapters for volume: '%s'.", volume_header
                    )

        return parsed_content

    def parse_chapters(self, content):
        """
        Split the content of txt file into chapters by chapter header.
        """
        chapter_pattern = re.compile(ZH_CHAPTER_REGEX, re.MULTILINE)
        chapter_headers = re.findall(chapter_pattern, content)

        if not chapter_headers:
            return False

        bodies = re.split(chapter_pattern, content)
        chapters = list(zip(chapter_headers, bodies[1:]))

        return chapters
