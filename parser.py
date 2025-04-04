import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def parse_summary(raw_content):
    prompt = (
    "You are a sales rep at this company. Based on the website content below, write a full sales-side breakdown of the business — like you're explaining it to a new AE or SDR so they know exactly how to talk about the company.\n\n"
    "Cover all of the following in clear, direct sales language:\n\n"
    "1. What we do — describe our purpose and domain clearly.\n"
    "2. What we sell — list all major products, services, and feature areas.\n"
    "3. Who we sell to — industries, customer types, and typical roles.\n"
    "4. Why people buy from us — what problems we solve or goals we help with.\n"
    "5. Competitive advantages — what sets us apart from other options on the market (specifics, not just vague strengths).\n"
    "6. Where we’re strong — any industries, use cases, or types of events we’re particularly good at.\n"
    "7. What makes our offering credible — proof points, platform depth, integrations, data, partnerships, etc.\n\n"
    "This should read like internal sales enablement content — not marketing fluff or customer-facing copy.\n\n"
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
