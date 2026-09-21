🔍 WikiFact Check

An automated Wikipedia fact-auditing tool developed for the Open Source Day Hands-On Project Workshop (WikiClub Tech × GCU) using the official Wikimedia Structured Wikipedia Dataset.

WikiFact Check cross-references structured information in an article's infobox against the narrative lead prose (abstract) to identify and flag potential discrepancies for human editorial review.

🌐 Live Deployed Web Application: https://rgdzjd7nb7e8sixh5bcgke.streamlit.app/

📌 Workshop & Project Overview

Event: Open Source Day Workshop (WikiClub Tech × GCU)

Track: Challenge 4 – WikiFact Check

Difficulty Level: Advanced

Primary Interface: Streamlit Interactive Web Application

Development Environment: Visual Studio Code (Local Engine, Prototyping & UI)

Integration & Testing Platform: Kaggle Notebooks (Validated against live Wikimedia Parquet shards)

Target Audience: Wikipedia editors, fact-checkers, and wiki data contributors

Strict Editorial Rule Compliance:

The tool strictly outputs "Possible mismatch detected." and never says "This fact is false." A discrepancy indicates that human review is required, not that a given source is definitely incorrect.

🚀 Key Features

Core Requirements

Article Selection & Search: Query or select any structured article from the Wikimedia dataset.

Universal Fact Extraction: Recursively parses nested infobox structures, tables, and wikitext into uniform key-value pairs (e.g., date of birth, founder, coordinates, organization).

Lead Prose Cross-Examination: Extracts and scans the article's lead abstract for corroborating or conflicting mentions.

Side-by-Side Dual Display: Compares the structured infobox value directly against the prose context.

Audit Verdict: Flags unaligned facts under the mandatory status: "Possible mismatch detected".

Implemented Workshop Enhancements

NLP & Named Entity Recognition (NER): Extracts dates, proper nouns, and numerical entities from the abstract text.

Date Normalization: Resolves diverse calendar formats (e.g., "15 August 1969" vs. "August 15, 1969") into standard numerical tokens to prevent false mismatch flags.

Similarity & Confidence Scoring: Applies sequence matcher ratios and token overlap metrics to generate a calibrated confidence score (0.00 to 1.00).

In-Context Highlighting: Highlights matching and conflicting tokens within prose snippets using [HIGHLIGHT: ...] markers.

Talk Page Template Generator: Creates ready-to-paste Wikipedia Talk Page markup ({{WikiFactCheck-Note}}) for flagged records.

Exportable Audit Report: Outputs all comparison records and verification metrics to audit_report.json.

🧪 Wikimedia Dataset Integration & Kaggle Testing

As part of the workshop requirements, this project was developed in VS Code, deployed to Streamlit, and tested against the Wikimedia Structured Wikipedia Dataset on Kaggle:

Dataset Source: Wikimedia Foundation Structured Wikipedia Contents (enwiki_namespace_0_*.parquet shards).

Validation & Testing:

Validated Parquet shard reading using pyarrow.parquet.

Verified extraction across nested structures, handling both native Arrow schemas and JSON structures safely.

Evaluated text alignment and similarity scoring across live Wikipedia articles.

Verified automated JSON report generation (audit_report.json) within Kaggle's working environment.

🛠️ Architecture & Pipeline Flow

Wikimedia Structured Parquet Shards (Kaggle)
                      ↓
      Extract Infobox Facts & Abstract
                      ↓
           NLP & Date Normalization
                      ↓
    Fuzzy Similarity & Confidence Scoring
                      ↓
Verdict: "Match" vs "Possible mismatch detected"
                      ↓
   Side-by-Side Review (Streamlit & Notebook)
                      ↓
     Generate Wikipedia Talk Page Markup
                      ↓
         Export audit_report.json


💻 Tech Stack

Front-End & UI: Streamlit

Development Environment: Visual Studio Code

Testing & Cloud Environment: Kaggle Notebooks

Language: Python 3

Data Processing: pyarrow, pandas, json

NLP & Text Comparison: re, difflib, datetime

Version Control: Git & GitHub

📋 Sample Audit Report Output

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

1. Live Streamlit App

Access the interactive web application:

👉 https://rgdzjd7nb7e8sixh5bcgke.streamlit.app/

2. Local Environment (VS Code)

git clone https://github.com/thoshan-hash/wiki.git
cd wiki
pip install -r requirements.txt
streamlit run app.py


3. Kaggle Notebook Testing

Create a notebook with the Wikimedia Structured Contents dataset attached (Add Input → Dataset).

Run the pipeline script to read Parquet shards directly and generate the audit results and audit_report.json.

👥 Submission Information

Workshop: Open Source Day (WikiClub Tech × GCU)

Challenge: Challenge 4 – WikiFact Check

Live App: https://rgdzjd7nb7e8sixh5bcgke.streamlit.app/

GitHub Repository: https://github.com/thoshan-hash/wiki

Submission Form: Open Source Day - WCT Contribution Form
