from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from auth import get_current_user, AuthBearer
from typing import Optional, Dict
import os

from dotenv import load_dotenv
load_dotenv()


# Initialize Supabase client
PUBLIC_SUPABASE_URL = os.getenv("PUBLIC_SUPABASE_URL")
PUBLIC_SUPABASE_ANON_KEY = os.getenv("PUBLIC_SUPABASE_ANON_KEY")

supabase: Client = create_client(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY)
auth = supabase.auth

# Initialize the router
router = APIRouter(
    # dependencies=[Depends(AuthBearer())]
    dependencies=[]
)

from orm import (
    create_user, 
    create_organization, 
    create_ats_link, 
    get_ats_link, 
    get_organization, 
    get_user, 
    get_recruiter_from_user,
    upsert_jobs,
    get_all_jobs_by_ats_link_id,
    get_applications_by_job_id,
)

@router.post("/organization", tags=["Organization"])
def new_organization(
    name: str
):
    var = create_organization(name)
    return var


@router.post("/user", tags=["User"])
def create_user_endoint(
    email: str,
    password: str,
    organization_id: int,
    ats_link_id: int
):
    var = create_user(email, password, organization_id, ats_link_id)
    return var


@router.post("/ats-link", tags=["ATS"])
def create_ats_link_endpoint(
    ats_type: str,
    account_id: str,
    account_token: str,
    organization_id: int,
    agg_type: str = "type1",
):
    var = create_ats_link(ats_type, account_id, account_token, organization_id, agg_type)
    return var

@router.get("/ats-link/{ats_link_id}", tags=["ATS"])
def get_ats_link_endpoint(ats_link_id: int):
    var = get_ats_link(ats_link_id)
    return var

@router.get("/organization/{organization_id}", tags=["Organization"])
def get_organization_endpoint(organization_id: int):
    var = get_organization(organization_id)
    return var

@router.get("/user/{user_id}", tags=["User"])
def get_user_endpoint(user_id: str):
    var = get_user(user_id)
    return var

@router.get("/recruiter/{user_id}", tags=["User"])
def get_recruiter_endpoint(user_id: str):
    var = get_recruiter_from_user(user_id)
    return var

@router.post("/upsert_jobs", tags=["Jobs"])
def upsert_jobs_endpoint(
    account_token: str,
    organization_id: int,
    ats_link_id: int
):
    var = upsert_jobs(
        account_token=account_token, 
        organization_id=organization_id, 
        ats_link_id=ats_link_id
    )
    return var


@router.get("/jobs/{ats_link_id}", tags=["Jobs"])
def get_all_jobs_by_ats_link_id_endpoint(ats_link_id: int):
    var = get_all_jobs_by_ats_link_id(ats_link_id)
    return var


@router.get("/jobs", dependencies=[Depends(AuthBearer())], tags=["Jobs"])
def get_all_jobs_by_user_id(user = Depends(get_current_user)):
    print(user)
    recruter = get_recruiter_from_user(user.id)
    print(recruter)
    print(recruter['ats_link_id'])
    jobs = get_all_jobs_by_ats_link_id(recruter['ats_link_id'])
    print(jobs['jobs'][0].keys())
    return jobs
    # return HTTPException(status_code=600, detail="Not implemented")
    
    
@router.get("/jobs/{job_id}/applications", tags=["Applications"])
async def applications_by_job_id(job_id: str):
    try:
        return get_applications_by_job_id(job_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))