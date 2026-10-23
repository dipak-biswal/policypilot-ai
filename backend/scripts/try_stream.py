from app.agent.stream import stream_agent

for q in [
    "How many days of post-hospitalisation are covered?",
    "Summarise this policy",
]:
    print(f"\n### {q}")
    for event in stream_agent(q):
        print(event, end="", flush=True)
