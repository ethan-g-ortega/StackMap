"""
SkillMap – FastAPI Entry Point

Purpose:
--------
This file exposes the HTTP interface for our app. It defines the `/analyze` endpoint
which orchestrates the flow:
    1. Fetch job postings from one or more connectors (starting with Greenhouse)
    2. Run skill extraction and aggregation
    3. Return a JSON report to the client (our frontend)

Design Notes:
-------------
- Keep this layer simple: it shouldnt contain business logic.
- It will later use dependency injection to swap in different sources.
- The goal is to make `app/` the “interface adapter” layer in a clean architecture.
"""
from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/jobs/fetch/")
def fetch_jobs(job_title: str = Query(...), location: str = Query(...)):
    list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_title}&location={location}"
    response = requests.get(list_url)
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li")
    id_list = []
    for job in page_jobs:
        base_card_div = job.find("div", {"class": "base-card"})
        job_id = base_card_div.get("data-entity-urn").split(":")[3]
        id_list.append(job_id)

    job_list = []
    for job_id in id_list:
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        job_response = requests.get(job_url)
        job_soup = BeautifulSoup(job_response.text, "html.parser")

        job_post = {}
        # Try to extract and store the job title
        try:
            job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
        except:
            job_post["job_title"] = None
            
        # Try to extract and store the company name
        try:
            job_post["company_name"] = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
        except:
            job_post["company_name"] = None
            
        # Try to extract and store the time posted
        try:
            job_post["time_posted"] = job_soup.find("span", {"class": "posted-time-ago__text topcard__flavor--metadata"}).text.strip()
        except:
            job_post["time_posted"] = None
            
        # Try to extract and store the number of applicants
        try:
            job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
        except:
            job_post["num_applicants"] = None

        # Try to extract and store the number of applicants
        try:
            job_post["job_info"] = job_soup.find("section", {"class": "core-section-container my-3 description"}).text.strip()
        except:
            job_post["job_info"] = None

        try:
            job_post["job_link"] = job_url
        except:
            job_post["job_link"] = None

        job_list.append(job_post)


        jobs_df = pd.DataFrame(job_list)
    return jobs_df.to_dict(orient="records")
