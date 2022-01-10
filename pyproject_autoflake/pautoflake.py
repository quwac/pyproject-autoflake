import os
import signal
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Union

import autoflake
import toml


def _get_pyproject_toml_path(path_candidates: List[str]) -> str:
    path_in_current = os.path.join(os.getcwd(), "pyproject.toml")
    if os.path.exists(path_in_current):
        return path_in_current

    absolute_paths: List[Path] = []
    for path_candidate in path_candidates:
        path = Path(path_candidate)
        if not path.is_absolute():
            path = Path(Path.cwd(), path_candidate)
        absolute_paths.append(path.resolve())

    for absolute_path in absolute_paths:
        dir_path = absolute_path if absolute_path.is_dir() else absolute_path.parent
        while dir_path.exists():
            pyproject_toml_path = Path(dir_path, "pyproject.toml")
            if pyproject_toml_path.exists() and pyproject_toml_path.is_file():
                return str(pyproject_toml_path)
            next_dir_path = dir_path.parent
            if next_dir_path == dir_path:
                break
            dir_path = next_dir_path

    raise ValueError("pyproject.toml not found.")


def _get_argv_from_toml(pyproject_path: str) -> List[str]:
    assert (
        pyproject_path is not None and pyproject_path != "" and os.path.exists(pyproject_path)
    ), f"pyproject.toml not found. {pyproject_path}"

    with open(pyproject_path, "r") as f:
        obj = toml.load(f)

    arg_pairs: List[Tuple[str, Union[None, str, int]]] = [(sys.argv[0], None)]
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

    path_candidates = list(filter(lambda arg: not arg.startswith("-"), sys.argv[1:]))
    if len(path_candidates) == 0:
        return autoflake._main(argv=[sys.argv[0], "-h"], standard_out=sys.stdout, standard_error=sys.stderr)
    pyproject_toml = _get_pyproject_toml_path(path_candidates)
    argv = _get_argv_from_toml(pyproject_toml)

    try:
        return autoflake._main(argv=argv, standard_out=sys.stdout, standard_error=sys.stderr)
    except KeyboardInterrupt:
        return 2
