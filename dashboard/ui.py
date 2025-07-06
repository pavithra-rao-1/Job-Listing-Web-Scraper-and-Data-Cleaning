import streamlit as st
import pandas as pd
from scrapers.internshala_scraper import scrape_internshala_jobs
from scrapers.linkedin_scraper import scrape_linkedin_jobs

st.set_page_config(page_title="Job Listing Scraper", layout="wide")
st.title("📊 Job Listing Scraper - LinkedIn & Internshala")

# --- Sidebar Inputs ---
st.sidebar.header("🔍 Search Filters")
job_titles_input = st.sidebar.text_input("Enter job titles (comma-separated)")
location_input = st.sidebar.text_input("Enter location")
pages = st.sidebar.slider("Number of pages to scrape", min_value=1, max_value=10, value=3)

search = st.sidebar.button("Search Jobs")

if search:
    job_titles = [title.strip() for title in job_titles_input.split(",") if title.strip()]

    with st.spinner("Scraping Internshala jobs..."):
        internshala_df = scrape_internshala_jobs(job_titles, location_input, pages)
        st.subheader("📘 Internshala Jobs")
        st.dataframe(internshala_df, use_container_width=True)

    with st.spinner("Scraping LinkedIn jobs..."):
        linkedin_df = scrape_linkedin_jobs(job_titles, location_input, pages)
        st.subheader("💼 LinkedIn Jobs")
        st.dataframe(linkedin_df, use_container_width=True)

    # Optionally save to CSVs
    internshala_df.to_csv("data/raw/internshala.csv", index=False)
    linkedin_df.to_csv("data/raw/linkedIn.csv", index=False)
    st.success("✅ Scraping complete. CSV files saved to data/raw/")
