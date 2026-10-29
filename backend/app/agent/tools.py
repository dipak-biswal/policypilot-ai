import ast
import operator as op
from datetime import date, timedelta

from langchain_core.tools import tool

from app.generation.citations import build_context
from app.retrieval.search import search

# --- safe calculator: only + - * / % ** and brackets, never eval() ---
_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Only numbers and + - * / % ** are allowed")


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression, e.g. '500000 * 0.2' or '(1800 - 500) / 2'.
    Use this for ANY maths on numbers from the document (percentages, co-pay, totals).
    """
    try:
        return str(round(_eval(ast.parse(expression, mode="eval").body), 2))
    except Exception as e:
        return f"Error: {e}"


@tool
def date_calculator(start: str, days: int = 0, months: int = 0) -> str:
    """Add a period to a date. start is YYYY-MM-DD or 'today'. Returns the resulting date.
    Use for questions like 'when does my 24-month waiting period end if I bought on 2025-03-01?'
    """
    d = date.today() if start == "today" else date.fromisoformat(start)
    month = d.month - 1 + months
    year, month = d.year + month // 12, month % 12 + 1
    day = min(d.day, 28)  # keep it valid for every month
    result = date(year, month, day) + timedelta(days=days)
    return result.isoformat()
