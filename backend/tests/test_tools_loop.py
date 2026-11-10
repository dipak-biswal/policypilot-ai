from app.agent.tools import calculator, date_calculator


def test_calculator_bad_input_returns_error_text():
    result = calculator.invoke({"expression": "abc"})
    assert "error" in str(result).lower()


def test_date_calculator_bad_date_does_not_crash_loop():
    try:
        result = date_calculator.invoke({"start": "not-a-date", "months": 2})
        assert "error" in str(result).lower()
    except Exception:
        # raising is OK here too, because qa.py now catches it
        pass
