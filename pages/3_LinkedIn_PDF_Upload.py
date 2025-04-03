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
    "You're helping a strategic sales rep prep for a hyper-personalized discovery call with a specific prospect.\n\n"
    "Here’s what you know:\n"
    f"- Seller’s company summary: {st.session_state['seller_summary']}\n"
    f"- Prospect’s company summary: {st.session_state['prospect_summary']}\n"
    f"- Prospect’s LinkedIn profile summary (first 2 pages):\n\n\"\"\"{text}\"\"\"\n\n"
    "---\n\n"
    "Please return **two things** only:\n\n"
    "---\n\n"
    "**1. Key Seller Value Props to Highlight (Based on This Prospect)**\n"
    "List 3–5 specific parts of the seller’s offering that would resonate most with this prospect. "
    "Explain *why each one matters*, based on their company’s needs, the buyer’s role, or likely challenges.\n\n"
    "---\n\n"
    "**2. Five Hyper-Personalized Discovery Questions (Mimic Example Format)**\n\n"
    "Each question should follow this exact format:\n\n"
    "1. **Tied to [Strategic Insight]**  \n"
    "“[Sharp, relevant discovery question — open-ended and sales-driven]”\n\n"
    "**Why this hits:**  \n"
    "Explain why this question is meaningful *in the context of this buyer*. "
    "Connect to a known pain, initiative, or goal — and how the seller's product helps.\n\n"
    "---\n\n"
    "📌 Example:\n\n"
    "1. **Tied to the Rebrand + Demand Gen**  \n"
    "“With the rebrand to Verita, how is your team thinking about building visibility or trust with new prospects through live or virtual experiences?”\n\n"
    "**Why this hits:**  \n"
    "Savannah’s job is to drive business development — she’ll care about brand trust, awareness, and high-quality lead engagement. "
    "Events are a huge lever for this, especially post-rebrand.\n\n"
    "---\n\n"
    "❌ Avoid:\n"
    "- Generic or innovation-for-the-sake-of-it questions\n"
    "- Vague or operational “how do you evaluate solutions” angles\n"
    "- Anything that wouldn’t directly help a seller qualify need or uncover urgency\n\n"
    "✅ Do:\n"
    "- Tie questions clearly to the buyer’s role, goals, or company initiatives\n"
    "- Focus on conversations that help surface need, friction, or fit\n\n"
    "Do not summarize anything — go straight to the value props and formatted questions."
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
