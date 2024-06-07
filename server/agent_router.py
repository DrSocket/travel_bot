from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from auth import get_current_user, AuthBearer
from typing import Optional, Dict
import os

from dotenv import load_dotenv

from agent_service.DashboardAgent.DashboardAgent import DashboardAgent
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

from agent_service.main import (
    createAgency
)
agency = createAgency()

@router.get("/agency", tags=["Agency"])
def new_agency(
    query: str
):
    yield agency.get_completion(query)

