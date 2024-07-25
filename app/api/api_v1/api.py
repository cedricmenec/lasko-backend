from fastapi import APIRouter, Path, Body, HTTPException
from typing import List
from pydantic import BaseModel, HttpUrl

"""
Defines the main FastAPI router for the API version 1 endpoints.
"""
api_router = APIRouter()


class PrinterBasic(BaseModel):
    """
    Represents a basic printer model, including its ID, name, and status.
    """
    id: str
    name: str
    status: str

class PrinterDetailed(PrinterBasic):
    """
    Represents a detailed printer model, including its capabilities and available drivers.
    
    Extends the `PrinterBasic` model with additional fields:
    
    - `capabilities`: A dictionary representing the printer's capabilities, such as supported media types, print resolutions, etc.
    - `drivers`: A list of strings representing the available printer drivers.
    """
    capabilities: dict
    drivers: List[str]

class PrintJobSubmission(BaseModel):
    """
    Represents a print job submission, including the printer ID, the URL of the document to print, and optional print options.
    
    :param printerId: The ID of the printer to use for the print job.
    :param documentUrl: The URL of the document to print.
    :param options: An optional dictionary of print options, such as paper size, orientation, etc.
    """
    printerId: str
    documentUrl: HttpUrl
    options: dict = None

class PrintJobResponse(BaseModel):
    """
    Represents the response for a submitted print job, including the job ID and the status of the print job.
    
    :param jobId: The unique identifier for the print job.
    :param status: The current status of the print job, such as "queued", "in progress", or "completed".
    """
    jobId: str
    status: str

class PrintJobStatus(BaseModel):
    """
    Represents the status of a print job, including the job ID, the current status, and an optional error message.
    
    :param jobId: The unique identifier for the print job.
    :param status: The current status of the print job, such as "queued", "in progress", "completed", or "failed".
    :param errorMessage: An optional error message if the print job failed.
    """
    jobId: str
    status: str
    errorMessage: str = None

# Routes
@api_router.get("/printers", response_model=List[PrinterBasic])
async def list_printers():
    # Implémentation à faire
    return []

@api_router.get("/printers/{printerId}", response_model=PrinterDetailed)
async def get_printer_details(printerId: str = Path(..., title="The ID of the printer to get")):
    # Implémentation à faire
    raise HTTPException(status_code=404, detail="Printer not found")

@api_router.post("/print-jobs", response_model=PrintJobResponse, status_code=201)
async def submit_print_job(job: PrintJobSubmission = Body(...)):
    # Implémentation à faire
    return {"jobId": "example_job_id", "status": "queued"}

@api_router.get("/print-jobs/{jobId}", response_model=PrintJobStatus)
async def get_print_job_status(jobId: str = Path(..., title="The ID of the print job to get")):
    # Implémentation à faire
    raise HTTPException(status_code=404, detail="Print job not found")