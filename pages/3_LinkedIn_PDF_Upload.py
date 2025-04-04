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
    "Your goal is to write 5 smart, natural, and strategic discovery questions. They should sound like a sharp AE who did their homework — not a product marketer.\n\n"
    "Each question should follow this format:\n\n"
    "1. **Tied to [Strategic Insight]**  \n"
    "“[Discovery question]”\n\n"
    "**Why this hits:**  \n"
    "Explain the pain it uncovers and how it connects to the seller’s offering — not by pitching, but by revealing friction they probably feel.\n\n"
    "---\n\n"
    "📌 Example Outputs (Use These As a Guide):\n\n"
    "**Tied to the Rebrand + Demand Gen**  \n"
    "“With the rebrand to Verita, how is your team thinking about building visibility or trust with new prospects through live or virtual experiences?”\n\n"
    "**Why this hits:**  \n"
    "Savannah’s job is to drive business development — she’ll care about brand trust, awareness, and high-quality lead engagement. Events are a huge lever for this, especially post-rebrand.\n\n"
    "**Tied to Her Role in Growth**  \n"
    "“What role do events or educational webinars currently play in your outreach or client conversion efforts?”\n\n"
    "**Why this hits:**  \n"
    "You’re connecting directly to her BD role — this lets you explore if Verita is using events as a sales or marketing channel, and where there might be inefficiencies.\n\n"
    "**Tied to Pain Points from Rebranding**  \n"
    "“How are you currently managing communications and invitations across your newly combined client base from the KCC, Gilardi, and RicePoint ecosystems?”\n\n"
    "**Why this hits:**  \n"
    "Rebranding = new challenges around messaging and segmentation. Cvent’s tools can solve that. You’re pointing right at a likely source of growing pains.\n\n"
    "**Tied to Operational Inefficiency (her Apple ops background)**  \n"
    "“Given your background in ops-heavy roles — what parts of running outreach or client-facing events still feel more manual than they should?”\n\n"
    "**Why this hits:**  \n"
    "You’re appealing to her personal lens — she likely sees inefficiencies others miss. This helps build trust and surfaces problems you can solve.\n\n"
    "**Tied to Data/Compliance Needs**  \n"
    "“In a space like fiduciary services, what kind of reporting or audit-readiness do you need after an event or mass communication?”\n\n"
    "**Why this hits:**  \n"
    "Verita is in a hyper-regulated space. They likely need proof of delivery, attendance, consent — and Cvent can deliver that. This question aligns with compliance pressure.\n\n"
    "---\n\n"
    "🧠 Now, generate 5 new discovery questions and value props for the current prospect. Match the structure and tone above."
)


                st.markdown(response.choices[0].message.content.strip())

            elif not st.session_state.get("seller_deep_profile") or not st.session_state.get("prospect_summary"):
                st.warning("❗ Please complete the seller profile and prospect analysis pages before using this step.")

        except Exception as e:
            st.error(f"Error processing PDF: {e}")
else:
    st.info("Please upload a LinkedIn PDF to begin.")
