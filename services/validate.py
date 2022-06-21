import subprocess
import re

from typing import List, Union

from pygls.lsp.types.basic_structures import Diagnostic, Position, Range, TextEdit


RE_VALIDATION = r'(\d+:\d+):\w+\s([a-zA-Z0-9\.]+):\s([a-zA-Z0-9\. ]+)'

class BufToolValidateService:
    """Buff tool format service.
    This service manages Protobuf file formatting.
    """
    def __init__(self, server_name: str) -> None:
        self.server_name = server_name

    def validate_document(self, path: str) -> List[Diagnostic]:
        """Given the document contents returns the list of TextEdits
        needed to properly layout the document.
        """
        validation_results = self.validate_content(path)
        if validation_results is None:
            return []

        diagnostics = []
        for result in validation_results.splitlines():
            matches = re.findall(RE_VALIDATION, result, re.IGNORECASE)
            if not matches:
                continue

            if len(matches[0]) != 3:
                continue

            match = matches[0]
            line = int(match[0].split(':')[0])
            column = int(match[0].split(':')[1])
            message = match[2]

            result = Diagnostic(
                range=Range(
                    start=Position(line=line - 1, character=column),
                    end=Position(line=line - 1, character=column),
                ),
                message=message,
                source=self.server_name,
            )
            diagnostics.append(result)
        return diagnostics

    def validate_content(self, path: str) -> Union[str, None]:
        """Formats the given protobuf content."""
        validations = run_buf_validate(path)
        if validations is not None:
            return validations
        return validations


def run_buf_validate(path: str) -> Union[str, None]:
    result = subprocess.run(['buf', 'lint', path.lstrip('file:')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        return None
    return result.stdout.decode("utf-8")
