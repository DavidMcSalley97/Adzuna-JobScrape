# Adzuna UK Care Job Scraper

---

## Output Format

The script generates:

```
uk_care_jobs.json
```

Each record contains:

```json
{
  "title": "Care Assistant",
  "company": "Health Care Ltd",
  "location": "Manchester",
  "salary_min": "£22,000",
  "salary_max": "£24,000",
  "phone_number": "+447123456789",
  "redirect_url": "https://..."
}
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/DavidMcSalley97/adzuna-job-scraper.git
cd adzuna-job-scraper
```

Install dependencies:

```bash
pip3 install requests
```

---

## Usage

Run the scraper:

```bash
python Job-Scraper.py
```

stop the script:

```
Ctrl + C
```

Progress will automatically save to:

```
uk_care_jobs.json
```

---

## PowerShell Commands

### View Companies With Multiple Job Listings

```powershell
$json = Get-Content .\uk_care_jobs.json -Raw | ConvertFrom-Json
$json | Group-Object company | Where-Object { $_.Count -gt 1 } | Select-Object Name, Count
```

---

### Total Duplicate Company Entries

```powershell
$json = Get-Content .\uk_care_jobs.json -Raw | ConvertFrom-Json
($json | Group-Object company | Where-Object { $_.Count -gt 1 } |
ForEach-Object { $_.Count - 1 } | Measure-Object -Sum).Sum
```

