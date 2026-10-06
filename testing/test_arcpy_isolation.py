import os
import subprocess
import sys
from pathlib import Path

dir_src = Path(__file__).parent.parent / "src"


def test_import_does_not_load_arcpy() -> None:
    # subprocess so arcpy loaded by other tests or conftest cannot mask a leak
    code = (
        "import sys, pkgutil, importlib, h3_route_solver;"
        "[importlib.import_module(m.name) for m in pkgutil.walk_packages("
        "h3_route_solver.__path__, 'h3_route_solver.')];"
        "sys.exit(1 if 'arcpy' in sys.modules else 0)"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, "PYTHONPATH": str(dir_src)},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"arcpy was imported by h3_route_solver\n{result.stderr}"
