from supabase import create_client, Client
from fastapi import HTTPException
import os
from typing import Optional, Dict, List
from dotenv import load_dotenv
load_dotenv()
import uuid

from merge_api import get_job_from_merge


# Initialize Supabase client
PUBLIC_SUPABASE_URL = os.getenv("PUBLIC_SUPABASE_URL")
PUBLIC_SUPABASE_ANON_KEY = os.getenv("PUBLIC_SUPABASE_ANON_KEY")
MERGE_API_KEY = os.getenv("MERGE_API_KEY")

supabase: Client = create_client(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY)
auth = supabase.auth


######################## CREATE FUNCTIONS ########################

def create_organization(
    name: str
):
    response = supabase.table("organization").insert({"name": name}).execute()
    if response.data:
        return {"status": "success", "organization": response.data[0]}
    else:
        raise HTTPException(status_code=400, detail="Error creating organization")


def create_user(
    email: str,
    password: str,
    organization_id: int,
    ats_link_id: int
) -> Dict[str, str]:
    # Create the user in Supabase auth
    user_response = auth.sign_up({
        "email": email,
        "password": password,
    })

    # Check for error during signup
    if user_response.user is None:
        raise HTTPException(status_code=400, detail="Error creating user")

    # Get the user ID
    user_id = user_response.user.id

    # Create recruiter record
    recruiter_response = supabase.table("recruiter").insert({
        "user_id": user_id,
        "organization_id": int(organization_id),
        "ats_link_id": ats_link_id
    }).execute()
    
    if recruiter_response.data is None:
        raise HTTPException(status_code=400, detail="Error creating recruiter")
   
    return {"status": "success", "user": user_response.user}


def create_ats_link(
    ats_type: str,
    account_id: str,
    account_token: str,
    organization_id: int,
    agg_type: str = "type1",
):
    response = supabase.table("ats_link").insert({
        "agg_type": agg_type,
        "ats_type": ats_type,
        "account_id": account_id,
        "account_token": account_token,
        "organization_id": organization_id
    }).execute()

    if response.data:
        return {"status": "success", "ats_link": response.data[0]}
    else:
        raise HTTPException(status_code=400, detail="Error creating ATS link")


def create_job(
    job_name: str,
    job_description: str,
    code: str,
    status: str,
    job_type: str,
    organization_id: int,
    agg_remote_id: str = None,
    agg_confidential: bool = False,
    ats_link_id: int = None
) -> Dict[str, str]:
    job_data = {
        "agg_job_name": job_name,
        "agg_job_description": job_description,
        "agg_code": code,
        "agg_status": status,
        "agg_type": job_type,
        "organization_id": organization_id,
        "agg_remote_id": agg_remote_id,
        "agg_confidential": agg_confidential,
        "ats_link_id": ats_link_id
    }

    # Insert the job record into the database
    response = supabase.table("job").insert(job_data).execute()

    if response.data:
        return {"status": "success", "job": response.data[0]}
    else:
        raise HTTPException(status_code=400, detail="Error creating job")
   
   
######################## GET FUNCTIONS ######################## 


def get_user(user_id: str) -> Dict[str, Optional[Dict]]:
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    if response.data:
        return {"status": "success", "user": response.data}
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_ats_link(ats_link_id: int) -> Dict[str, Optional[Dict]]:
    response = supabase.table("ats_link").select("*").eq("id", ats_link_id).single().execute()
    if response.data:
        return {"status": "success", "ats_link": response.data}
    else:
        raise HTTPException(status_code=404, detail="ATS link not found")

def get_organization(organization_id: int) -> Dict[str, Optional[Dict]]:
    response = supabase.table("organization").select("*").eq("id", organization_id).single().execute()
    if response.data:
        return {"status": "success", "organization": response.data}
    else:
        raise HTTPException(status_code=404, detail="Organization not found")

def get_recruiter_from_user(user_id: str) -> Dict[str, Optional[Dict]]:
    user_id = uuid.UUID(user_id)
    response = supabase.table("recruiter").select("*").eq("user_id", user_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    else:
        raise HTTPException(status_code=404, detail="Recruiters not found")
    

def get_job(job_id: str) -> Dict[str, Optional[Dict]]:
    response = supabase.table("job").select("*").eq("agg_id", job_id).single().execute()

    if response.data:
        return {"status": "success", "job": response.data}
    else:
        raise HTTPException(status_code=404, detail="Job not found")


def get_all_jobs_by_ats_link_id(ats_link_id: int) -> Dict[str, Optional[List[Dict]]]:
    response = supabase.table("job").select("*").eq("ats_link_id", ats_link_id).execute()
    if response.data:
        return {"status": "success", "jobs": response.data}
    else:
        raise HTTPException(status_code=404, detail="No jobs found for the specified ATS link ID")


def get_applications_by_job_id(job_id: str) -> Dict[str, Optional[List[Dict]]]:
    # Query to get applications associated with the job_id
    applications_response = supabase.table("application").select("*").eq("agg_job_id", job_id).execute()

    if applications_response.data:
        return {"status": "success", "applications": applications_response.data}
    else:
        raise HTTPException(status_code=404, detail="No applications found for the given job ID")



######################## UPSERT FUNCTIONS ########################  


def upsert_jobs(account_token: str, api_key: str = MERGE_API_KEY, organization_id: int = None, ats_link_id: int = None):
    """
    Upserts job data from the Merge API into the Supabase database.
    """
    job_list = get_job_from_merge(api_key, account_token)
    
    for job in job_list:
        job["organization_id"] = organization_id
        job["ats_link_id"] = ats_link_id
        try:
            supabase.table("job").upsert(job).execute()
        except Exception as e:
            print(f"Error upserting job: {e}")
    
    return {"status": "success"}
            
    
