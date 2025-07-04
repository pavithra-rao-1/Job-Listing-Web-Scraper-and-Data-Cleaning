import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote_plus
import os
import time

# Create output directory
os.makedirs("data/raw", exist_ok=True)

# Define job roles and location
job_roles = ["Data Scientist", "Python Developer", "Machine Learning Engineer", "Data Analyst", "AI Engineer", "Data Engineer", "Business Analyst"]
location = "India"
pages = 10

# Initialize job list
job_list = []

for role in job_roles:
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
            job_post = {"role": role}
            try:
                base_card = job.find("div", class_="base-card")
                job_id = base_card["data-entity-urn"].split(":")[3]
                job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
                job_res = requests.get(job_url)
                job_soup = BeautifulSoup(job_res.text, "html.parser")

                job_post["job_title"] = job_soup.find("h2", class_="top-card-layout__title").text.strip()
                job_post["company_name"] = job_soup.find("a", class_="topcard__org-name-link").text.strip()
                job_post["company_link"] = job_soup.find("a", class_="topcard__org-name-link")["href"]
                job_post["job_location"] = job_soup.find("span", class_="topcard__flavor--bullet").text.strip()
                job_post["time_posted"] = job_soup.find("span", class_="posted-time-ago__text").text.strip()
                job_post["num_applicants"] = job_soup.find("span", class_="num-applicants__caption").text.strip()
                job_post["skills"] = job_soup.find("div", class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden").text.strip()
            except Exception:
                continue

            job_list.append(job_post)
        time.sleep(1)

# Save to CSV
df = pd.DataFrame(job_list)
df.to_csv("data/raw/linkedIn.csv", index=False)
print("\n✅ Scraping complete. Data saved to data/raw/linkedIn.csv")
