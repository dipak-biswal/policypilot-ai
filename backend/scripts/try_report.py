import json

from dotenv import load_dotenv

load_dotenv()

from app.agent.graph import graph

result = graph.invoke(
    {
        "question": "Create a detailed report of coverages, exclusions and waiting periods"
    }
)
print("Intent:", result["intent"])
print(json.dumps(result["report"], indent=2))
