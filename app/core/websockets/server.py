import asyncio
import websockets
import msgpack
import logging
from typing import Dict
from app.core.websockets.instructions import Instruction, InstructionType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketServer:
    """
    The `WebSocketServer` class is responsible for managing WebSocket connections and processing instructions received from connected clients.
    """
    def __init__(self):
        self.active_connections: Dict[str, websockets.WebSocketServerProtocol] = {}

    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """
        Handles the connection and processing of WebSocket messages for a connected client.
        
        This method is called when a new WebSocket connection is established. It associates the connection with an agent ID based on the path of the WebSocket request. It then enters a loop to continuously receive and process messages from the client.
        
        For each message received, it unpacks the message using msgpack, creates an `Instruction` object from the message data, and passes it to the `process_instruction` method to handle the instruction. The response from `process_instruction` is then sent back to the client.
        
        When the connection is closed, the method removes the agent ID from the `active_connections` dictionary.
        """
        agent_id = path.split('/')[-1]
        self.active_connections[agent_id] = websocket
        
        # Log new connection
        logger.info(f"New agent connected: {agent_id}")
        
        try:
            async for message in websocket:
                data = msgpack.unpackb(message)
                
                # Handle ping
                if data.get("type") == "ping":
                    await websocket.send(msgpack.packb({"type": "pong"}))
                    logger.debug(f"Ping received from agent {agent_id}, sent pong")
                    continue
                
                instruction = Instruction(InstructionType(data["type"]), data["payload"])
                response = await self.process_instruction(instruction)
                await websocket.send(msgpack.packb(response))
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for agent: {agent_id}")
        finally:
            del self.active_connections[agent_id]

    async def process_instruction(self, instruction: Instruction) -> dict:
        """
        Process an incoming WebSocket instruction and return a response.
        
        This method is responsible for handling different types of instructions received from connected WebSocket clients. It takes an `Instruction` object as input, which contains the instruction type and payload, and returns a dictionary containing the response data.
        
        The method currently supports the following instruction types:
        - `GET_PRINTER_LIST`: Returns a list of available printers.
        - `GET_PRINTER_STATUS`: Returns the status of the printer.
        - `SUBMIT_PRINT_JOB`: Submits a new print job and returns the job ID.
        - `GET_PRINT_JOB_STATUS`: Returns the status of a print job.
        - `CANCEL_PRINT_JOB`: Cancels a print job and returns a success flag.
        
        If an unknown instruction type is received, the method returns an error response.
        """
        # Implement the logic to process each instruction type
        # This is a placeholder implementation
        if instruction.type == InstructionType.GET_PRINTER_LIST:
            return {"printers": ["printer1", "printer2"]}
        elif instruction.type == InstructionType.GET_PRINTER_STATUS:
            return {"status": "online"}
        elif instruction.type == InstructionType.SUBMIT_PRINT_JOB:
            return {"job_id": "job1"}
        elif instruction.type == InstructionType.GET_PRINT_JOB_STATUS:
            return {"status": "printing"}
        elif instruction.type == InstructionType.CANCEL_PRINT_JOB:
            return {"success": True}
        else:
            return {"error": "Unknown instruction type"}

    async def send_message(self, agent_id: str, message: dict):
        """
        Sends a message to the WebSocket connection associated with the specified agent ID.
        
        Args:
            agent_id (str): The ID of the agent to send the message to.
            message (dict): The message to be sent, which will be serialized using msgpack.
        
        Raises:
            KeyError: If the specified agent ID is not found in the `active_connections` dictionary.
        """
        if agent_id in self.active_connections:
            await self.active_connections[agent_id].send(msgpack.packb(message))

    async def broadcast(self, message: dict):
        """
        Broadcasts a message to all active WebSocket connections.
        
        Args:
            message (dict): The message to be broadcast, which will be serialized using msgpack.
        """
        for connection in self.active_connections.values():
            await connection.send(msgpack.packb(message))

websocket_server = WebSocketServer()

# This function should be called when starting the server
async def start_websocket_server(host: str, port: int):
    server = await websockets.serve(
        websocket_server.handle_connection,
        host,
        port
    )
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()