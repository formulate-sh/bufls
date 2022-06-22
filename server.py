from typing import List, Optional
from pygls.lsp.methods import FORMATTING, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE
from pygls.lsp.types.basic_structures import Diagnostic
from pygls.lsp.types.language_features.formatting import DocumentFormattingParams
from pygls.lsp.types.workspace import DidChangeTextDocumentParams, DidOpenTextDocumentParams, DidSaveTextDocumentParams
from pygls.server import LanguageServer
from pygls.workspace import Document

from services.service import BufToolLanguageService


class BufLanguageServer(LanguageServer):
    def __init__(self):
        super().__init__()
        self.services = BufToolLanguageService('bufls')


language_server = BufLanguageServer()


@language_server.feature(FORMATTING)
def formatting(ls: BufLanguageServer, params: DocumentFormattingParams):
    """Formats the whole document using the provided parameters"""
    document = _get_valid_document(ls, params.text_document.uri)
    if document:
        content = document.source
        return ls.services.format_document(document.uri, content, params)
    return None


@language_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: BufLanguageServer, params: DidSaveTextDocumentParams):
    diagnostics: List[Diagnostic] = []
    document = _get_valid_document(ls, params.text_document.uri)
    if document:
        diagnostics = ls.services.validate_document(document.uri)
    ls.publish_diagnostics(params.text_document.uri, diagnostics=diagnostics)


@language_server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: BufLanguageServer, params: DidOpenTextDocumentParams):
    diagnostics: List[Diagnostic] = []
    document = _get_valid_document(ls, params.text_document.uri)
    if document:
        diagnostics = ls.services.validate_document(document.uri)
    ls.publish_diagnostics(params.text_document.uri, diagnostics=diagnostics)


@language_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: BufLanguageServer, params: DidChangeTextDocumentParams):
    diagnostics: List[Diagnostic] = []
    document = _get_valid_document(ls, params.text_document.uri)
    if document:
        diagnostics = ls.services.validate_document(document.uri)
    ls.publish_diagnostics(params.text_document.uri, diagnostics=diagnostics)


def _get_valid_document(server: BufLanguageServer, uri: str) -> Optional[Document]:
    document = server.workspace.get_document(uri)
    if _is_document_supported(document):
        return document
    return None


def _is_document_supported(document: Document) -> bool:
    """Returns True if the given document is supported by the server."""

    if not document.uri.lower().endswith(".proto"):
        return False
    return True


language_server.start_io()
