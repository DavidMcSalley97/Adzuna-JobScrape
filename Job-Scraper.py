import requests
import json
import re
import time
import signal
import sys
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

APP_ID = "644761c2"
APP_KEY = "fff1d2d67aba26807b7e53334e7486eb"

BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/"
RESULTS_PER_PAGE = 50
OUTPUT_FILE = "uk-care-jobs.json"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

CARE_KEYWORDS = [
    "care assistant",
    "care worker",
    "support worker",
    "healthcare assistant",
    "carer",
    "domiciliary care",
    "care home",
    "residential care",
    "nursing home",
    "elderly care"
]

RECRUITMENT_KEYWORDS = [
    "recruitment", "recruiter", "staffing", "agency",
    "consultant", "consultancy", "talent", "resourcing",
    "solutions", "employment", "workforce", "personnel",
    "hiring", "search ltd", "careers ltd", "temporary",
    "temp", "hr services"
]

AGENCY_DOMAINS = [
    "indeed", "cv-library", "reed", "totaljobs",
    "monster", "jobsite", "staffing", "recruit"
]

PHONE_PATTERN = re.compile(
    r'(\+44\s?7\d{3}|\(?07\d{3}\)?|\+44\s?1\d{3}|\(?01\d{3}\)?)\s?\d{3}\s?\d{3}'
)

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

all_jobs = []
seen = set()

def save_jobs():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(all_jobs)} jobs to {OUTPUT_FILE}")

def handle_exit(sig, frame):
    save_jobs()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

def is_care_job(title, description):
    text = f"{title} {description}".lower()
    return any(keyword in text for keyword in CARE_KEYWORDS)

def is_recruitment(company, description, redirect_url):
    combined = f"{company} {description}".lower()
    if any(word in combined for word in RECRUITMENT_KEYWORDS):
        return True
    if redirect_url:
        domain = urlparse(redirect_url).netloc.lower()
        if any(agency in domain for agency in AGENCY_DOMAINS):
            return True
    return False

def extract_phone(text):
    if not text:
        return None
    match = PHONE_PATTERN.search(text)
    if not match:
        return None
    return re.sub(r"[^\d+]", "", match.group(0))

def format_salary(value):
    if not value:
        return None
    return f"£{int(value):,}"

def generate_key(title, company, location):
    return f"{title.lower()}|{company.lower()}|{location.lower()}"

def fetch_jobs():
    page = 1

    while True:
        print(f"Fetching page {page}")

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": "care",
            "results_per_page": RESULTS_PER_PAGE
        }

        try:
            response = session.get(
                f"{BASE_URL}{page}",
                params=params,
                headers=HEADERS,
                timeout=(5, 30)
            )
        except requests.exceptions.RequestException:
            break

        if response.status_code != 200:
            break

        data = response.json()
        results = data.get("results")

        if not results:
            break

        for job in results:
            title = job.get("title", "")
            company = job.get("company", {}).get("display_name", "")
            location = job.get("location", {}).get("display_name", "")
            description = job.get("description", "")
            redirect_url = job.get("redirect_url")

            if not is_care_job(title, description):
                continue

            if is_recruitment(company, description, redirect_url):
                continue

            key = generate_key(title, company, location)

            if key in seen:
                continue

            seen.add(key)

            all_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary_min": format_salary(job.get("salary_min")),
                "salary_max": format_salary(job.get("salary_max")),
                "phone_number": extract_phone(description),
                "redirect_url": redirect_url
            })

        page += 1
        time.sleep(0.3)

if __name__ == "__main__":
    try:
        fetch_jobs()
    finally:
        save_jobs()
