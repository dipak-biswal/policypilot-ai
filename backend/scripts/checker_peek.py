from dotenv import load_dotenv

load_dotenv()

from app.agent.subagents.citation_checker import citation_checker

ctx = "[Page 9] 30-day waiting period for any illness. 24 months for specified diseases.\n[Page 12] Maternity expenses are excluded (Excl18)."

good = citation_checker.invoke(
    {"answer": "Specified diseases have a 24-month wait [Page 9].", "context": ctx}
)
bad = citation_checker.invoke(
    {"answer": "Maternity is covered after 9 months [Page 4].", "context": ctx}
)
print("GOOD:", good["verified"], good["issues"])
print("BAD:", bad["verified"], bad["issues"])

HONEST = "The document does not state a maternity waiting period, so I don't know."
print("HONEST:", citation_checker.invoke({"answer": HONEST, "context": ctx}))

MIXED = "Maternity expenses have a waiting period of 30 days [Page 12]."
print("MIXED:", citation_checker.invoke({"answer": MIXED, "context": ctx}))
