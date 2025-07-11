from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from email_sender import send_job_template_email
from config import DEFAULT_QUERY
from datetime import datetime
from openaiAPI import generate_updated_resume, update_existing_resume_docx
from config import TEMPLATE

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("Missing SERPAPI_API_KEY environment variable")

def search_linkedin_jobs(query):
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "location": "Canada", 
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs = results.get("jobs_results", [])

    formatted_jobs = []

    for job in jobs:
        title = job.get("title", "N/A")
        company = job.get("company_name", "N/A")
        location = job.get("location", "N/A")
        description = job.get("description", "N/A")

        # Get link: prefer apply_options, fallback to share_link
        apply_options = job.get("apply_options", [])
        link = apply_options[0].get("link") if apply_options else job.get("share_link", "")

        summary, tech = generate_updated_resume(title, company, description)
        update_existing_resume_docx(summary, tech, title, company, TEMPLATE)    

        formatted_jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link
        })

    if formatted_jobs:
        today = datetime.now().strftime("%B %d, %Y")
        send_job_template_email("Harmeet", formatted_jobs, today)
    else:
        print("❌ No jobs found for query:", query)

if __name__ == "__main__":
    search_linkedin_jobs(DEFAULT_QUERY)