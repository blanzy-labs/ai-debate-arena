from pathlib import Path

from fastapi.testclient import TestClient

from app import main


REPO_ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".html", ".json", ".py", ".ts", ".tsx", ".txt"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_text(paths: list[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        if path.is_dir():
            for file_path in path.rglob("*"):
                if file_path.is_file() and file_path.suffix in TEXT_SUFFIXES:
                    chunks.append(read_text(file_path))
        elif path.is_file():
            chunks.append(read_text(path))
    return "\n".join(chunks)


def test_env_example_is_safe() -> None:
    env_example = REPO_ROOT / ".env.example"
    text = read_text(env_example)

    assert "OPENAI_API_KEY=" in text
    assert "GEMINI_API_KEY=" in text
    assert "OPENAI_MODEL=gpt-4.1-mini" in text
    assert "GEMINI_MODEL=gemini-2.5-flash" in text
    assert "VITE_OPENAI_API_KEY" not in text
    assert "VITE_GEMINI_API_KEY" not in text
    assert "sk-" not in text
    assert "AIza" not in text


def test_gitignore_protects_env_files_and_preserves_examples() -> None:
    text = read_text(REPO_ROOT / ".gitignore")

    assert ".env" in text
    assert ".env.*" in text
    assert "!.env.example" in text
    assert "backend/.env" in text
    assert "frontend/.env" in text
    assert "!backend/.env.example" in text
    assert "!frontend/.env.example" in text


def test_frontend_does_not_reference_provider_secrets() -> None:
    text = collect_text(
        [
            REPO_ROOT / "frontend" / "src",
            REPO_ROOT / "frontend" / "index.html",
            REPO_ROOT / "frontend" / "package.json",
        ]
    )

    assert "OPENAI_API_KEY" not in text
    assert "GEMINI_API_KEY" not in text
    assert "sk-" not in text
    assert "AIza" not in text


def test_backend_app_does_not_hard_code_real_looking_provider_keys() -> None:
    text = collect_text([REPO_ROOT / "backend" / "app"])

    assert "sk-" not in text
    assert "AIza" not in text


def test_no_frontend_browser_persistence() -> None:
    text = collect_text([REPO_ROOT / "frontend" / "src"])

    assert "localStorage" not in text
    assert "sessionStorage" not in text
    assert "indexedDB" not in text


def test_no_obvious_backend_storage_dependencies_or_implementation() -> None:
    requirements = read_text(REPO_ROOT / "backend" / "requirements.txt").lower()
    backend_app = collect_text([REPO_ROOT / "backend" / "app"]).lower()

    forbidden_dependencies = [
        "sqlalchemy",
        "psycopg",
        "psycopg2",
        "asyncpg",
        "pymongo",
        "redis",
        "sqlite-utils",
        "alembic",
    ]
    forbidden_app_strings = ["sqlalchemy", "pymongo", "redis", "sqlite"]

    for dependency in forbidden_dependencies:
        assert dependency not in requirements

    for app_string in forbidden_app_strings:
        assert app_string not in backend_app


def test_health_response_hides_api_key_fields_and_values() -> None:
    response = TestClient(main.app).get("/health")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["openai_configured"], bool)
    assert isinstance(body["gemini_configured"], bool)
    assert "openai_api_key" not in body
    assert "gemini_api_key" not in body
    assert "OPENAI_API_KEY" not in response.text
    assert "GEMINI_API_KEY" not in response.text
