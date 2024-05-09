import requests
from typing import Dict, Optional
from fastapi import HTTPException

import requests
from typing import Dict, Optional
from fastapi import HTTPException

def parse_job_data(job_data: Dict) -> Dict:
    """
    Parses the JSON data of a job list into a structured dictionary list.

    Args:
    job_data (Dict): The raw job data JSON from the API.

    Returns:
    Dict: A list of dictionary containing structured jobs data.
    """
    try:
        return [{
            "agg_id": job["id"],
            "agg_job_name": job["name"],
            "agg_job_description": job["description"],
            "agg_code": job["code"],
            "agg_status": job["status"],
            "agg_type": job["type"],
            "agg_remote_id": job.get("remote_id"),
            "agg_confidential": job.get("confidential", False),
            "agg_remote_created": job.get("remote_created_at"),
            "agg_remote_updated": job.get("remote_updated_at")
        } for job in job_data["results"]] 
    except KeyError:
        raise HTTPException(status_code=400, detail="Failed to parse job data")


def get_job_from_merge(api_key: str, account_token: str) -> Optional[Dict]:
    """
    Fetches a specific job by ID from the Merge API and returns a parsed job record.
    
    Args:
    api_key (str): API key for the Merge API.
    account_token (str): Account-specific token for the Merge API.
    job_id (str): The ID of the job to retrieve.

    Returns:
    Optional[Dict]: A dictionary containing the job data or None if not found.
    """
    url = f'https://api.merge.dev/api/ats/v1/jobs'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'X-Account-Token': account_token
    }

    response = requests.get(url, headers=headers)
    # print("response", response.json())
    if response.status_code == 200:
        job_data = response.json()
        # print("job_data", job_data)
        job_record = parse_job_data(job_data)
        return job_record
    elif response.status_code == 404:
        return None
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch job from Merge API")
