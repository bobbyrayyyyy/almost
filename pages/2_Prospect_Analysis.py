import streamlit as st
from scraper import scrape_target_sections
from parser import parse_prospect_breakdown

st.title("🎯 Prospect Website Breakdown")

url = st.text_input("Enter the prospect's website URL:", placeholder="https://prospect.com")

if st.button("Analyze Prospect"):
    with st.spinner("Scraping and breaking down content..."):
        try:
            sections = scrape_target_sections(url)
            raw_content = "\n\n".join(sections.values())

            st.subheader("🔍 Scraped Website Content:")
            st.text(raw_content if raw_content else "Nothing scraped from this website.")

            if raw_content.strip():
                gpt_output = parse_prospect_breakdown(raw_content)
                st.success("✅ GPT Output Below")
                st.markdown(gpt_output)
            else:
                st.warning("No useful content scraped from this site.")
        except Exception as e:
            st.error(f"Error: {e}")