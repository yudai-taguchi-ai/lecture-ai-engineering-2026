from types import SimpleNamespace

from app import ask


def test_ask_prints_time_and_token_usage(monkeypatch, capsys):
    class FakeModels:
        def generate_content(self, **kwargs):
            return SimpleNamespace(
                text="fixed answer",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=12,
                    candidates_token_count=7,
                ),
            )

    class FakeClient:
        def __init__(self, **kwargs):
            self.models = FakeModels()

    ticks = iter([1.0, 1.25])
    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask.time, "perf_counter", lambda: next(ticks))

    assert ask.ask("question") == "fixed answer"

    output = capsys.readouterr().out
    assert "[time] 0.25s" in output
    assert "[tokens] input=12 output=7" in output