from fastapi import APIRouter, Path, Body, HTTPException
from typing import List
from pydantic import BaseModel, HttpUrl
from app.core.websockets.server import websocket_server
from app.core.websockets.instructions import Instruction, InstructionType
import asyncio
import msgpack

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
    """
    List all printers from connected Lasko Agents.
    
    This function sends a GET_PRINTER_LIST instruction to all connected Lasko Agents
    via WebSocket, collects their responses, and returns a consolidated list of printers.
    """
    
    # Get all active connections
    active_connections = websocket_server.active_connections
    
    if not active_connections:
        raise HTTPException(status_code=503, detail="No Lasko Agents are currently connected")
    
    # Process responses
    all_printers = []
    for agent_id in active_connections.keys():
        try:
            response = await websocket_server.send_request(agent_id, "get_printer_list")
            printers = response.get("printers", [])
            all_printers.extend([PrinterBasic(**printer) for printer in printers])
        except TimeoutError:
            print(f"Timeout while requesting printer list from agent {agent_id}")
        except Exception as e:
            print(f"Error requesting printer list from agent {agent_id}: {str(e)}")
    
    if not all_printers:
        raise HTTPException(status_code=404, detail="No printers found")
    
    return all_printers

async def send_and_receive(agent_id: str, connection, instruction: Instruction):
    try:
        await connection.send(msgpack.packb(instruction.to_dict()))
        response = await connection.recv()
        return msgpack.unpackb(response)
    except Exception as e:
        print(f"Error communicating with agent {agent_id}: {str(e)}")
        return None

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