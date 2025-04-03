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
    "You're helping a sales rep prepare to speak with a specific prospect. Based on the following inputs:\n\n"
    f"- Seller’s company summary: {st.session_state['seller_summary']}\n"
    f"- Prospect’s company summary: {st.session_state['prospect_summary']}\n"
    f"- The prospect’s LinkedIn profile summary (from the first 2 pages):\n\n\"\"\"{text}\"\"\"\n\n"
    "Perform two tasks:\n\n"
    "---\n\n"
    "**PART 1: Match the Seller's Value Props to the Prospect**\n\n"
    "List the 3–5 parts of the seller’s offering that are most likely to resonate with this prospect. For each, briefly explain *why*, based on their role, company priorities, or background.\n\n"
    "---\n\n"
    "**PART 2: Generate 5 Strategic Discovery Questions**\n\n"
    "For each question, follow this exact format:\n\n"
    "1. **Tied to [Strategic Insight]**  \n"
    "“[Personalized, open-ended discovery question]”\n\n"
    "**Why this hits:**  \n"
    "[Explain why this question matters, using something specific from the prospect’s role, company initiatives, background, or the seller’s relevant capabilities.]\n\n"
    "Examples of strategic insights: recent rebrand, operations-heavy background, regulated industry, buyer role, business growth stage, manual processes, recent acquisitions, etc.\n\n"
    "These should feel handcrafted, deeply personalized, and grounded in the inputs provided — not generic. Avoid fluff."
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
