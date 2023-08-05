import logging
from datazen import DEFAULT_TYPE as DEFAULT_TYPE
from datazen.code import ARBITER as ARBITER
from typing import Any, Tuple

LOG: Any

def write_dir(directory: str, data: dict, out_type: str = ...) -> None: ...
def str_compile(configs: dict, data_type: str, logger: logging.Logger = ...) -> str: ...
def get_compile_output(entry: dict, default_type: str = ...) -> Tuple[str, str]: ...
