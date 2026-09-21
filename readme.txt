# 🔍 WikiFact Check

An automated Wikipedia fact-auditing tool developed for the **Open Source Day Hands-On Project Challenge** using the **Wikimedia Structured Wikipedia Dataset**.

WikiFact Check cross-references structured information in an article's infobox against the narrative lead prose (abstract) to identify and flag potential discrepancies for human verification.

---

## 📌 Project Overview

* **Assigned Track:** Challenge 4 – WikiFact Check
* **Difficulty Level:** Advanced
* **Target Users:** Wikipedia editors, fact-checkers, and data quality contributors
* **Mandatory Rule:** The tool strictly follows the competition requirement:
  > It states **`"Possible mismatch detected."`** and **never** states `"This fact is false."` Discrepancies do not necessarily indicate an incorrect fact; they require manual human review.

---

## 🚀 Key Features

### Core Requirements
* **Article Selection & Search:** Select a structured article or query records directly from the dataset[cite: 1].
* **Universal Fact Extraction:** Recursively extracts key-value attributes (dates, locations, organizations, titles) from nested infobox tables, lists, and wikitext[cite: 1].
* **Text Prose Search:** Scans the article's lead section (`abstract`) for corroborating mentions[cite: 1].
* **Side-by-Side Dual Display:** Presents the infobox value alongside the corresponding prose value for human review[cite: 1].
* **Discrepancy Flagging:** Flags discrepancies under the official status: `"Possible mismatch detected"`[cite: 1].

### Implemented Optional Features
* **NLP & Named Entity Recognition (NER):** Extracts dates, proper nouns, and numerical tokens from lead text[cite: 1].
* **Date Normalization:** Unifies diverse date formats (e.g., `"15 May 1980"` vs. `"May 15, 1980"`) into standardized numerical tokens to prevent false mismatch flags[cite: 1].
* **Similarity Matching & Confidence Scoring:** Evaluates fuzzy token overlap and string similarity on a `0.00` to `1.00` confidence scale[cite: 1].
* **Highlighted Text:** Wraps matched or conflicting prose tokens inside `[HIGHLIGHT: ...]` tags for visual inspection[cite: 1].
* **Comparison Report Export:** Exports complete audit results to `audit_report.json`[cite: 1].
* **Talk Page Markup:** Generates formatted Wikipedia Talk Page templates (`{{WikiFactCheck-Note}}`) for flagged items.

---

## 🛠️ Architecture & Pipeline Flow

The project follows the standard challenge flow[cite: 1]:

```text
User Search / Select Article
             ↓
Retrieve Article from Wikimedia Dataset (Parquet)
             ↓
Extract Structured Infobox Facts
             ↓
Search Article Lead Prose (Abstract)
             ↓
Apply NLP / Date Normalization / Similarity Match
             ↓
Flag Discrepancies ("Possible mismatch detected")
             ↓
Display Dual Values & Export JSON Report
📦 Dataset Integration
Dataset Source: Wikimedia Structured Wikipedia Dataset (enwiki_namespace_0_*.parquet)[cite: 1]

Integration Platform: Kaggle Notebooks / GitHub

Key Fields Utilized:

name: Article title[cite: 1]

abstract: Lead narrative text[cite: 1]

infoboxes: Structured key-value properties[cite: 1]

💻 Tech Stack
Language: Python 3

Data Processing: pyarrow, pandas, json

Text Processing & NLP: re, difflib, datetime

Environment: Kaggle Notebooks / Google Colab

📋 Sample Output
Plaintext
===========================================================================
🔍 WIKIFACT CHECK AUDIT REPORT
Target Article: Indian Space Research Organisation
===========================================================================

[LEAD ABSTRACT PROSE]
> The Indian Space Research Organisation is the national space agency of India...

---------------------------------------------------------------------------
Structured Facts Audited : 6
Matches Confirmed        : 5
Flagged for Review       : 1
---------------------------------------------------------------------------

--- SIDE-BY-SIDE AUDIT COMPARISON ---

1. [Headquarters]
   • Infobox Value    : Bengaluru, Karnataka
   • Prose Text       : [HIGHLIGHT: Bengaluru]
   • Result Status    : 🟢 Match (Confidence: 0.85)
   • Explanation      : Core entity/date tokens for 'Headquarters' verified in lead prose.

2. [Established]
   • Infobox Value    : 15 August 1969
   • Prose Text       : Conflicting prose context: '[HIGHLIGHT: 1969]'
   • Result Status    : ⚠️ Possible mismatch detected (Confidence: 0.40)
   • Explanation      : Potential discrepancy between infobox value and prose context.
   • Talk Page Action : {{WikiFactCheck-Note | field = Established | infobox = 15 August 1969 | status = Possible mismatch detected | note = Flagged for editor review.}}
⚙️ How to Run
Open your Kaggle Notebook with the Wikimedia Structured Contents dataset attached[cite: 1].

Clone or paste the script into the notebook.

Run the notebook cells (Shift + Enter).

Enter an article title to search or press Enter to evaluate a random structured article.

Review the audit results and download the generated audit_report.json report[cite: 1].

👥 Submission Information
Assigned Track: Challenge 4 – WikiFact Check[cite: 1]

Submission Format: Publicly accessible GitHub repository / Kaggle Notebook

Platform Form: Open Source Day - WCT Contribution Form
