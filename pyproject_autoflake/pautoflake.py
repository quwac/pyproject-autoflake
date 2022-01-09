import os
import re
import signal
import sys
from typing import Dict, List, Optional, Tuple, Union

import autoflake
import toml


def _get_argv_from_toml(pyproject_path: Optional[str] = None) -> List[str]:
    if pyproject_path is None:
        pyproject_path = os.path.join(os.getcwd(), "pyproject.toml")
    assert (
        pyproject_path is not None and pyproject_path != "" and os.path.exists(pyproject_path)
    ), f"pyproject.toml not found. {pyproject_path}"

    with open(pyproject_path, "r") as f:
        obj = toml.load(f)

    argv0 = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    arg_pairs: List[Tuple[str, Union[None, str, int]]] = [(argv0, None)]
    arg_name_to_index: Dict[str, int] = {}

    try:
        try:
            tool = obj["tool"]
            tool_autoflake: Dict[str, Union[str, bool, int]] = tool["autoflake"]
        except Exception as e:
            raise ValueError(f"[tool.autoflake] section not found in {pyproject_path}.") from e

        for key, value in tool_autoflake.items():
            if key is None or key == "":
                continue

            assert value is not None, f"tool.autoflake.{key} must be not null."
            type_value = type(value)
            assert (
                type_value is bool or type_value is int or type_value is str
            ), f"tool.autoflake.{key} must be bool or string, but {type_value}"
            del type_value

            if len(key) == 1:
                arg_name = f"-{key}"
            else:
                arg_name = f"--{key}"

            arg_value: Union[None, str, int] = None
            if type(value) is bool:
                if not value:
                    continue
            elif type(value) is int:
                arg_value = value
            elif type(value) is str:
                if value == "":
                    continue
                arg_value = value
            else:
                raise ValueError(f"Logic error. key={key},value={value}")

            arg_pairs.append((arg_name, arg_value))
            arg_name_to_index[arg_name] = len(arg_pairs) - 1
    except Exception:
        pass

    for arg in sys.argv[1:]:
        arg_pairs.append((arg, None))

    argv = []
    for key, value in arg_pairs:
        if value is not None:
            if type(value) is str:
                argv.append(key)
                argv.append(value)
            elif type(value) is int:
                for _ in range(value):
                    argv.append(key)
        else:
            argv.append(key)

    return argv


def main() -> int:
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass
    argv = _get_argv_from_toml()

    try:
        return autoflake._main(argv=argv, standard_out=sys.stdout, standard_error=sys.stderr)
    except KeyboardInterrupt:
        return 2
