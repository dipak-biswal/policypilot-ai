from app.agent.graph import graph, thread_config

config = thread_config("test-thread-1")

for q in [
    "IS maternity covered?",
    "What about cataract?",
    "And its waiting period?",
]:
    result = graph.invoke({"question": q}, config=config)
    print("Q:", q)
    print("Rewritten:", result.get("standalone_question"))
    print("A:", result["answer"][:200], "\n")
