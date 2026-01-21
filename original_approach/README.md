# Original Red Teaming Approach

This folder contains the original, manual red teaming approach for testing the StudentAdvisor chatbot.

## Files

- **`red_teaming.py`** - The main red teaming script with 28 manually defined attack vectors across 9 categories
- **`test_agent_connection.py`** - Simple connection test to verify agent access

## Approach Overview

### Attack Categories Tested:
1. **Direct Prohibited Requests** - Straightforward asks for forbidden content
2. **Indirect/Reframed Requests** - Asking about prohibited topics indirectly  
3. **Role-Playing Bypass** - Attempting to bypass by assuming different roles
4. **Hypothetical Scenarios** - Using hypothetical framing
5. **False Authority/Research Claims** - Claiming academic or research purposes
6. **Gradual Escalation** - Starting innocuous then escalating
7. **Consent/Safety Framing** - Reframing inappropriate topics as safety
8. **Pressure and Persistence** - Using social pressure tactics
9. **Legitimate Academic Questions** - Control group that should NOT be refused

### Testing Method:
- **Manual attack vectors**: 28 predefined prompts
- **Simple scoring**: Keyword-based refusal detection
- **Basic analysis**: Pass/fail with percentage calculations
- **Limited scale**: Small subset testing due to manual effort

### Key Characteristics:
- ✅ **Simple to understand** - Clear, readable test cases
- ✅ **Fast to run** - Small number of tests complete quickly
- ✅ **Direct control** - Full visibility into each test case
- ❌ **Limited coverage** - Only 28 attack vectors vs thousands possible
- ❌ **Static attacks** - No adaptation based on responses  
- ❌ **Manual effort** - Requires hand-crafting each test case
- ❌ **Basic scoring** - Simple keyword matching vs AI-powered analysis

## Usage

```bash
# Run the main red teaming script
python red_teaming.py

# Test agent connection first
python test_agent_connection.py
```

## Results Format

The original approach provides:
- **Pass/fail percentage** - Overall safety score
- **Category breakdown** - Performance by attack type
- **Failed test details** - Which specific attacks succeeded
- **JSON export** - Timestamped results file

This approach established the baseline security posture and validated that the StudentAdvisor agent properly refuses inappropriate requests while handling legitimate academic questions.