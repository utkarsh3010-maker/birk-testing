import asyncio
from memanto.cli.client.sdk_client import SdkClient
from langchain.tools import tool

class StateManager:
    def __init__(self):
        self.client = SdkClient()
        self.agent_id = 'sys_eng_test_001'

    def get_atomic_lua_script(self):
        # Logic Inversion: Predicate evaluates terminal state to prevent double-transition
        return """
        local current = redis.call('get', KEYS[1])
        if current == ARGV[1] then
            redis.call('set', KEYS[1], ARGV[2])
            return 1
        end
        return 0
        """

@tool
def atomic_state_transition(current_state: str, target_state: str) -> bool:
    """
    Executes an atomic state transition using a Lua guard to eliminate TOCTOU race conditions.
    """
    manager = StateManager()
    lua_script = manager.get_atomic_lua_script()
    
    # Atomic Guard implementation via SDK
    success = manager.client.execute_lua(
        script=lua_script,
        keys=[f"{manager.agent_id}:system_status"],
        args=[current_state, target_state]
    )
    return bool(success)

async def run_persistence_proof():
    # Process 1: Initialize State
    client_a = SdkClient()
    agent_id = 'sys_eng_test_001'
    client_a.set(agent_id, {'system_status': 'INACTIVE'})
    
    # Verify initial state
    initial_check = client_a.get(agent_id, 'system_status')
    print(f"Initial state: {initial_check}")

    # Process 2 (Simulated): Execute Atomic Transition
    # Using the LangChain bound tool
    result_forward = atomic_state_transition.invoke({
        "current_state": "INACTIVE", 
        "target_state": "ACTIVE"
    })
    print(f"Forward transition (INACTIVE -> ACTIVE): {result_forward}")

    # Test Idempotency: Attempting the same transition again should fail
    result_idempotent = atomic_state_provision = atomic_state_transition.invoke({
        "current_state": "INACTIVE", 
        "target_state": "ACTIVE"
    })
    print(f"Idempotency check (Should be False): {result_idempotent}")

    # Symmetry Validation: Testing the other way around
    result_inverse = atomic_state_transition.invoke({
        "current_state": "ACTIVE", 
        "target_state": "INACTIVE"
    })
    print(f"Inverse transition (ACTIVE -> INACTIVE): {result_inverse}")

if __name__ == "__main__":
    asyncio.run(run_persistence_proof())
