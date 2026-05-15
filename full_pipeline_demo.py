import os
from memanto.cli.client.sdk_client import SdkClient
from langchain.tools import Tool

AGENT_ID = "sys_eng_logic_extraction_01"

def setup_sdk():
    client = SdkClient()
    return client

def memanto_store_state(state_payload):
    client = setup_sdk()
    client.store(agent_id=AGENT_ID, payload=state_payload)
    return "State persisted"

def memanto_retrieve_state():
    client = setup_sdk()
    return client.retrieve(agent_id=AGENT_ID)

# Bind Memanto functions as LangChain Tools
tools = [
    Tool(
        name="StoreState",
        func=memanto_store_state,
        description="Persists system state to the data layer"
    ),
    Tool(
        name="RetrieveState",
        func=memanto_retrieve_state,
        description="Retrieves system state from the data layer"
    )
]

def run_demo():
    # Process 1: Ingestion
    state_update = {"version": 1, "status": "initialized"}
    tools[0].run(state_update)
    print(f"Process 1: Stored state for {AGENT_ID}")

    # Process 2: Recall (Simulating cross-process persistence)
    retrieved_state = tools[1].run({})
    print(f"Process 2: Retrieved state: {retrieved_state}")
    
    assert retrieved_state == state_update
    print("Cross-process persistence verified.")

if __name__ == "__main__":
    run_demo()
