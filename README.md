# Logic Extraction: Dependency Elimination

This implementation replaces external synchronization libraries with a lean utility and data-layer atomicity.

## Strategy
To maintain zero-dependency overhead and O(1) binary size increase, the synchronization logic was moved from the client to the data layer using Lua scripts. This ensures atomicity without client-side locking.

## Implementation
- **Client-side**: A minimal utility handles the execution of server-side scripts.
- **Data-layer**: Lua scripts perform conditional updates to prevent race conditions.
