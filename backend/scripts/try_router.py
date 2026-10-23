from dotenv import load_dotenv

load_dotenv()

from app.agent.nodes.router import router_node

questions = [
    "What is the waiting period for pre-existing diseases?",
    "Give me a quick summary of this policy",
    "Create a detailed report of coverages, exclusions and waiting periods",
]

for q in questions:
    print(f"{router_node({'question': q})['intent']:8} <- {q}")
