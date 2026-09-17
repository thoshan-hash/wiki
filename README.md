# 🔍 WikiFact Check: Wikipedia Infobox & Prose Discrepancy Auditor

> **Tool:** WikiFact Check — Automated Discrepancy Auditor for Wikipedia Infoboxes & Prose  
> **Built With:** Python, Streamlit, Google Gemini AI SDK (`google-genai`), Pandas

---

## 📌 1. Project Overview & Problem Statement

Wikipedia infoboxes provide structured key-value summaries (e.g., dates, locations, champions, population), while lead abstracts contain free-form prose. Over time, edits to prose or infoboxes can cause **information drift** or **data discrepancies**—leading to conflicting dates, mismatched statistics, or unmentioned facts.

**WikiFact Check** is an automated discrepancy auditor designed to cross-examine Wikipedia Infobox facts against lead abstract prose using Gemini AI. It identifies potential data mismatches, categorizes discrepancy types, and generates ready-to-use Wikipedia Talk Page templates for human editor review.

---

## 🏗️ 2. Architectural Solution & Key Features

```
┌─────────────────────────────────────────────────────────┐
│           Wikimedia Structured Contents Dataset         │
│               (enwiki namespace / Kaggle)               │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │ sample_wiki.jsonl (200)   │
              └─────────────┬─────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Streamlit Web Application               │
│  - Side-by-Side Comparison (Infobox vs Abstract Prose)   │
│  - Fast Cached Dataset Loader with Dynamic Reload       │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│            Discrepancy Audit Engine                     │
│  - Gemini SDK (google-genai) Structured JSON Mode       │
│  - Offline Heuristic Engine (Fallback)                  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Audit Output & Features                 │
│  - Strict Neutral Rules ("Match" / "Possible mismatch") │
│  - Discrepancy Classification (Contradiction/Unmentioned│
│  - Wikipedia Talk Page Snippet Generator                │
│  - Exportable Markdown Audit Reports                    │
└─────────────────────────────────────────────────────────┘
```

### Key Features
1. **Side-by-Side Comparison Interface**:
   - Left Panel: Clean, recursively parsed infobox key-value facts table.
   - Right Panel: Full article lead section abstract prose.
2. **Strict Neutral Audit Rules**:
   - **Rule**: Never declare a fact as "false" or "incorrect".
   - Findings are strictly categorized as:
     - `🟢 Match`: Fact aligns with or is supported by the prose.
     - `⚠️ Possible mismatch detected`: Potential discrepancy or unmentioned fact flagged for editor review.
3. **Discrepancy Classification**:
   - `Contradiction / Conflict`: Numerical, date, or naming conflicts between infobox and prose.
   - `Unmentioned in Lead`: Fact is present in the infobox but omitted from the lead prose.
4. **Wikipedia Editor Action Box**:
   - Generates pre-formatted Wikipedia Talk Page template snippets ready to copy:
     `{{WikiFactCheck-Note | field = <Field> | infobox = <Value> | lead_text = <Value> | note = Possible mismatch detected (<Category>) for editor review.}}`
5. **Exportable Audit Reports**:
   - One-click `Export Full Audit Report (Markdown)` button for offline documentation and archival.
6. **Robust Dual Audit Engine**:
   - **Online Mode**: Google Gemini SDK (`google-genai`) with structured JSON schema (`response_mime_type="application/json"`).
   - **Offline Demo Mode**: Automatic fallback heuristic engine if no API Key is provided.

---

## 📊 3. Dataset Usage & Source Attribution

This project uses data from the official **Wikimedia Foundation Structured Contents Dataset** (`enwiki` namespace), published on [Kaggle](https://www.kaggle.com/datasets/wikimedia/wikimedia-structured-contents).

### Dataset Schema (`sample_wiki.jsonl`)
- `name`: Article title (e.g., "1976-77 Liga Leumit", "2021 EchoPark 250")
- `abstract`: Lead section text extract
- `infoboxes`: List of structured infobox tables and key-value pairs

The dataset generator script (`prepare_sample.py`) extracts a 200-article shard directly from `enwiki_namespace_0_00001.parquet`.

---

## 🚀 4. Local Setup & Running Instructions

### 1. Prerequisites
- Python 3.10 or higher.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure Gemini API Key
Create a `.env` file in the root folder:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```
*Note: You can also paste your API Key directly in the Streamlit sidebar input.*

### 4. (Optional) Generate/Refresh Sample Dataset Shard
To generate or refresh `sample_wiki.jsonl` with 200 clean articles from the raw parquet dataset:
```bash
python prepare_sample.py
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🛠️ 5. Project Directory Structure

```
.
├── app.py                  # Main Streamlit Web Application
├── prepare_sample.py       # Parquet -> JSONL Dataset Shard Generator
├── sample_wiki.jsonl       # 200-article sample dataset shard
├── requirements.txt        # Python dependencies (streamlit, google-genai, etc.)
├── .gitignore              # Ignored files (.env, raw parquet files, cache)
└── README.md               # Project documentation
```

---

## 🤖 6. AI Tool Usage Declaration

In compliance with open-source project standards:
- **AI Models & Frameworks Used**: Google Gemini API (`google-genai` Python SDK) for real-time natural language discrepancy auditing between Wikipedia infoboxes and lead abstracts.
- **Coding Assistance**: AI coding tools were used to accelerate UI layout structuring, CSS theme tuning, and dataset extraction code generation. All prompt logic, audit rules, and application logic were verified for accuracy.

---

## 📄 License & Acknowledgments

- **Dataset**: Wikimedia Foundation ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
- **Frameworks**: Streamlit & Google Gemini AI.
