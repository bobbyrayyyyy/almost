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
    "You are helping a sales rep prepare for a hyper-personalized outreach.\n\n"
    "Here’s what you know:\n"
    f"- Seller’s company summary: {st.session_state['seller_summary']}\n"
    f"- Prospect’s company summary: {st.session_state['prospect_summary']}\n"
    f"- This is the LinkedIn profile summary (first 2 pages) of the prospect they’re targeting:\n\n{text}\n\n"
    "From this context, generate the following:\n\n"
    "1. A list of which parts of the seller’s offering are most likely to resonate with this prospect — based on their role, company focus, and likely pain points.\n"
    "   - Be specific and tie each part of the offering to something relevant from the prospect’s company or role.\n\n"
    "2. Five deeply personalized discovery questions the rep could ask, each following this format:\n\n"
    "    - **Headline**: Explain what the question is tied to (e.g., role, company initiative, career background, etc.)\n"
    "    - **Question**: Phrase it as a conversational open-ended discovery question\n"
    "    - **Why this hits**: Explain why this question is likely to resonate, based on the context above\n\n"
    "Do not add fluff. These questions should be sharp, strategic, and visibly informed by the research provided."
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
