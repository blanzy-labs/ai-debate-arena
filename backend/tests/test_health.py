from fastapi.testclient import TestClient

from app.config import Settings
from app import main


def test_health_works_without_keys() -> None:
    main.settings = Settings(openai_api_key="", gemini_api_key="")

    response = TestClient(main.app).get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["openai_configured"] is False
    assert body["gemini_configured"] is False
    assert body["models"] == {
        "openai": "gpt-4.1-mini",
        "gemini": "gemini-2.5-flash",
    }
    assert "OPENAI_API_KEY" not in response.text
    assert "GEMINI_API_KEY" not in response.text
