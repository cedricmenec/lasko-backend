import asyncio
import websockets
import msgpack
import uuid
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
        self.pending_requests: Dict[str, asyncio.Future] = {}

    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """
        Handles the connection and processing of WebSocket messages for a connected client.
        
        This method is called when a new WebSocket connection is established. It associates the connection with an agent ID based on the path of the WebSocket request. It then enters a loop to continuously receive and process messages from the client.
        
        For each message received, it unpacks the message using msgpack, creates an `Instruction` object from the message data, and passes it to the `process_instruction` method to handle the instruction. The response from `process_instruction` is then sent back to the client.
        
        When the connection is closed, the method removes the agent ID from the `active_connections` dictionary.
        """
        # Extract agent_id from the path
        agent_id = path.split('/')[-1]
        
        if not agent_id:
            logger.error("Connection attempt with empty agent_id")
            await websocket.close(1008, "Agent ID is required")
            return

        if agent_id in self.active_connections:
            logger.warning(f"Agent with ID {agent_id} is already connected. Closing old connection.")
            await self.active_connections[agent_id].close(1008, "New connection initiated for this agent ID")


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

                if data["type"] == "response":
                    await self.handle_response(data)
                elif data["type"] == "request":
                    # Handle any requests from the agent (if applicable)
                    pass
    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for agent: {agent_id}")
        finally:
            del self.active_connections[agent_id]

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

    async def send_request(self, agent_id: str, command: str, payload: dict = None):
        if agent_id not in self.active_connections:
            raise ValueError(f"Agent {agent_id} not connected")
        
        request_id = str(uuid.uuid4())
        request = {
            "type": "request",
            "id": request_id,
            "command": command,
            "payload": payload or {}
        }
        
        future = asyncio.Future()
        self.pending_requests[request_id] = future

        await self.active_connections[agent_id].send(msgpack.packb(request))

        try:
            return await asyncio.wait_for(future, timeout=10.0)  # 10 seconds timeout
        except asyncio.TimeoutError:
            del self.pending_requests[request_id]
            raise TimeoutError(f"Request {request_id} from agent {agent_id} timed out ")
        
    async def handle_response(self, response: dict):
        request_id = response["id"]
        if request_id in self.pending_requests:
            future = self.pending_requests.pop(request_id)
            future.set_result(response["payload"])

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