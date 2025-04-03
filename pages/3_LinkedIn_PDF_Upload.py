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
    "You're helping a strategic sales rep prep for a discovery call with a prospect.\n\n"
    "You’ve already researched:\n"
    f"- Seller’s company: {st.session_state['seller_summary']}\n"
    f"- Prospect’s company: {st.session_state['prospect_summary']}\n"
    f"- Prospect’s LinkedIn profile (first 2 pages):\n\n\"\"\"{text}\"\"\"\n\n"
    "---\n\n"
    "🎯 Your job is to write two things that directly support a sales conversation:\n\n"
    "---\n\n"
    "**PART 1: Value Props That Will Land**\n\n"
    "List 3–5 of the seller’s offerings that will **actually resonate** with this specific prospect.\n"
    "- Each value prop must be clearly tied to the buyer’s company priorities, role, or friction points\n"
    "- Avoid generic phrasing like “efficiency,” “innovation,” or “solutions”\n"
    "- Focus on what the buyer *cares about*, not what the product does\n\n"
    "---\n\n"
    "**PART 2: 5 Strategic Discovery Questions**\n\n"
    "Each question should follow this exact format:\n\n"
    "1. **Tied to [Strategic Insight]**  \n"
    "“[Open-ended, sales-relevant discovery question — no fluff, no feature pitches]”\n\n"
    "**Why this hits:**  \n"
    "Explain what this question is really targeting — a pain, a process, or a pressure. Tie it **directly** to something surfaced in the LinkedIn profile or prospect company overview.\n\n"
    "Use natural, confident sales language. These questions should feel like something a sharp AE would actually say on a call.\n\n"
    "---\n\n"
    "📌 Examples of good structure and tone:\n\n"
    "- **Tied to the Merger + Event Outreach Complexity**  \n"
    "“With clients now coming from KCC, Gilardi, RicePoint, etc., how are you managing segmentation and messaging across those different audiences during event outreach?”\n\n"
    "**Why this hits:**  \n"
    "This points to a real pain: merged contact lists, complex targeting, and disjointed messaging. Cvent simplifies this across live and virtual events.\n\n"
    "- **Tied to Her Role in Growth**  \n"
    "“What role do events or educational webinars currently play in your outreach or client conversion efforts?”\n\n"
    "**Why this hits:**  \n"
    "This ties to her BD role — it surfaces whether events are being used to drive pipeline or stay top-of-funnel.\n\n"
    "---\n\n"
    "🚫 Do NOT:\n"
    "- Ask generic questions like “what do you look for in a partner” or “how important is efficiency”\n"
    "- Use empty terms like “industry-leading” or “digital transformation”\n"
    "- Make the prospect explain why they should need you\n\n"
    "✅ DO:\n"
    "- Help the seller sound intuitive, confident, and informed\n"
    "- Make every question something the rep would be proud to say\n\n"
    "Do not summarize anything. Go straight to the outputs. Format exactly as shown."
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
