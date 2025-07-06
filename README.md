
# 🧑‍💼 Job Listing Web Scraper

A Streamlit-powered web application that scrapes job listings from **Internshala** and **LinkedIn**, based on user-defined job titles and locations. Useful for job seekers, career changers, and data enthusiasts looking for real-time job market insights.

🚀 [Live Demo](https://job-listing-web-scraper.streamlit.app/)

---

## 📌 Features

- 🔍 Search by **job title(s)** and **location**
- 🧾 Scrapes job data from:
  - **Internshala**
  - **LinkedIn**
- 📑 Displays results in scrollable tables
- 💾 Download job listings as CSV
- 📊 Minimal, user-friendly interface using **Streamlit**

---

## 📁 Project Structure

```
job-listing-webscraper/
├── scrapers/
│   ├── internshala_scraper.py
│   └── linkedin_scraper.py
├── data/
│   └── raw/
├── dashboard/
│   └── (optional components or visualizations)
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛠️ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/job-listing-webscraper.git
cd job-listing-webscraper
```

### 2. Set Up a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate    # For macOS/Linux
venv\Scripts\activate       # For Windows
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app.py
```

---

## 🧪 Sample Usage

- Enter job titles: `data analyst, python developer`
- Enter location: `Chennai` or leave empty
- Select number of pages to scrape (1–10)
- Click **Search Jobs** and view results

---

## 📦 Output

Two CSV files are saved to the `data/raw/` directory:
- `internshala.csv`
- `linkedIn.csv`

Each contains structured job data like:
- Job Title
- Company
- Location
- Salary
- Job Type
- Experience
- Description
- Skills
- Job URL
- Platform
- Keywords Used

---

## 📌 To-Do / Future Improvements

- [ ] Add keyword-based job scoring
- [ ] Add time-based filters (e.g. posted in last X days)
- [ ] Add clustering of similar job roles
- [ ] Enable automated email alerts for new jobs

---

## 📚 Requirements

- Python 3.7+
- BeautifulSoup4
- Requests
- Pandas
- Streamlit

All dependencies are listed in `requirements.txt`.

---

## 📄 License

MIT License

---


