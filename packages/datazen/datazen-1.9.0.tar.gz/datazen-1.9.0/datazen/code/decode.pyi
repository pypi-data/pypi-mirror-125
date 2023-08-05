import logging
from typing import Any, NamedTuple, TextIO

LOG: Any
INI_INTERPOLATION: Any

class LoadResult(NamedTuple):
    data: dict
    success: bool

def decode_ini(data_file: TextIO, logger: logging.Logger = ...) -> LoadResult: ...
def decode_json(data_file: TextIO, logger: logging.Logger = ...) -> LoadResult: ...
def decode_yaml(data_file: TextIO, logger: logging.Logger = ...) -> LoadResult: ...
