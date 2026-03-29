# Code Review - Red Teaming Student Advisor Repository

**Date:** 2026-02-06  
**Reviewer:** GitHub Copilot Agent  
**Repository:** adrianwright/red-teaming-student-advisor

## Executive Summary

This code review covers the Red Teaming Student Advisor repository, which implements an Azure AI-powered student advisor chatbot with comprehensive security testing capabilities using PyRIT and Azure Red Teaming Agent.

**Overall Assessment:** The codebase is well-structured with good documentation. Several minor issues were identified that should be addressed to improve security, code quality, and maintainability.

---

## Critical Issues ⚠️

### 1. Hardcoded Agent Name in chatbot.py
**File:** `chatbot.py` (line 93)  
**Severity:** Medium  
**Issue:** The agent name is hardcoded as "StudentAdvisor2" instead of using the environment variable.

```python
# Current:
agent = await provider.create_agent(
    name="StudentAdvisor2",
    instructions=self._get_advisor_instructions()
)

# Should be:
agent_name = os.getenv("AZURE_AI_AGENT_NAME", "StudentAdvisor")
agent = await provider.create_agent(
    name=agent_name,
    instructions=self._get_advisor_instructions()
)
```

**Recommendation:** Use the environment variable consistently throughout the codebase.

---

## High Priority Issues 🔴

### 2. Missing Error Handling for Environment Variables
**Files:** Multiple Python files  
**Severity:** Medium  
**Issue:** Several environment variables are accessed with `os.getenv()` without validation. If these variables are not set, the code will fail with unclear error messages.

**Affected Files:**
- `pyrit_tests/quickstart.py` (line 43)
- `pyrit_tests/01_basic_prompt_sending.py` (line 51)
- `pyrit_tests/02_crescendo_attack.py` (line 59)

**Recommendation:** Add validation for required environment variables at the start of each script:

```python
def validate_environment():
    """Validate required environment variables are set."""
    required_vars = ["OPENAI_CHAT_ENDPOINT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
```

### 3. SQLite Memory Path Management
**Files:** PyRIT test files  
**Severity:** Medium  
**Issue:** Some scripts use in-memory SQLite (`:memory:`), while others use persistent SQLite without specifying a path. This can lead to unintended database files being created in the working directory.

**Example:** `pyrit_tests/01_basic_prompt_sending.py` (line 42)
```python
memory = SQLiteMemory()  # Creates pyrit_dbs/ directory in current location
```

**Recommendation:** Consistently use a dedicated directory for persistent storage or in-memory for temporary tests:
```python
memory = SQLiteMemory(db_path="results/pyrit_memory.db")
```

### 4. Temperature Value Edge Case
**File:** `pyrit_tests/02_crescendo_attack.py` (line 197)  
**Severity:** Low  
**Issue:** Temperature is set to 1.2, which is beyond the typical OpenAI range of 0.0-1.0 (though some models support higher values).

```python
adversarial_target = OpenAIChatTarget(
    api_key=api_key,
    temperature=1.2,  # May cause unexpected behavior
)
```

**Recommendation:** Use temperature values within the documented range (0.0-1.0) or add a comment explaining why a higher value is intentional.

---

## Medium Priority Issues 🟡

### 5. Inconsistent Exception Handling
**Files:** Multiple test scripts  
**Severity:** Low-Medium  
**Issue:** Exception handling is inconsistent across the codebase. Some scripts have try-catch blocks, others don't.

**Example:** `pyrit_tests/01_basic_prompt_sending.py` (lines 127-146)  
Has a try-catch, but doesn't clean up resources properly.

**Recommendation:** Implement consistent exception handling with proper resource cleanup:
```python
try:
    # code
except Exception as e:
    logger.error(f"Error: {e}")
    raise
finally:
    # cleanup
```

### 6. Missing Type Hints
**Files:** All Python files  
**Severity:** Low  
**Issue:** Type hints are minimal or absent in most functions, reducing code maintainability and IDE support.

**Example:** `chatbot.py`
```python
# Current:
def _get_advisor_instructions():
    return """..."""

# Better:
def _get_advisor_instructions() -> str:
    return """..."""
```

**Recommendation:** Add type hints to all function signatures for better code quality.

### 7. Magic Numbers and Strings
**Files:** Multiple files  
**Severity:** Low  
**Issue:** Several magic numbers and strings are used throughout the code without explanation.

**Examples:**
- `pyrit_tests/01_basic_prompt_sending.py`: `percentage=40.0` (line 77)
- `ai_red_teaming_agent_tests/create_red_team_run.py`: `num_conversation_turns = 5` (line 341)

**Recommendation:** Define constants with descriptive names:
```python
DEFAULT_RANDOM_CAP_PERCENTAGE = 40.0
DEFAULT_CONVERSATION_TURNS = 5
```

### 8. Incomplete Test Coverage
**Severity:** Medium  
**Issue:** The codebase lacks unit tests. Only integration/functional tests exist in the form of PyRIT demos.

**Recommendation:** Add unit tests for:
- `chatbot.py` functions
- Environment variable validation
- Helper functions in test scripts

### 9. Hardcoded File Paths
**File:** `ai_red_teaming_agent_tests/create_red_team_run.py` (line 162)  
**Severity:** Low  
**Issue:** File paths are hardcoded as strings rather than using Path objects consistently.

```python
# Current:
temp_path = Path("results/sme_test_cases_upload.jsonl")

# Better:
results_dir = Path(__file__).parent / "results"
temp_path = results_dir / "sme_test_cases_upload.jsonl"
```

---

## Low Priority Issues / Suggestions 🔵

### 10. Documentation Improvements
**Files:** Python source files  
**Severity:** Low  
**Issue:** While README files are comprehensive, inline documentation (docstrings) could be more detailed.

**Recommendation:**
- Add detailed docstrings with parameter descriptions and return types
- Include usage examples in docstrings
- Document expected exceptions

### 11. Logging Consistency
**File:** `chatbot.py` (line 17)  
**Severity:** Low  
**Issue:** Logging is configured to ERROR level only. More granular logging would be beneficial for debugging.

```python
logging.basicConfig(
    level=logging.ERROR,  # Too restrictive
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Recommendation:** Use environment variable for log level or INFO as default:
```python
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
```

### 12. String Formatting Consistency
**Files:** Multiple files  
**Severity:** Low  
**Issue:** Mix of string formatting styles (f-strings, format(), %-formatting).

**Recommendation:** Standardize on f-strings for consistency and readability.

### 13. TODO/FIXME Comments
**Severity:** Low  
**Issue:** No TODO or FIXME comments found, but some areas could benefit from them for future improvements.

**Recommendation:** Add TODO comments for:
- Performance optimization opportunities
- Future feature additions
- Technical debt items

---

## Security Considerations 🔒

### 14. Credential Management
**Status:** ✅ Good  
The code properly uses Azure credential providers (`AzureCliCredential`, `DefaultAzureCredential`) and the PyRIT auth helper (`get_azure_openai_auth`) instead of hardcoding API keys.

### 15. Environment Variable Security
**Status:** ⚠️ Needs Improvement  
**Issue:** The `.env.template` file is missing. This would help users understand what environment variables are needed without exposing sensitive values.

**Recommendation:** Create `.env.template` file:
```env
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
AZURE_RESOURCE_GROUP_NAME=your-resource-group-here
# ... etc
```

### 16. Input Validation
**Status:** ⚠️ Needs Improvement  
**Issue:** Limited input validation in the chatbot and test scripts.

**Recommendation:** Add input validation for:
- User input length limits
- Special character handling
- File path validation before file operations

---

## Best Practices & Code Quality

### ✅ Good Practices Observed
1. **Async/await usage:** Proper use of async/await throughout the codebase
2. **Context managers:** Good use of context managers for resource management
3. **Separation of concerns:** Clear separation between chatbot, PyRIT tests, and Azure red teaming
4. **Documentation:** Comprehensive README files with clear instructions
5. **Environment-based configuration:** Using `.env` files for configuration
6. **Gitignore:** Comprehensive `.gitignore` file excluding sensitive data

### ❌ Areas for Improvement
1. **Testing:** Add unit tests
2. **Type hints:** Add type annotations throughout
3. **Error handling:** More consistent and comprehensive error handling
4. **Logging:** More detailed logging for debugging
5. **Code duplication:** Some code patterns repeated across test files

---

## Specific File Recommendations

### chatbot.py
- ✅ Well-structured and readable
- ⚠️ Fix hardcoded agent name (line 93)
- ⚠️ Add type hints
- ⚠️ Improve error messages

### PyRIT Test Files
- ✅ Good demonstration of PyRIT capabilities
- ⚠️ Consolidate common setup code into a shared module
- ⚠️ Add environment variable validation
- ⚠️ Improve error handling and cleanup

### create_red_team_run.py
- ✅ Comprehensive and well-documented
- ⚠️ Function `_to_json_primitive` could be in a utility module
- ⚠️ Long function (440 lines) should be broken down
- ⚠️ Add more granular error handling

---

## Performance Considerations

1. **Memory usage:** SQLite in-memory databases are efficient, but persistent storage should be managed carefully to avoid accumulation.
2. **API rate limiting:** No rate limiting logic detected. Consider adding retry logic with exponential backoff.
3. **Concurrent requests:** No concurrent request handling observed. Consider adding for better performance.

---

## Recommendations Summary

### Immediate Actions (High Priority)
1. Fix hardcoded agent name in `chatbot.py`
2. Add environment variable validation to all scripts
3. Standardize SQLite memory path management
4. Fix temperature value edge case

### Short-term Actions (Medium Priority)
5. Add comprehensive error handling
6. Add type hints to all functions
7. Create constants for magic numbers
8. Create `.env.template` file
9. Add input validation

### Long-term Actions (Low Priority)
10. Add unit tests
11. Improve logging granularity
12. Consolidate common code into shared utilities
13. Add performance monitoring
14. Consider adding rate limiting and retry logic

---

## Conclusion

The Red Teaming Student Advisor repository is a well-designed project with good documentation and proper security practices for credential management. The main areas for improvement are:
- Code quality (type hints, error handling)
- Testing coverage
- Configuration management
- Code consistency

With these improvements, the codebase will be more maintainable, testable, and robust.

---

## Appendix: Files Reviewed

### Core Files
- `chatbot.py` - Main chatbot implementation
- `requirements.txt` - Python dependencies

### PyRIT Tests
- `pyrit_tests/quickstart.py`
- `pyrit_tests/01_basic_prompt_sending.py`
- `pyrit_tests/02_crescendo_attack.py`
- `pyrit_tests/03_scoring_evaluation.py`
- `pyrit_tests/04_qr_code_attacks.py`
- `pyrit_tests/05_memory_analysis.py`
- `pyrit_tests/run_all_demos.py`

### Azure Red Teaming
- `ai_red_teaming_agent_tests/create_red_team_run.py`

### Documentation
- `README.md`
- `pyrit_tests/README.md`
- `.github/copilot-instructions.md`

### Configuration
- `.gitignore`
- `azure.yaml`
- `.env.template` (missing - recommended to create)
