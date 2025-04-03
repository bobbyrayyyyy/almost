import streamlit as st
import fitz  # PyMuPDF
from parser import parse_summary
from parser import parse_prospect_breakdown

st.title("🔗 Prospect LinkedIn PDF Upload")

uploaded_file = st.file_uploader("Upload your prospect's LinkedIn profile (PDF format)", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded.")
    with st.spinner("Reading and analyzing first 2 pages..."):
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for i in range(min(2, len(doc))):
                page = doc.load_page(i)
                text += page.get_text()

            st.subheader("📄 Extracted Text (First 2 Pages Only)")
            st.text(text if text.strip() else "No useful text found on the first 2 pages.")

            if text.strip() and st.session_state.get("seller_summary") and st.session_state.get("prospect_summary"):
                st.subheader("🧠 GPT-Powered Analysis")

                from openai import OpenAI
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                full_prompt = (
    "You're helping a strategic B2B sales rep prepare for a discovery conversation with a prospect.\n\n"
    "You've already researched:\n"
    f"- Seller’s company: {st.session_state['seller_summary']}\n"
    f"- Prospect’s company: {st.session_state['prospect_summary']}\n"
    f"- Prospect’s LinkedIn profile summary (first 2 pages): \n\n\"\"\"{text}\"\"\"\n\n"
    "---\n\n"
    "Your job is to write two outputs that support a real, high-quality sales conversation — not marketing fluff.\n\n"
    "---\n\n"
    "**PART 1: Seller Value Props That Will Land**\n\n"
    "List 3–5 parts of the seller’s offering that would most resonate with this buyer, based on their role, responsibilities, and company needs.\n\n"
    "✅ Each one should:\n"
    "- Be directly tied to real-world friction (e.g. segmentation, manual processes, lead visibility, client education, compliance reporting)\n"
    "- Map clearly to how events, webinars, or outreach tools solve something\n"
    "- Avoid generic themes like “security,” “efficiency,” “innovation,” or “transformation”\n\n"
    "---\n\n"
    "**PART 2: 5 Strategic Discovery Questions**\n\n"
    "Write 5 sharp, personalized discovery questions — using this format:\n\n"
    "1. **Tied to [Strategic Insight]**  \n"
    "“[Open-ended discovery question focused on how they manage X — especially in relation to outreach, education, or events.]”\n\n"
    "**Why this hits:**  \n"
    "Explain the real friction or pressure this question surfaces. Tie it to the **seller’s capabilities** (events, segmentation, virtual + live experiences, post-event tracking, engagement, etc.)\n\n"
    "These questions should feel like they’re coming from a top AE — confident, conversational, and informed.\n\n"
    "---\n\n"
    "📌 Example of great tone:\n\n"
    "1. **Tied to the Merger + Event Outreach Complexity**  \n"
    "“With clients now coming from KCC, Gilardi, RicePoint, etc., how are you managing segmentation and messaging across those different audiences during event outreach?”\n\n"
    "**Why this hits:**  \n"
    "Merged contact lists and fragmented messaging are common post-merger. This question highlights a coordination challenge Cvent solves with targeted outreach and unified messaging.\n\n"
    "---\n\n"
    "🚫 DO NOT:\n"
    "- Ask what they look for in a partner\n"
    "- Ask about technology adoption or software evaluation\n"
    "- Use generic words like “industry-leading,” “solutions,” or “optimize”\n\n"
    "✅ DO:\n"
    "- Anchor in real business complexity or change (mergers, BD pressure, compliance, education)\n"
    "- Make the rep sound sharp, not pitchy\n\n"
    "Only return the value props and formatted questions. No summaries."
)




                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a B2B sales strategy assistant."},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.5,
                    max_tokens=1000
                )

                st.markdown(response.choices[0].message.content.strip())

            elif not st.session_state.get("seller_summary") or not st.session_state.get("prospect_summary"):
                st.warning("❗ Please complete the seller profile and prospect analysis pages before using this step.")

        except Exception as e:
            st.error(f"Error processing PDF: {e}")
else:
    st.info("Please upload a LinkedIn PDF to begin.")
