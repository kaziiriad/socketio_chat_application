from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os
import redis
from typing import Dict
os.environ["UVICORN_ACCESS_LOGGING"] = "false"  # Disable access log for security reasons

# Connect to Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

app = FastAPI()

redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, max_connections=5)

redis_client = redis.Redis(connection_pool=redis_pool)
redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"

manager = socketio.RedisManager(url=redis_url)
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # Allow all origins
    logger=True,  # Enable logging for debugging
    engineio_logger=True
)

socket_app = socketio.ASGIApp(sio, app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def check_redis_connection() -> Dict[str, str]:
    try:
        redis_client.ping()
        return {"status": "ok", "message": "Redis connection successful"}
    except redis.exceptions.ConnectionError:
        return {"status": "error", "message": "Failed to connect to Redis"}

@app.get('/health')
async def health():
    redis_status = check_redis_connection()
    return {
        "status": "ok",
        "redis": redis_status,
        "version": "1.0.0"
    }
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup Redis connections on application shutdown."""
    redis_pool.disconnect()

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connected', {'sid': sid}, room=sid)
    await sio.enter_room(sid, 'global_chat')  # Add the client to a global chat room
    await sio.emit('message', {'data': 'Welcome to the chat!'}, room=sid)
    await sio.emit('broadcast', {'data': f'A new user {sid} joined the chat!'}, room='global_chat', skip_sid=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    await sio.emit('broadcast', {'data': f'User {sid} left the chat'}, room='global_chat', skip_sid=sid)
    await sio.leave_room(sid, 'global_chat')  # Remove the client from the global chat room
    print('User disconnected')

@sio.event
async def chat_message(sid, message):
    print(f"Received message from {sid}: {message}")
    await sio.emit('message', {'sid': sid, 'message': message}, room='global_chat')  # Broadcast to all clients in the global chat room

@app.post("/send_message")
async def send_message(message: str):
    await sio.emit('message', {'message': message})  # Emit to all connected clients
    return {"message": "Message sent successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     host = os.getenv("HOST", "127.0.0.1")
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run(socket_app, host=host, port=port)