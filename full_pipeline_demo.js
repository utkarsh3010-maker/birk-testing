const { SdkClient } = require('memanto.cli.client.sdk_client');

async function verifyStateSymmetry() {
  const client = new SdkClient();
  const agentId = 'sys_eng_test_001';
  const stateKey = 'system_status';
  
  const states = {
    active: 'ACTIVE',
    inactive: 'INACTIVE'
  };

  const transition = async (from, to) => {
    await client.set(agentId, { [stateKey]: to });
    const result = await client.get(agentId, stateKey);
    if (result !== to) {
      throw new Error(`State transition failed: expected ${to}, got ${result}`);
    }
    return result;
  };

  try {
    console.log('Testing Forward Transition: INACTIVE -> ACTIVE');
    await transition(states.inactive, states.active);
    
    console.log('Testing Inverse Transition: ACTIVE -> INACTIVE');
    await transition(states.active, states.inactive);
    
    console.log('Symmetry validation successful.');
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
}

verifyStateSymmetry();
