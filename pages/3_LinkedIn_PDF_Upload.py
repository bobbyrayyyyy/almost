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
    "You're helping a top-performing sales rep prepare for a hyper-personalized discovery call with a specific prospect.\n\n"
    "You’ve already researched:\n"
    f"- The seller’s company: {st.session_state['seller_summary']}\n"
    f"- The prospect’s company: {st.session_state['prospect_summary']}\n"
    f"- The prospect’s LinkedIn profile (first 2 pages):\n\n\"\"\"{text}\"\"\"\n\n"
    "---\n\n"
    "🎯 Your job:\n"
    "Write **two sections** that directly support a real sales conversation.\n\n"
    "---\n\n"
    "**PART 1: Value Props That Will Land**\n\n"
    "List the 3–5 most relevant value props from the seller’s offering *that will land with this specific prospect*.\n\n"
    "- Each one must be specific and clearly tied to something from the prospect’s company, industry, or role.\n"
    "- Avoid generic tech/innovation themes unless they directly relate to real friction or urgency.\n\n"
    "---\n\n"
    "**PART 2: 5 Strategic Discovery Questions**\n\n"
    "Write five sharp, strategic discovery questions the rep could ask. Use the following format for each:\n\n"
    "1. **Tied to [Strategic Insight]**  \n"
    "“[Open-ended, conversational discovery question — avoid sounding like a pitch or demo opener]”\n\n"
    "**Why this hits:**  \n"
    "Call out the relevant pain point, initiative, shift, or role insight. Tie it directly to Cvent’s offering or strategic value — but subtly. Prioritize **buyer psychology** and **situation framing**, not “pitch language.”\n\n"
    "---\n\n"
    "🎯 Examples of what good sounds like:\n"
    "- “With the rebrand to Verita, how is your team thinking about building visibility or trust with new prospects through live or virtual experiences?”\n"
    "- “From your experience in ops-heavy roles, where do you still see the most manual lift when planning or running outreach campaigns or events?”\n"
    "- “How are you currently managing communications and invitations across your newly combined client base from the KCC, Gilardi, and RicePoint ecosystems?”\n\n"
    "---\n\n"
    "❌ Do NOT:\n"
    "- Ask buyers to tell us why they need software\n"
    "- Use buzzwords like “solutions,” “enhance,” “evaluate software,” or “digital transformation”\n"
    "- Ask questions that sound like feature fishing\n\n"
    "✅ DO:\n"
    "- Make the rep sound informed, intuitive, and strategic\n"
    "- Bake in context — this should feel like a tailored conversation starter\n\n"
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
