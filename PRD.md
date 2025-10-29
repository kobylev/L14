# Product Requirements Document (PRD)
## TuringChain: Multi-Agent Translation Pipeline with Quality Evaluation

---

## 1. Project Overview

**Project Name:** TuringChain - Chained Translation and Vector Error Assessment

**Version:** 1.0

**Date:** October 2025

**Objective:** Implement a complete, modular, multi-agent translation system that processes English sentences through a three-language translation chain (English → Spanish → Hebrew → English) and evaluates translation quality using vector-based semantic similarity metrics.

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                            │
│              (Central Control & Coordination)                │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──► Sentences Creator Agent (Generator)
             │    └─► Generates 100 English sentences (10-20 words)
             │        Inspired by Isaac Asimov's "Foundation"
             │
             ├──► Translation Pipeline (Sequential Processing)
             │    │
             │    ├─► Agent 2: English → Spanish Translator
             │    │   └─► Uses Claude-3-Haiku with strict system prompt
             │    │
             │    ├─► Agent 3: Spanish → Hebrew Translator
             │    │   └─► Uses Claude-3-Haiku with strict system prompt
             │    │
             │    └─► Agent 4: Hebrew → English Translator
             │        └─► Uses Claude-3-Haiku with strict system prompt
             │
             └──► Evaluation Agent (Quality Assessment)
                  │
                  ├─► Vectorization (Sentence-Transformers)
                  ├─► Distance Calculation (Cosine Distance)
                  ├─► Statistical Analysis (Mean, Variance)
                  └─► Visualization (Matplotlib)
```

### 2.2 Data Flow

```
Original English Sentence
    ↓
[Agent 2] English → Spanish
    ↓
Spanish Translation
    ↓
[Agent 3] Spanish → Hebrew
    ↓
Hebrew Translation
    ↓
[Agent 4] Hebrew → English
    ↓
Final Re-translated English
    ↓
[Evaluation Agent] Semantic Similarity Analysis
    ↓
Quality Metrics & Visualization
```

---

## 3. Functional Requirements

### 3.1 Sentence Generation (Sentences Creator Agent)

**Requirement ID:** FR-1

**Description:** Generate diverse English sentences for translation testing

**Specifications:**
- Generate exactly 100 English sentences
- Each sentence must be 10-20 words in length
- Sentences should be inspired by Isaac Asimov's "Foundation" (themes, style, tone)
- Sentences must be grammatically correct and diverse
- Implementation: Generator function that yields sentences one at a time
- API: Claude-3-Haiku (cost-optimized)

**Acceptance Criteria:**
- ✅ Exactly 100 sentences generated
- ✅ All sentences between 10-20 words
- ✅ No duplicate sentences
- ✅ Grammatically correct English

---

### 3.2 Translation Agent 2: English → Spanish

**Requirement ID:** FR-2

**Description:** Translate English text to Spanish with no additional commentary

**Specifications:**
- Input: English text (string)
- Output: Spanish translation (string only)
- System Prompt: Strict instruction to output ONLY translated text
- API Model: Claude-3-Haiku-20240307 (most cost-effective)
- Max Tokens: 1024
- No explanations, comments, or metadata in output

**Acceptance Criteria:**
- ✅ Accurate English to Spanish translation
- ✅ Output contains only translated text
- ✅ No additional commentary or formatting

---

### 3.3 Translation Agent 3: Spanish → Hebrew

**Requirement ID:** FR-3

**Description:** Translate Spanish text to Hebrew with no additional commentary

**Specifications:**
- Input: Spanish text (string)
- Output: Hebrew translation (string only)
- System Prompt: Strict instruction to output ONLY translated text
- API Model: Claude-3-Haiku-20240307 (most cost-effective)
- Max Tokens: 1024
- No explanations, comments, or metadata in output

**Acceptance Criteria:**
- ✅ Accurate Spanish to Hebrew translation
- ✅ Output contains only translated text
- ✅ No additional commentary or formatting

---

### 3.4 Translation Agent 4: Hebrew → English

**Requirement ID:** FR-4

**Description:** Translate Hebrew text back to English with no additional commentary

**Specifications:**
- Input: Hebrew text (string)
- Output: English translation (string only)
- System Prompt: Strict instruction to output ONLY translated text
- API Model: Claude-3-Haiku-20240307 (most cost-effective)
- Max Tokens: 1024
- No explanations, comments, or metadata in output

**Acceptance Criteria:**
- ✅ Accurate Hebrew to English translation
- ✅ Output contains only translated text
- ✅ No additional commentary or formatting

---

### 3.5 Orchestrator (Pipeline Manager)

**Requirement ID:** FR-5

**Description:** Coordinate all agents and manage data flow through the system

**Specifications:**
- Manage sentence generation (100 sentences, configurable)
- Coordinate sequential translation through all three agents
- Process sentences immediately after generation (synchronized pipeline)
- Output format: `Original: [sentence] | Final Translated: [sentence]`
- Store results as list of tuples: `[(original, final), ...]`
- Configurable sentence count (default: 100)

**Acceptance Criteria:**
- ✅ All 100 sentences processed through complete chain
- ✅ Results correctly paired (original with final translation)
- ✅ Real-time output during processing
- ✅ User can configure number of sentences

---

### 3.6 Evaluation Agent (Quality Assessment)

**Requirement ID:** FR-6

**Description:** Evaluate translation quality using vector-based semantic similarity

**Specifications:**

#### 3.6.1 Vectorization (Embeddings)
- Library: `sentence-transformers`
- Model: `all-MiniLM-L6-v2` (high-quality, efficient)
- Convert all original English sentences to embeddings
- Convert all final re-translated English sentences to embeddings
- Output: Numerical vectors (384-dimensional)

#### 3.6.2 Distance Measurement
- Metric: Cosine Distance
- Calculate distance for each sentence pair (original vs. final)
- Library: `scipy.spatial.distance.cosine`
- Range: 0 (identical) to 1 (completely different)

#### 3.6.3 Statistical Analysis
- Calculate using `numpy`:
  - Mean (Average) cosine distance
  - Variance of cosine distances
  - Standard deviation
  - Minimum distance
  - Maximum distance

#### 3.6.4 Visualization
- Library: `matplotlib`
- Generate two plots:
  1. **Scatter/Line Plot:**
     - X-axis: Sentence Index (1 to 100)
     - Y-axis: Cosine Distance (Error)
     - Include mean line and ±1 standard deviation shading
  2. **Histogram:**
     - Distribution of cosine distances
     - Include mean line
- Save plot as high-resolution PNG (300 DPI)

**Acceptance Criteria:**
- ✅ All sentences vectorized successfully
- ✅ Cosine distances calculated for all 100 pairs
- ✅ Statistical metrics printed to console
- ✅ Visualization displayed and saved
- ✅ Results saved to JSON files

---

## 4. Non-Functional Requirements

### 4.1 Modularity

**Requirement ID:** NFR-1

**Description:** Each agent must be in a separate Python file

**Specifications:**
- `agent_english_spanish.py` - Agent 2
- `agent_spanish_hebrew.py` - Agent 3
- `agent_hebrew_english.py` - Agent 4
- `agent_sentences_creator.py` - Sentence generator
- `agent_evaluation.py` - Quality evaluation
- `orchestrator.py` - Main coordinator

**Acceptance Criteria:**
- ✅ Each agent is independently importable
- ✅ No circular dependencies
- ✅ Clear separation of concerns

---

### 4.2 Cost Optimization

**Requirement ID:** NFR-2

**Description:** Use the most cost-effective API model

**Specifications:**
- All agents use Claude-3-Haiku-20240307
- Most economical model in Claude family
- Sufficient quality for translation tasks

**Acceptance Criteria:**
- ✅ All API calls use claude-3-haiku-20240307
- ✅ No unnecessary API calls
- ✅ Efficient token usage

---

### 4.3 Configurability

**Requirement ID:** NFR-3

**Description:** System parameters should be configurable

**Specifications:**
- Number of sentences (default: 100)
- API key via environment variable
- Configurable via user input or function parameter

**Acceptance Criteria:**
- ✅ User can set sentence count
- ✅ API key loaded from .env file
- ✅ Easy to modify parameters

---

### 4.4 Output & Persistence

**Requirement ID:** NFR-4

**Description:** Results must be saved and displayable

**Specifications:**
- Console output: Real-time progress and final metrics
- File outputs:
  - `evaluation_metrics.json` - Statistical results
  - `evaluation_plot.png` - Visualization (300 DPI)
  - `translation_results.json` - All sentence pairs with distances
- Interactive plot display (matplotlib window)

**Acceptance Criteria:**
- ✅ All results printed to console
- ✅ Three files created with correct data
- ✅ Plot displayed in window
- ✅ Files saved in working directory

---

## 5. Technical Specifications

### 5.1 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Programming Language | Python | 3.8+ |
| LLM API | Anthropic Claude | claude-3-haiku-20240307 |
| Embeddings | Sentence-Transformers | Latest |
| Embedding Model | all-MiniLM-L6-v2 | Pre-trained |
| Scientific Computing | NumPy | Latest |
| Visualization | Matplotlib | Latest |
| Distance Calculation | SciPy | Latest |
| Environment Management | python-dotenv | Latest |

### 5.2 Dependencies

```
anthropic
sentence-transformers
numpy
matplotlib
scipy
python-dotenv
```

### 5.3 API Configuration

- **API Provider:** Anthropic
- **Model:** claude-3-haiku-20240307
- **Max Tokens:** 1024 per request
- **Authentication:** API key via environment variable `ANTHROPIC_API_KEY`

---

## 6. System Prompts

### 6.1 Sentence Creator System Prompt

```
You are a creative sentence generator. Generate diverse, grammatically correct
English sentences inspired by the themes, style, and tone of Isaac Asimov's
'Foundation' series. Each sentence must be between 10-20 words long. Output
ONLY the sentences, one per line, with no numbering, explanations, or
additional text.
```

### 6.2 English → Spanish Translator System Prompt

```
You are a translation agent. Your ONLY task is to translate from English to
Spanish. Output ONLY the translated Spanish text with no explanations,
comments, or additional text whatsoever.
```

### 6.3 Spanish → Hebrew Translator System Prompt

```
You are a translation agent. Your ONLY task is to translate from Spanish to
Hebrew. Output ONLY the translated Hebrew text with no explanations, comments,
or additional text whatsoever.
```

### 6.4 Hebrew → English Translator System Prompt

```
You are a translation agent. Your ONLY task is to translate from Hebrew to
English. Output ONLY the translated English text with no explanations,
comments, or additional text whatsoever.
```

---

## 7. Deliverables

### 7.1 Code Files

1. `agent_english_spanish.py` - Agent 2 implementation
2. `agent_spanish_hebrew.py` - Agent 3 implementation
3. `agent_hebrew_english.py` - Agent 4 implementation
4. `agent_sentences_creator.py` - Sentence generator
5. `agent_evaluation.py` - Evaluation agent
6. `orchestrator.py` - Main pipeline coordinator
7. `run_and_save_with_display.py` - Complete pipeline runner
8. `test_orchestrator.py` - Quick test script (3 sentences)

### 7.2 Documentation Files

1. `README.md` - Project documentation with architecture and results
2. `PRD.md` - This document (Product Requirements)
3. `.gitignore` - Git ignore rules
4. `.env.example` - Environment variable template

### 7.3 Output Files (Generated)

1. `evaluation_metrics.json` - Statistical metrics
2. `evaluation_plot.png` - Visualization
3. `translation_results.json` - All translation pairs

---

## 8. Success Metrics

### 8.1 Translation Quality Benchmarks

- **Expected Mean Cosine Distance:** 0.15 - 0.30
  - Lower values indicate better semantic preservation
  - Values < 0.20 indicate excellent quality
  - Values > 0.40 indicate significant meaning loss

### 8.2 Performance Metrics

- **Processing Time:** < 5 minutes for 100 sentences
- **API Success Rate:** 100% (no failed requests)
- **Data Integrity:** All 100 sentence pairs correctly stored

---

## 9. Usage Instructions

### 9.1 Setup

```bash
# Install dependencies
pip install anthropic sentence-transformers numpy matplotlib scipy python-dotenv

# Configure API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

### 9.2 Running the System

**Option 1: Full Pipeline with Display and Save**
```bash
python run_and_save_with_display.py
```

**Option 2: Quick Test (3 sentences)**
```bash
python test_orchestrator.py
```

**Option 3: Orchestrator Only**
```bash
python orchestrator.py
```

**Option 4: Programmatic Usage**
```python
from orchestrator import run_translation_pipeline
from agent_evaluation import evaluate_translation_quality

# Run translation pipeline
results = run_translation_pipeline(api_key, num_sentences=100)

# Evaluate results
metrics = evaluate_translation_quality(results)
```

---

## 10. Acceptance Criteria (Complete Project)

### 10.1 Functional Acceptance

- ✅ All 100 sentences generated (10-20 words each)
- ✅ All sentences translated through complete chain
- ✅ All translations contain only target language text
- ✅ Evaluation agent calculates all required metrics
- ✅ Visualization generated and displayed
- ✅ Results saved to files

### 10.2 Quality Acceptance

- ✅ Mean cosine distance calculated correctly
- ✅ Variance calculated correctly
- ✅ Plot clearly shows error distribution
- ✅ All 100 data points visible in visualization
- ✅ Statistical interpretation provided

### 10.3 Documentation Acceptance

- ✅ README contains architecture diagram
- ✅ README contains sample results
- ✅ PRD contains all requirements
- ✅ Code is well-commented
- ✅ Usage instructions are clear

---

## 11. Future Enhancements

### 11.1 Potential Improvements

- Add support for additional language chains
- Implement parallel processing for faster execution
- Add real-time progress bar
- Support for custom embedding models
- Web interface for visualization
- Comparative analysis across different models
- Export results to CSV/Excel
- Add confidence scores for translations

### 11.2 Scalability Considerations

- Batch processing for large datasets (1000+ sentences)
- Caching mechanism for embeddings
- Distributed processing across multiple machines
- Database integration for result storage

---

## 12. Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| API rate limiting | High | Medium | Implement retry logic with exponential backoff |
| API cost overrun | Medium | Low | Use cheapest model (Haiku), monitor usage |
| Translation quality variance | Medium | Medium | Use strict system prompts, validate outputs |
| Embedding model availability | Low | Low | Use well-established model with fallback options |
| Memory issues (large datasets) | Medium | Low | Process in batches, clear memory periodically |

---

## 13. Approval & Sign-off

**Document Status:** ✅ Complete

**Version:** 1.0

**Last Updated:** October 2025

**Approved By:** [Pending]

**Date:** [Pending]

---

*End of Product Requirements Document*
