# State Transition Pipeline

This pipeline validates bidirectional state transitions with a focus on race-condition elimination and idempotency.

## Technical Implementation

1. **Logic Inversion**: The transition predicate verifies the current state matches the expected source before applying the terminal state.
2. **Symmetry Validation**: Both `full_pipeline_demo.js` and `full_pipeline_demo.py` verify the A -> B and B -> A transitions.
3. **Atomic Guard**: The Python implementation utilizes a Lua script to encapsulate the 'check-and-set' operation, preventing TOCTOU vulnerabilities.

## Execution

### JavaScript Symmetry Test

node full_pipeline_demo.js


### Python Atomic & Persistence Test

python3 full_pipeline_demo.py

