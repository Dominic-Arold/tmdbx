from typing import Any
from enum import StrEnum
from tmdbx.endpoints._def import ParamDef, ParamKind

class AccountObjectIdDef(ParamDef):
    name:        str       = "account_object_id"
    kind:        ParamKind = ParamKind.PATH
    description: str       = "The v4 account object ID"


class PageDef(ParamDef):
    name:        str      = "page"
    kind:        ParamKind = ParamKind.QUERY
    python_type: str      = "int"
    required:    bool     = False
    default:     Any      = 1
    description: str      = "Page number"


class SortBy(StrEnum):
    created_at_asc  = "created_at.asc"
    created_at_desc = "created_at.desc"


class SortByDef(ParamDef):
    name:        str       = "sort_by"
    kind:        ParamKind = ParamKind.QUERY
    required:    bool      = False
    default:     Any       = SortBy.created_at_asc
    description: str       = "Sort order"


class Language(StrEnum):
    en_US = "en-US"


class LanguageDef(ParamDef):
    name:        str       = "language"
    kind:        ParamKind = ParamKind.QUERY
    required:    bool      = False
    default:     Any       = Language.en_US
    description: str       = "Language"