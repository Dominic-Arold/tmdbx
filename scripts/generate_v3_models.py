import subprocess, pathlib

ROOT = pathlib.Path(__file__).parent.parent

subprocess.run([
    "datamodel-codegen",
    "--input",            str(ROOT / "data/tmdb_v3_openapi_patched.json"),
    "--input-file-type",  "openapi",
    "--output",           str(ROOT / "src/tmdbx/models/generated/v3.py"),
    "--output-model-type","pydantic_v2.BaseModel",
    "--openapi-scopes", "paths",
    "--use-annotated",
    "--snake-case-field",
    "--reuse-model",
    "--collapse-root-models",
    "--formatters", "ruff-format", "ruff-check"
], check=True)