import streamlit as st
from scraper import scrape_target_sections
from parser import parse_summary

st.title("🏢 Seller Profile Setup")

url = st.text_input("Enter your company's website URL:", placeholder="https://yourcompany.com")

if 'seller_deep_profile' not in st.session_state:
    st.session_state['seller_deep_profile'] = None

if st.button("Analyze My Company"):
    with st.spinner("Scraping and analyzing..."):
        try:
            sections = scrape_target_sections(url)
            raw_content = "\n\n".join(sections.values())

            st.subheader("🔍 Scraped Website Content:")
            st.text(raw_content if raw_content else "Nothing scraped.")

            if raw_content.strip():
                summary = parse_summary(raw_content)
                st.session_state["seller_deep_profile"] = summary
                st.success("✅ Seller profile saved!")
                st.subheader("🧠 GPT's Sales Profile of Your Company:")
                st.markdown(summary)
            else:
                st.warning("No meaningful content found.")
        except Exception as e:
            st.error(f"Error: {e}")

