from datazen.code.decode import LoadResult as LoadResult, decode_ini as decode_ini, decode_json as decode_json, decode_yaml as decode_yaml
from datazen.code.encode import encode_ini as encode_ini, encode_json as encode_json, encode_yaml as encode_yaml
from enum import Enum
from io import StringIO
from logging import Logger
from typing import Any, Callable, List, NamedTuple, Optional, TextIO

DataDecoder = Callable[[TextIO, Logger], LoadResult]
DataEncoder = Callable[[dict, StringIO], None]

class DataHandle(NamedTuple):
    extensions: List[str]
    decoder: DataDecoder
    encoder: DataEncoder

class DataType(Enum):
    JSON: Any
    YAML: Any
    INI: Any

class DataArbiter:
    encode: Any
    decode: Any
    ext_map: Any
    def __init__(self) -> None: ...
    def decoder(self, ext: str) -> Optional[DataDecoder]: ...
    def encoder(self, ext: str) -> Optional[DataEncoder]: ...

ARBITER: Any
