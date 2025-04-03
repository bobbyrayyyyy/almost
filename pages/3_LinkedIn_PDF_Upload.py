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
    "You're helping a smart, strategic AE prep for a discovery call with a prospect.\n\n"
    "You already know:\n"
    f"- The seller’s company: {st.session_state['seller_summary']}\n"
    f"- The prospect’s company: {st.session_state['prospect_summary']}\n"
    f"- The prospect’s LinkedIn summary (first 2 pages): \n\n\"\"\"{text}\"\"\"\n\n"
    "---\n\n"
    "Your job is to return **two things only**, written in the voice of a confident AE who’s done their homework — not a product marketer.\n\n"
    "---\n\n"
    "**PART 1: Seller Value Props That Might Land**\n\n"
    "List 3–5 of the seller’s offerings that are most *likely* to resonate with this buyer.\n"
    "✅ You don’t have to be perfect. Just call out things that might hit based on their:\n"
    "- Company structure\n"
    "- Role\n"
    "- Market\n"
    "- Challenges they’re probably facing\n\n"
    "These can be informed guesses. Be human. Be strategic. Avoid vague buzzwords.\n\n"
    "---\n\n"
    "**PART 2: 5 Creative Discovery Questions**\n\n"
    "Write 5 open-ended discovery questions that *feel like someone smart and observant would ask* — not like a form being filled out.\n\n"
    "Use this format:\n\n"
    "1. **Tied to [Strategic Insight or Detail You Noticed]**  \n"
    "“[Casual but pointed question — think like a curious rep trying to surface real stuff]”\n\n"
    "**Why this hits:**  \n"
    "Call out the angle. Is it tied to a merger? A segmented client base? A complex buyer journey? A high-stakes service? A background in ops? Say why it’s smart to ask.\n\n"
    "You’re allowed to be playful, slightly unexpected, or take a risk. These are door-opening questions, not qualification checklists.\n\n"
    "---\n\n"
    "📌 A few example vibes:\n"
    "- “With clients coming from KCC, Gilardi, and RicePoint — are you treating those audiences separately when it comes to events or outreach?”\n"
    "- “You’ve got ops and BD in your background — what’s still annoyingly manual when you run campaigns or launch events?”\n"
    "- “How are you getting the right people to show up when you host something like a fiduciary or restructuring update?”\n\n"
    "---\n\n"
    "🚫 Don’t:\n"
    "- Ask them to justify needing a tool\n"
    "- Ask about evaluating software\n"
    "- Use phrases like “industry-leading,” “solutions,” or “ensure alignment”\n\n"
    "✅ Do:\n"
    "- Ask things a rep would actually want to know\n"
    "- Point to moments where communication, segmentation, or engagement might fall apart\n"
    "- Use natural, real-world tone — not formal business writing\n\n"
    "No summary. Just value props and formatted questions. Be smart, confident, and a little free."
)





                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a B2B sales strategy assistant."},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.9,
                    max_tokens=1000
                )

                st.markdown(response.choices[0].message.content.strip())

            elif not st.session_state.get("seller_summary") or not st.session_state.get("prospect_summary"):
                st.warning("❗ Please complete the seller profile and prospect analysis pages before using this step.")

        except Exception as e:
            st.error(f"Error processing PDF: {e}")
else:
    st.info("Please upload a LinkedIn PDF to begin.")
