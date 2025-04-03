import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def parse_summary(raw_content):
    prompt = (
        "You're an expert business analyst. Based on the website content below, summarize:\n\n"
        "1. What this company does.\n"
        "2. Their core product or service areas.\n"
        "3. Who they serve.\n"
        "4. Any standout value propositions or specialties.\n\n"
        "Website content:\n"
        + raw_content
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You summarize company value props from websites."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def parse_prospect_breakdown(raw_content):
    prompt = (
        "You're a strategic sales researcher helping an enterprise seller understand a target company.\n\n"
        "From the website content below, break it into three clearly labeled sections using markdown:\n\n"
        "### 📌 About / What They Do\n"
        "Summarize in 2–3 sentences what the company does, including its history, focus areas, and target industries.\n\n"
        "### 📰 Recent News or Strategic Changes\n"
        "Mention any rebrands, leadership changes, product launches, mergers, acquisitions, or major industry pivots. If nothing is obvious, say 'None found.'\n\n"
        "### 🛠️ Products & Services\n"
        "List up to 5 core services or product categories with a 1-line description for each.\n\n"
        "Only use info from the website text. Don’t guess or fill in fluff.\n\n"
        "Website content:\n"
        + raw_content
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You generate strategic summaries from websites."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()