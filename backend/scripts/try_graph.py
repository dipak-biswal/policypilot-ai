from dotenv import load_dotenv

load_dotenv()


from app.agent.graph import graph

for q in [
    "What is the waiting period for pre-existing diseases?",
    "Summarise this policy",
]:
    result = graph.invoke({"question": q})
    print(f"\n=== [{result['intent']}] {q}\n{result['answer']}")
    print("Cited pages:", [c["page"] for c in result["citations"]])
