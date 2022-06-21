from typing import List
from pygls.lsp.types.basic_structures import Diagnostic, TextEdit
from pygls.lsp.types.language_features.formatting import DocumentFormattingParams
from .format import BufToolFormatService
from .validate import BufToolValidateService


class BufToolLanguageService:
    """Buf tool Language service.
    This service manages all the operations supported
    by the LSP.
    """
    def __init__(self, server_name: str) -> None:
        self.server_name = server_name
        self.format_service = BufToolFormatService(server_name=server_name)
        self.validate_service = BufToolValidateService(server_name=server_name)

    def format_document(self, uri: str, content: str, params: DocumentFormattingParams) -> List[TextEdit]:
        """Given the document contents returns the list of TextEdits
        needed to properly format and layout the document.
        """
        return self.format_service.format(uri, content, params)

    def validate_document(self, uri: str) -> List[Diagnostic]:
        """Given the document contents returns the list of TextEdits
        needed to properly format and layout the document.
        """
        return self.validate_service.validate_document(uri)
