import subprocess
import os


from typing import List

from pygls.lsp.types import DocumentFormattingParams
from pygls.lsp.types.basic_structures import Position, Range, TextEdit


class BufToolFormatService:
    """Buff tool format service.
    This service manages Protobuf file formatting.
    """
    def __init__(self, server_name: str) -> None:
        self.server_name = server_name

    def format(self, path: str, contents: str, params: DocumentFormattingParams) -> List[TextEdit]:
        """Given the document contents returns the list of TextEdits
        needed to properly layout the document.
        """
        formatted_result = self.format_content(contents, params.options.tab_size)

        lines = contents.count("\n")
        start = Position(line=0, character=0)
        end = Position(line=lines + 1, character=0)
        return [TextEdit(range=Range(start=start, end=end), new_text=formatted_result)]

    def format_content(self, path: str, tabSize: int = 4) -> str:
        """Formats the given protobuf content."""
        new = run_buf_format(path)
        return new


def run_buf_format(contents: str) -> str:
    with open('./tmp.proto', 'w') as fp:
        fp.write(contents)

    result = subprocess.run(['buf', 'format', './tmp.proto'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        return result.stderr.decode('utf-8')

    os.remove('./tmp.proto')
    return result.stdout.decode("utf-8")
