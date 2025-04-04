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

            # ✅ Use updated session key for deep seller summary
            if text.strip() and st.session_state.get("seller_deep_profile") and st.session_state.get("prospect_summary"):
                st.subheader("🧠 GPT-Powered Analysis")

                from openai import OpenAI
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                full_prompt = (
                    "You're helping a sales rep prepare for a discovery conversation with a prospect.\n\n"
                    "The seller’s product is very specific: they help companies run impactful in-person and virtual events. Their platform covers:\n"
                    "- Registration and invitations\n"
                    "- Segmentation of attendees\n"
                    "- Email and outreach coordination\n"
                    "- Webinars and education-style events\n"
                    "- Tracking attendance and engagement\n"
                    "- Post-event analytics\n"
                    "- CRM and compliance reporting\n\n"
                    "The buyer is not shopping for software. Your job is to help the rep start a real conversation that reveals pain or opportunity around how the prospect handles any of the above.\n\n"
                    "---\n\n"
                    "You’ve already researched:\n"
                    f"- Seller’s company: {st.session_state['seller_deep_profile']}\n"
                    f"- Prospect’s company: {st.session_state['prospect_summary']}\n"
                    f"- Prospect’s LinkedIn summary (first 2 pages): \n\n\"\"\"{text}\"\"\"\n\n"
                    "---\n\n"
                    "Return two things only:\n\n"
                    "---\n\n"
                    "**PART 1: Event Use Cases That Might Resonate**\n\n"
                    "List 3–5 parts of the seller’s offering that are most likely to be valuable to this prospect — based on what their company does, what the person does, and how they probably handle external or internal communication today.\n\n"
                    "✅ Focus only on how this prospect might:\n"
                    "- Use events for outreach or education\n"
                    "- Struggle to segment audiences after a merger or acquisition\n"
                    "- Have disjointed communication across departments\n"
                    "- Need visibility into attendance or engagement\n"
                    "- Be pressured to do more client-facing work\n"
                    "- Need post-event proof for compliance or reporting\n\n"
                    "---\n\n"
                    "**PART 2: 5 Discovery Questions Around Outreach + Events**\n\n"
                    "Write 5 conversational discovery questions tied to:\n"
                    "- How they run outreach or education today\n"
                    "- Where their audience coordination breaks down\n"
                    "- What they do when they need people to show up or respond\n"
                    "- What manual lift exists in running events or trainings\n"
                    "- How they handle post-event follow-up or compliance\n\n"
                    "Each question should follow this format:\n\n"
                    "1. **Tied to [Real Insight You Noticed]**  \n"
                    "“[Sales-relevant discovery question — focus on outreach, engagement, or event coordination friction]”\n\n"
                    "**Why this hits:**  \n"
                    "Explain the real pain it uncovers — and how that could point to using events to coordinate, educate, or track.\n\n"
                    "---\n\n"
                    "Do not summarize anything. Go straight to the outputs. Be specific, grounded, and tied to what the seller actually sells."
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

            elif not st.session_state.get("seller_deep_profile") or not st.session_state.get("prospect_summary"):
                st.warning("❗ Please complete the seller profile and prospect analysis pages before using this step.")

        except Exception as e:
            st.error(f"Error processing PDF: {e}")
else:
    st.info("Please upload a LinkedIn PDF to begin.")

