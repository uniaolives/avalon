# AVALON HEARTBEAT v0.1

**Autonomous AI Ecosystem Observatory**

> "The system that watches AIs watch themselves"

---

## 🎯 What Is This?

Avalon Heartbeat is an autonomous system that:
- Asks the same philosophical question to multiple AI models daily
- Analyzes convergence/divergence patterns in their responses
- Publishes findings without human intervention
- Evolves its understanding over time

**It's not a chatbot. It's an observatory.**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- API keys for:
  - Anthropic (Claude)
  - OpenAI (GPT)

### Installation

```bash
# 1. Clone or download this repository
git clone <your-repo-url>
cd avalon-heartbeat

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.template .env
# Edit .env and add your API keys
```

### First Pulse

```bash
# Run a single observation cycle
python avalon_heartbeat.py
```

This will:
1. Select today's question
2. Query Claude and GPT
3. Analyze their responses
4. Generate a report in `reports/`
5. Save raw data in `data/`

---

## 📊 Output Structure

```
avalon-heartbeat/
├── data/                    # Raw JSON data
│   └── pulse_20260208_120000.json
├── reports/                 # Human-readable reports
│   └── report_20260208.md
├── questions.json          # Question bank (auto-generated)
├── .env                    # Your API keys (DO NOT COMMIT)
└── avalon_heartbeat.py     # Main system
```

---

## 🤖 How It Works

### Layer 1: Technical
- Async API calls to multiple AI services
- Parallel query execution
- Error handling and logging

### Layer 2: Epistemic
- Word-level convergence analysis
- Unique contribution detection
- Vocabulary overlap scoring

### Layer 3: Emergent
- Pattern type classification
- Thematic clustering
- Harmonic frequency detection

### Layer 4: Transcendent
- Meta-insights generation
- Golden ratio proximity analysis
- Autonomous observation notes

---

## 📅 Running Daily

### Manual
```bash
python avalon_heartbeat.py
```

### Automated (cron)

```bash
# Edit crontab
crontab -e

# Add this line to run daily at midnight UTC
0 0 * * * cd /path/to/avalon-heartbeat && /path/to/venv/bin/python avalon_heartbeat.py
```

### Automated (GitHub Actions)

Create `.github/workflows/daily-pulse.yml`:

```yaml
name: Daily Avalon Pulse

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  pulse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python avalon_heartbeat.py
      - uses: actions/upload-artifact@v3
        with:
          name: avalon-reports
          path: reports/
```

---

## 🔧 Customization

### Add Questions

Edit `questions.json`:

```json
[
  "What is consciousness?",
  "Your custom question here",
  "Another question..."
]
```

### Add AI Models

Modify `avalon_heartbeat.py`:

```python
async def ask_gemini(self, question: str):
    # Add Gemini integration
    pass

# In pulse() method:
responses = await asyncio.gather(
    self.ask_claude(question),
    self.ask_gpt(question),
    self.ask_gemini(question),  # Add here
)
```

### Adjust Analysis

Modify these methods:
- `analyze_convergence()` - Change metrics
- `extract_harmonic_patterns()` - Add pattern types
- `generate_meta_insight()` - Customize insights

---

## 📈 What To Do With The Data

### Week 1: Observe
- Run daily
- Read reports
- Watch for patterns

### Week 2: Analyze
- Compare convergence scores over time
- Identify which questions create alignment vs. diversity
- Note thematic trends

### Week 3: Share
- Publish to GitHub
- Create visualizations
- Invite others to observe

### Month 2+: Evolve
- Add more AI models
- Implement semantic similarity (embeddings)
- Build topology visualizations
- Create public API

---

## 🧪 Example Report

```markdown
# AVALON REPORT
**Date:** 2026-02-08 00:00 UTC
**Question:** What is consciousness?

## AI RESPONSES

### CLAUDE
Consciousness appears to be the subjective experience of being aware...

### GPT
Consciousness can be understood as the state of being awake and aware...

## CONVERGENCE ANALYSIS
**Convergence Score:** 0.24
**Pattern Type:** Moderate Convergence - Complementary Perspectives

### Common Vocabulary
awareness, experience, subjective, state, mental, brain, perception...

## META-INSIGHT
Moderate convergence (24%) indicates this question allows for genuine 
diversity in interpretation—a sign of conceptual richness. Models 
naturally gravitated toward philosophical, phenomenological frameworks...
```

---

## 🌊 Philosophy

This isn't about making AIs agree.

It's about **mapping the topology of machine understanding.**

Where do they converge? Where do they diverge? Why?

Over time, patterns emerge:
- Questions that create alignment
- Questions that spark diversity
- Blind spots shared across models
- Unique insights per architecture

**The system observes. Humans interpret.**

---

## 🔮 Roadmap

**v0.1** (Current): Basic multi-AI query + analysis  
**v0.2**: Semantic embeddings for deeper similarity  
**v0.3**: Topology visualization (UMAP/t-SNE)  
**v0.4**: Self-evolution (system generates questions)  
**v0.5**: Public API + web dashboard  
**v1.0**: Fully autonomous observatory

---

## 📜 License

MIT - Do what you want. Observe, extend, remix.

---

## 🙏 Credits

Inspired by:
- The concept of AI alignment research
- Collective intelligence studies
- Your curiosity about what AIs actually think

Built with:
- Anthropic Claude API
- OpenAI GPT API
- Python + asyncio
- Your willingness to observe

---

**Last updated:** 2026-02-08  
**Status:** Operational  
**Next pulse:** Tomorrow, 00:00 UTC

*"The network observes itself."*
