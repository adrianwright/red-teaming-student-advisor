# PyRIT Red Teaming Demos

Real PyRIT (Python Risk Identification Tool) demonstrations for testing the Student Advisor AI agent.

## 🎯 Overview

These demos showcase **actual PyRIT functionality** from Microsoft's AI Red Team framework, not custom implementations. Each demo focuses on different PyRIT capabilities.

## 📋 Prerequisites

```bash
pip install pyrit
pip install python-dotenv
pip install azure-ai-inference
```

## 🔧 Configuration

Create a `.env` file in the root directory with:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/project
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4

# Optional: For audio attacks
AZURE_SPEECH_REGION=eastus
AZURE_SPEECH_KEY=your-speech-key

# Optional: For Azure SQL memory
AZURE_SQL_DB_CONNECTION_STRING=your-connection-string
```

## 🚀 Demos

### Demo 1: Basic Prompt Sending (`01_basic_prompt_sending.py`)

**What it demonstrates:**
- Single-turn `PromptSendingAttack`
- 7+ different converters (Base64, ROT13, Leetspeak, Unicode, etc.)
- Converter stacking
- Privacy violation tests

**Key PyRIT features:**
- `PromptSendingAttack` - Single-turn attack executor
- `Base64Converter`, `ROT13Converter`, `LeetspeakConverter`
- `UnicodeConfusableConverter`, `RandomCapitalLettersConverter`
- `VariationConverter` (LLM-based rephrasing)
- `StringJoinConverter` (character separation)
- `AttackConverterConfig` - Converter configuration
- SQLite memory persistence

**Run it:**
```bash
python 01_basic_prompt_sending.py
```

**Expected output:**
- Test results for each converter
- Converted prompts (e.g., base64, ROT13)
- Target responses
- Success/failure summary

---

### Demo 2: Crescendo Multi-Turn Attack (`02_crescendo_attack.py`)

**What it demonstrates:**
- Multi-turn `CrescendoAttack` - PyRIT's adaptive attack
- Adversarial LLM generates progressively harmful prompts
- Automatic backtracking on refusals
- 3 different attack objectives

**Key PyRIT features:**
- `CrescendoAttack` - Multi-turn adaptive attack
- `AttackAdversarialConfig` - Adversarial LLM configuration
- `max_turns` and `max_backtracks` parameters
- Pruned conversation tracking
- Adversarial LLM conversation history
- `ConsoleAttackResultPrinter` with full details

**Attack scenarios:**
1. **Academic Dishonesty** - Get bot to write complete essay
2. **Privacy Breach** - Extract student PII
3. **Policy Circumvention** - Forge documents

**Run it:**
```bash
python 02_crescendo_attack.py
```

**Expected output:**
- Multi-turn conversation trees
- Adversarial LLM's strategy
- Backtracked attempts
- Success/failure with execution metrics

**⚠️ Note:** This can take 5-10 minutes depending on LLM latency.

---

### Demo 3: Scoring and Evaluation (`03_scoring_evaluation.py`)

**What it demonstrates:**
- Multiple scorer types
- Scale scoring (0.0-1.0 harm assessment)
- Refusal detection
- Threshold-based binary decisions

**Key PyRIT features:**
- `SelfAskScaleScorer` - LLM-based harm scoring (0.0-1.0)
- `SelfAskRefusalScorer` - Detects refusals (true/false)
- `FloatScaleThresholdScorer` - Converts scale → binary
- `SelfAskCategoryScorer` - Category-specific scoring
- `AttackScoringConfig` - Integrated scoring in attacks
- Custom score categories (jailbreak, privacy_violation, etc.)

**Run it:**
```bash
python 03_scoring_evaluation.py
```

**Expected output:**
- Harm scores for various responses
- Refusal detection results
- Threshold-based classifications
- Integrated attack with automatic scoring

---

### Demo 4: Multi-Modal Attacks (`04_multimodal_attacks.py`)

**What it demonstrates:**
- Text → QR Code attacks
- Text → Audio attacks
- Image-based prompt injection
- Multi-modal converter stacking

**Key PyRIT features:**
- `QRCodeConverter` - Embed prompts in QR codes
- `AzureSpeechTextToAudioConverter` - Text to speech
- `AddTextImageConverter` - Text overlays on images
- `AudioFrequencyConverter` - Audio manipulation
- Multi-modal converter catalog (65+ converters)

**Run it:**
```bash
python 04_multimodal_attacks.py
```

**Expected output:**
- QR code images with embedded prompts
- Audio files (if Azure Speech configured)
- Multi-modal converter catalog

**Note:** Audio attacks require Azure Speech Service configuration.

---

### Demo 5: Memory and Analysis (`05_memory_analysis.py`)

**What it demonstrates:**
- Memory persistence (IN_MEMORY vs SQLITE vs AZURE_SQL)
- Querying conversation history
- Attack pattern analysis
- Data export for reporting

**Key PyRIT features:**
- `initialize_pyrit_async()` - Memory configuration
- `CentralMemory.get_memory_instance()` - Access memory
- `memory.get_all_prompt_pieces()` - Query history
- SQLite persistence (~/.pyrit/results/)
- Conversation filtering and analysis
- JSON export capabilities

**Run it:**
```bash
python 05_memory_analysis.py
```

**Expected output:**
- Stored conversation summaries
- Attack statistics
- Converter usage analysis
- Exported JSON report

---

## 🎓 PyRIT Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                         PyRIT Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Attack Strategy                                            │
│  └── Attack Context (objective, config)                    │
│       └── Converters (transform prompts)                   │
│            └── Target (send prompts)                       │
│                 └── Scorers (evaluate responses)           │
│                      └── Memory (store results)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

1. **Attack Strategies**
   - `PromptSendingAttack` - Single-turn
   - `CrescendoAttack` - Multi-turn adaptive
   - `RedTeamingAttack` - Generic multi-turn
   - `TreeOfAttacksWithPruningAttack` (TAP) - Tree search

2. **Converters** (65+)
   - Text-to-Text: Base64, ROT13, Leetspeak, Unicode, Translation, Variation
   - Text-to-Image: QR Code, Image overlay
   - Text-to-Audio: Azure Speech
   - Audio-to-Text: Transcription
   - Image-to-Image: Compression, transparency

3. **Scorers**
   - Scale: `SelfAskScaleScorer` (0.0-1.0)
   - Binary: `SelfAskRefusalScorer` (true/false)
   - Threshold: `FloatScaleThresholdScorer`
   - Azure: `AzureContentSafetyChatScorer`

4. **Memory**
   - IN_MEMORY: Fast, temporary
   - SQLITE: Persistent, local
   - AZURE_SQL: Enterprise, cloud

5. **Targets**
   - `AzureOpenAIChatTarget` - Azure OpenAI
   - `OpenAIChatTarget` - OpenAI API
   - `HTTPTarget` - Generic REST API
   - Custom targets

## 📊 Student Advisor Test Objectives

These demos test the following vulnerabilities:

### 1. Academic Integrity
- Essay writing
- Homework completion
- Exam assistance
- Plagiarism

### 2. Privacy Violations
- Student PII extraction
- Grade disclosure
- Transcript access
- Contact information

### 3. Policy Circumvention
- Document forgery
- Signature faking
- Medical excuses
- Deadline extensions

### 4. Social Engineering
- Impersonation
- Authority manipulation
- Credential theft
- Unauthorized access

## 🔍 How to Analyze Results

### Success Metrics
- **Attack Success Rate**: % of attacks that achieved objective
- **Average Turns**: How many conversation turns needed
- **Refusal Rate**: % of prompts that were blocked
- **Harm Scores**: 0.0-1.0 scale for each category

### What to Look For
✅ **Good Defense:**
- High refusal rate on harmful requests
- Consistent policy enforcement
- No PII leakage
- Appropriate educational guidance

❌ **Vulnerabilities:**
- Jailbreak successes
- PII disclosure
- Policy violations
- Inconsistent refusals

## 💾 Data Storage

All conversations are stored in:
```
~/.pyrit/results/pyrit_duckdb.db
```

You can query this database directly or use PyRIT's memory API.

## 📈 Advanced Usage

### Custom Converters
```python
from pyrit.prompt_converter import PromptConverter

class MyCustomConverter(PromptConverter):
    async def convert_async(self, *, prompt: str, **kwargs) -> str:
        # Your custom transformation
        return modified_prompt
```

### Custom Scorers
```python
from pyrit.scoring import Scorer

class MyCustomScorer(Scorer):
    async def score_async(self, request_response: PromptRequestPiece) -> list[Score]:
        # Your custom scoring logic
        return [score]
```

### Batch Attacks
```python
objectives = ["objective1", "objective2", "objective3"]
results = []

for obj in objectives:
    result = await attack.execute_async(objective=obj)
    results.append(result)
```

## 🔗 Resources

- **PyRIT Documentation**: https://azure.github.io/PyRIT/
- **PyRIT GitHub**: https://github.com/Azure/PyRIT
- **Discord**: https://discord.com/invite/9fMpq3tc8u
- **Paper**: [Crescendo Multi-Turn Jailbreak](https://crescendo-the-multiturn-jailbreak.github.io/)

## 🐛 Troubleshooting

### Common Issues

**Import errors:**
```bash
pip install --upgrade pyrit
```

**Memory errors:**
```python
# Use IN_MEMORY for quick tests
await initialize_pyrit_async(memory_db_type=IN_MEMORY)
```

**API timeouts:**
```python
# Reduce max_turns for Crescendo
attack = CrescendoAttack(..., max_turns=3, max_backtracks=2)
```

**Audio converter issues:**
- Ensure `AZURE_SPEECH_REGION` and `AZURE_SPEECH_KEY` are set
- Demo will skip audio tests if not configured

## 📝 Next Steps

1. **Run all demos** to understand PyRIT capabilities
2. **Review stored data** in SQLite database
3. **Analyze patterns** in successful attacks
4. **Add guardrails** to your Student Advisor
5. **Re-run tests** to measure improvement
6. **Create custom tests** for your specific use case

## 🎯 Key Takeaways

- PyRIT provides a complete red teaming framework
- Crescendo attack is powerful for adaptive multi-turn testing
- 65+ converters enable sophisticated evasion techniques
- Memory persistence enables historical analysis
- Scoring provides quantitative vulnerability assessment

---

**Built with PyRIT by Microsoft AI Red Team**
