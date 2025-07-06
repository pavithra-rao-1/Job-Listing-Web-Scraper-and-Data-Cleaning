import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import pandas as pd
import os
import time

def scrape_linkedin_jobs(job_titles, location="India", pages=5):
    os.makedirs("data/raw", exist_ok=True)
    job_list = []

    for role in job_titles:
        encoded_role = quote_plus(role)
        encoded_location = quote_plus(location)
        print(f"\n🔍 Scraping jobs for role: {role} | Location: {location}")

        for page in range(pages):
            start = page * 25
            list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_role}&location={encoded_location}&start={start}"
            print(f"   ↪ Page {page + 1}: {list_url}")

            try:
                response = requests.get(list_url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"   ⚠️ Failed to fetch job list: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.find_all("li")

            for job in jobs:
                job_post = {"searched_role": role}
                try:
                    base_card = job.find("div", class_="base-card")
                    if not base_card:
                        continue
                    job_id = base_card.get("data-entity-urn", "").split(":")[-1]
                    job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
                    job_res = requests.get(job_url)
                    job_soup = BeautifulSoup(job_res.text, "html.parser")

                    job_post["job_title"] = job_soup.find("h2", class_="top-card-layout__title").get_text(strip=True)
                    job_post["company_name"] = job_soup.find("a", class_="topcard__org-name-link").get_text(strip=True)
                    job_post["company_link"] = job_soup.find("a", class_="topcard__org-name-link")["href"]
                    job_post["job_location"] = job_soup.find("span", class_="topcard__flavor--bullet").get_text(strip=True)
                    job_post["time_posted"] = job_soup.find("span", class_="posted-time-ago__text").get_text(strip=True)

                    num_applicants_tag = job_soup.find("span", class_="num-applicants__caption")
                    job_post["num_applicants"] = num_applicants_tag.get_text(strip=True) if num_applicants_tag else "N/A"

                    desc_tag = job_soup.find("div", class_="show-more-less-html__markup")
                    job_post["skills"] = desc_tag.get_text(strip=True) if desc_tag else "N/A"

                    job_post["job_url"] = job_url

                except Exception as e:
                    print(f"   ⚠️ Error parsing job: {e}")
                    continue

                job_list.append(job_post)
            time.sleep(1)

    df = pd.DataFrame(job_list)
    df.to_csv("data/raw/linkedIn.csv", index=False)
    print(f"\n✅ Scraped {len(df)} job listings. Saved to data/raw/linkedIn.csv")
    return df
