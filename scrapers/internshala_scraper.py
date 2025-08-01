import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Function to scrape job description and skills from individual job page
def get_job_details(job_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        res = requests.get(job_url, headers=headers)
        job_soup = BeautifulSoup(res.text, "html.parser")

        desc_tag = job_soup.find("div", class_="text-container")
        description = desc_tag.get_text(strip=True) if desc_tag else "N/A"

        skill_tags = job_soup.find_all("li")
        skills = [s.get_text(strip=True) for s in skill_tags]
        skills_text = ", ".join(skills) if skills else "N/A"

        return description, skills_text

    except Exception as e:
        print(f"⚠️ Failed to fetch details from: {job_url}")
        return "N/A", "N/A"


# Main scraper
def scrape_internshala_jobs(job_titles, location=None, pages=3):
    all_jobs = []

    # Combine job titles and location into a single keyword string
    search_keywords = job_titles + ([location] if location else [])
    raw_keywords = ", ".join(search_keywords)
    encoded_keywords = raw_keywords.replace(" ", "%20").replace(",", "%2C")

    for page in range(1, pages + 1):
        url = f"https://internshala.com/jobs/keywords-{encoded_keywords}/page-{page}/"
        print(f"🔍 Scraping listing page: {url}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print("⚠️ Failed to load page:", e)
            continue

        jobs = soup.find_all("div", class_="individual_internship")

        for item in jobs:
            try:
                title_tag = item.find("a", class_="job-title-href") 
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                company_tag = item.find("p", class_="company-name")
                company = company_tag.get_text(strip=True) if company_tag else "N/A"

                location_tag = item.find("span")
                location = location_tag.get_text(strip=True) if location_tag else "N/A"

                salary_tag = item.find("span", class_="desktop")
                salary = salary_tag.get_text(strip=True) if salary_tag else "N/A"

                job_type_tag = item.find("div", class_="status-li")
                job_type = job_type_tag.get_text(strip=True) if job_type_tag else "N/A"

                experience_tag = item.find_all("div", class_="row-1-item")
                experience = experience_tag[1].get_text(strip=True) if len(experience_tag) > 1 else "N/A"

                job_link_tag = item.find("a", class_="job-title-href")
                job_url = "https://internshala.com" + job_link_tag["href"] if job_link_tag else "N/A"

                description, skills = get_job_details(job_url)

                all_jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "job_type": job_type,
                    "experience": experience,
                    "description": description,
                    "skills": skills,
                    "job_url": job_url,
                    "platform": "Internshala",
                    "keywords_used": raw_keywords
                })

            except Exception as e:
                print("⚠️ Skipping job due to error:", e)
                continue

        time.sleep(1)

    return pd.DataFrame(all_jobs)


# Example usage
if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    keywords = ["data analyst", "data engineer"]
    location = "Bangalore"
    df = scrape_internshala_jobs(job_titles=keywords, location=location, pages=5)
    df.to_csv("data/raw/internshala.csv", index=False)
    print(f"\n✅ Scraped {len(df)} job listings. Saved to data/raw/internshala.csv")
