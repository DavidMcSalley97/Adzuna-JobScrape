# Adzuna-JobScrape

# To get count of companies from the json in powershell the command to use: 

```$json = Get-Content .\uk_care_jobs.json -Raw | ConvertFrom-Json
$json | Group-Object company | Where-Object { $_.Count -gt 1 } | 
Select-Object Name, Count```
