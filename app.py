# pyrefly: ignore [missing-import]
import json
import os
import random
import re
# pyrefly: ignore [missing-import]
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="WikiFact Check | Discrepancy Auditor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Modern Slate-Blue Theme
st.markdown(
    """
<style>
    /* Main Background & Typography */
    .stApp {
        background-color: #161d2f;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Card */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.75rem 2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .main-header h1 {
        color: #38bdf8;
        font-weight: 700;
        margin-bottom: 0.35rem;
        font-size: 2.2rem;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Section Cards */
    .column-card {
        background-color: #212a42;
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid #384566;
        height: 100%;
    }

    /* Status Badges */
    .badge-match {
        background-color: rgba(34, 197, 94, 0.18);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.45);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-mismatch {
        background-color: rgba(245, 158, 11, 0.18);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.45);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-category {
        background-color: rgba(148, 163, 184, 0.15);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 8px;
    }

    /* Abstract Prose Container */
    .prose-box {
        background-color: #192136;
        padding: 1.35rem;
        border-radius: 8px;
        border-left: 4px solid #38bdf8;
        border-top: 1px solid #2d3854;
        border-right: 1px solid #2d3854;
        border-bottom: 1px solid #2d3854;
        font-size: 1.02rem;
        line-height: 1.7;
        color: #cbd5e1;
    }

    /* Metrics Cards */
    .metric-container {
        background: #212a42;
        border: 1px solid #384566;
        padding: 1.1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- DATA LOADING & PARSING ---

@st.cache_data
def load_wiki_data(filepath="sample_wiki.jsonl"):
    """Load JSONL Wikipedia dataset shard with st.cache_data."""
    articles = []
    if not os.path.exists(filepath):
        return articles

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    articles.append(json.loads(line))
                except Exception:
                    continue
    return articles


def extract_infobox_facts(infobox_data):
    """Recursively extract key-value facts from Wikipedia infobox structures."""
    facts = []

    def traverse(item, current_section=""):
        if isinstance(item, dict):
            item_type = item.get("type")
            name = item.get("name", "")
            val = item.get("value", "")
            values = item.get("values", [])

            display_val = (
                val
                if val
                else (
                    ", ".join(values)
                    if isinstance(values, list)
                    else str(values)
                )
            )

            if item_type == "field" and name and display_val:
                facts.append(
                    {"field": name.strip(), "value": display_val.strip()}
                )
            elif "has_parts" in item and isinstance(item["has_parts"], list):
                sec_name = name if item_type == "section" else current_section
                for part in item["has_parts"]:
                    traverse(part, sec_name)
            elif name and display_val and item_type not in ["infobox", "section"]:
                facts.append(
                    {"field": name.strip(), "value": display_val.strip()}
                )
        elif isinstance(item, list):
            for element in item:
                traverse(element, current_section)

    traverse(infobox_data)

    seen_fields = set()
    unique_facts = []
    for fact in facts:
        key = (fact["field"], fact["value"])
        if key not in seen_fields:
            seen_fields.add(key)
            unique_facts.append(fact)

    return unique_facts


# --- AUDIT HEURISTIC ENGINE ---

def run_auditor(abstract, facts):
    """Audits facts against lead prose using clean entity tokenization."""
    results = []
    abstract_lower = abstract.lower()
    sentences = re.split(r'(?<=[.!?])\s+', abstract)

    for fact in facts:
        field = fact["field"]
        val = fact["value"]
        val_lower = val.lower()

        # Clean tokens to match against abstract prose
        tokens = [
            t.strip()
            for t in re.split(r"[\s,\(\)\-\/]+", val_lower)
            if len(t.strip()) > 2 and not t.strip().isdigit()
        ]
        numbers = re.findall(r"\b\d+\b", val_lower)

        # Check full literal phrase match first
        if val_lower in abstract_lower:
            matched_sentence = next((s for s in sentences if val_lower in s.lower()), abstract[:120] + "...")
            status = "Match"
            category = "Match"
            text_snippet = matched_sentence.strip()
            explanation = f"The infobox value aligns directly with the lead text."
        else:
            token_matches = [t for t in tokens if t in abstract_lower]
            number_matches = [n for n in numbers if n in abstract_lower]

            if (tokens and len(token_matches) >= max(1, len(tokens) // 2)) or (numbers and len(number_matches) == len(numbers)):
                status = "Match"
                category = "Match"
                matched_snippet = token_matches[0] if token_matches else (number_matches[0] if number_matches else "")
                text_snippet = f"Relevant mention identified: '{matched_snippet}' in prose"
                explanation = f"Core values and entities for '{field}' are supported by the lead text."
            else:
                status = "Possible mismatch detected"
                if token_matches or number_matches:
                    category = "Contradiction / Conflict"
                    matched_snippet = token_matches[0] if token_matches else number_matches[0]
                    text_snippet = f"Partial reference found: '{matched_snippet}'"
                    explanation = f"The field '{field}' ({val}) has partial token overlap with the lead, but appears inconsistent or contradictory."
                else:
                    category = "Unmentioned in Lead"
                    text_snippet = "Not explicitly stated in lead prose"
                    explanation = f"The infobox field '{field}' ({val}) is omitted from the lead abstract text."

        results.append({
            "field": field,
            "infobox_value": val,
            "text_value": text_snippet,
            "status": status,
            "category": category,
            "explanation": explanation,
        })

    return results


def generate_markdown_report(article_name, abstract_text, audit_results):
    """Generate Markdown report for export download."""
    total = len(audit_results)
    matches = sum(1 for r in audit_results if r.get("status") == "Match")
    mismatches = total - matches
    match_rate = (matches / total * 100) if total > 0 else 0

    md = "# WikiFact Check Audit Report\n\n"
    md += f"**Article Title:** {article_name}  \n"
    md += f"**Auditor Engine:** WikiFact Check Discrepancy Engine  \n\n"
    md += "## Summary Metrics\n"
    md += f"- **Total Facts Audited:** {total}\n"
    md += f"- **Matches:** {matches}\n"
    md += f"- **Potential Mismatches:** {mismatches}\n"
    md += f"- **Match Rate:** {match_rate:.1f}%\n\n"
    md += f"## Article Lead Abstract\n> {abstract_text}\n\n"
    md += "## Detailed Fact Audit\n\n"

    for idx, r in enumerate(audit_results, 1):
        field = r.get("field", "Unknown")
        infobox_val = r.get("infobox_value", "")
        text_val = r.get("text_value", "")
        status = r.get("status", "Match")
        category = r.get("category", status)
        explanation = r.get("explanation", "")

        status_tag = "MATCH" if status == "Match" else f"POSSIBLE MISMATCH ({category})"
        md += f"### {idx}. {field}: `{infobox_val}`\n"
        md += f"- **Status:** {status_tag}\n"
        md += f"- **Lead Prose Context:** {text_val}\n"
        md += f"- **Explanation:** {explanation}\n"
        if status != "Match":
            snippet = (
                f"{{{{WikiFactCheck-Note | field = {field} | infobox = {infobox_val} "
                f"| lead_text = {text_val} | note = Possible mismatch detected ({category}) for editor review.}}}}"
            )
            md += f"- **Wikipedia Talk Page Snippet:**\n  ```wikitext\n  {snippet}\n  ```\n"
        md += "\n---\n\n"

    return md


# --- MAIN APPLICATION UI ---

def main():
    # Sidebar Setup
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/120px-Wikipedia-logo-v2.svg.png",
            width=55,
        )
        st.title("WikiFact Check")
        st.caption("Automated Discrepancy Auditor")
        st.markdown("---")

        st.subheader("Dataset & Cache")
        articles = load_wiki_data()
        st.metric("Loaded Articles", len(articles))
        st.caption("Source: Wikimedia Structured Contents Dataset")

        col_sb1, col_sb2 = st.columns([1, 1])
        with col_sb1:
            if st.button("Reload", width="stretch", help="Clear cache and reload dataset"):
                st.cache_data.clear()
                st.rerun()
        with col_sb2:
            if st.button("Random", width="stretch", help="Pick a random article"):
                if articles:
                    st.session_state["selected_index"] = random.randint(0, len(articles) - 1)
                    st.rerun()

    # Main Header
    st.markdown(
        """
    <div class="main-header">
        <h1>WikiFact Check</h1>
        <div class="subtitle">Automated Discrepancy Auditor for Wikipedia Infoboxes & Prose</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not articles:
        st.error("No dataset found. Please ensure `sample_wiki.jsonl` exists in the workspace.")
        st.info("Run `python prepare_sample.py` to generate the dataset shard.")
        return

    # Article Selection
    article_titles = [f"{i+1}. {a.get('name', 'Untitled')}" for i, a in enumerate(articles)]

    if "selected_index" not in st.session_state or st.session_state["selected_index"] >= len(articles):
        st.session_state["selected_index"] = 0

    selected_title = st.selectbox(
        "Select Wikipedia Article for Audit:",
        options=article_titles,
        index=st.session_state["selected_index"],
    )

    current_index = article_titles.index(selected_title)
    st.session_state["selected_index"] = current_index
    selected_article = articles[current_index]

    article_name = selected_article.get("name", "Untitled")
    abstract_text = selected_article.get("abstract", "")
    raw_infoboxes = selected_article.get("infoboxes", [])
    extracted_facts = extract_infobox_facts(raw_infoboxes)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two-Column Comparison Layout
    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.markdown("### Structured Infobox Facts")
        if extracted_facts:
            st.caption(f"Found {len(extracted_facts)} structured facts in infobox")
            fact_df = [{"Field": f["field"], "Value": f["value"]} for f in extracted_facts]
            st.dataframe(fact_df, width="stretch", hide_index=True)
        else:
            st.warning("No structured infobox fields found for this article.")

    with col_right:
        st.markdown("### Article Lead Abstract Prose")
        st.caption(f"Length: {len(abstract_text.split())} words")
        st.markdown(f'<div class="prose-box">{abstract_text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Audit Trigger Button
    audit_col1, audit_col2, audit_col3 = st.columns([1, 2, 1])
    with audit_col2:
        run_audit = st.button("Run Discrepancy Audit", type="primary", width="stretch")

    session_audit_key = f"audit_results_{current_index}"

    if run_audit:
        if not extracted_facts:
            st.warning("Cannot run audit: No infobox facts extracted for this article.")
        else:
            with st.spinner("Auditing infobox facts against lead prose..."):
                audit_data = run_auditor(abstract_text, extracted_facts)
                st.session_state[session_audit_key] = audit_data

    # Display Audit Results
    if session_audit_key in st.session_state:
        audit_results = st.session_state[session_audit_key]

        st.markdown("## Discrepancy Audit Results")

        total = len(audit_results)
        matches = sum(1 for r in audit_results if r.get("status") == "Match")
        mismatches = total - matches
        match_rate = (matches / total * 100) if total > 0 else 0

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-container"><div class="metric-value">{total}</div><div class="metric-label">Facts Audited</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-container"><div class="metric-value" style="color: #4ade80;">{matches}</div><div class="metric-label">Matches</div></div>',
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f'<div class="metric-container"><div class="metric-value" style="color: #fbbf24;">{mismatches}</div><div class="metric-label">Potential Mismatches</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f'<div class="metric-container"><div class="metric-value" style="color: #38bdf8;">{match_rate:.0f}%</div><div class="metric-label">Match Rate</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Export Report Download Button
        report_md_content = generate_markdown_report(article_name, abstract_text, audit_results)
        st.download_button(
            label="Export Full Audit Report (Markdown)",
            data=report_md_content,
            file_name=f"WikiFactCheck_Audit_{article_name.replace(' ', '_')}.md",
            mime="text/markdown",
            width="stretch",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Filter Options
        filter_status = st.radio(
            "Filter Audit Findings:",
            options=["All Findings", "Matches Only", "Possible Mismatches Only"],
            horizontal=True,
        )

        filtered_results = audit_results
        if filter_status == "Matches Only":
            filtered_results = [r for r in audit_results if r.get("status") == "Match"]
        elif filter_status == "Possible Mismatches Only":
            filtered_results = [r for r in audit_results if r.get("status") == "Possible mismatch detected"]

        # Render expanders with status tags & editor action box
        for item in filtered_results:
            field = item.get("field", "Unknown Field")
            infobox_val = item.get("infobox_value", "")
            text_val = item.get("text_value", "")
            status = item.get("status", "Match")
            category = item.get("category", "Match")
            explanation = item.get("explanation", "")

            if status == "Match":
                badge_html = '<span class="badge-match">Match</span>'
            else:
                badge_html = f'<span class="badge-mismatch">Possible mismatch detected</span><span class="badge-category">{category}</span>'

            expander_title = f"{field}: {infobox_val}"

            with st.expander(expander_title):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown("**Infobox Value:**")
                    st.info(infobox_val)
                with c2:
                    st.markdown("**Article Prose Context:**")
                    st.code(text_val, language="text")

                st.markdown(f"**Audit Status:** {badge_html}", unsafe_allow_html=True)
                st.markdown(f"**Explanation:** {explanation}")

                # Editor Action Box for Mismatches
                if status != "Match":
                    st.markdown("---")
                    st.markdown("📝 **Editor Action — Wikipedia Talk Page Template Snippet:**")
                    st.caption("Copy this pre-formatted snippet to post on the Wikipedia article Talk Page for editor review:")
                    talk_snippet = (
                        f"{{{{WikiFactCheck-Note | field = {field} | infobox = {infobox_val} | lead_text = {text_val} | note = Possible mismatch detected ({category}) for editor review.}}}}"
                    )
                    st.code(talk_snippet, language="text")


if __name__ == "__main__":
    main()
