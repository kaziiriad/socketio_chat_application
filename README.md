


# Real-Time Chat Application

A scalable real-time chat application built with FastAPI, Socket.IO, and Redis for message broadcasting across multiple instances.

## Features

- Real-time messaging using WebSockets via Socket.IO
- Scalable architecture with Redis as a message broker
- Global chat room for all connected users
- User join/leave notifications
- Docker containerization for easy deployment
- Nginx as a reverse proxy for load balancing

## Technology Stack

- **Backend**: FastAPI (Python)
- **Real-time Communication**: Socket.IO
- **Message Broker**: Redis
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx

## Prerequisites

- Docker and Docker Compose
- Git

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd chat_app
```

### Configuration

The application uses environment variables for configuration. These are set in the `docker-compose.yml` file:

- `PORT`: The port on which the FastAPI application runs (default: 8000)
- `REDIS_HOST`: Hostname for Redis (default: redis)
- `REDIS_PORT`: Port for Redis (default: 6379)

### Running the Application

Build and start the containers:

```bash
docker compose up --build
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost/api

### Development Setup

For local development without Docker:

1. Install Python 3.8+ and Redis
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run Redis locally
5. Start the application:
   ```bash
   cd backend
   uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `GET /`: Root endpoint, returns a welcome message
- `GET /health`: Health check endpoint, verifies Redis connection
- `POST /send_message`: Send a message to all connected clients

## Socket.IO Events

### Client to Server

- `chat_message`: Send a chat message to all users in the global chat room

### Server to Client

- `connected`: Sent when a client connects, includes the session ID
- `message`: Received chat messages or system notifications
- `broadcast`: System messages about user activity (join/leave)

## Project Structure

```
chat_app/
├── backend/
│   ├── main.py           # FastAPI and Socket.IO application
│   ├── Dockerfile        # Docker configuration for backend
│   └── requirements.txt  # Python dependencies
├── docker-compose.yml    # Docker Compose configuration
├── nginx.conf            # Nginx configuration
└── index.html            # Simple frontend for testing
```

## Scaling

The application is designed to scale horizontally. The Redis message broker allows multiple instances of the application to communicate with each other, ensuring that messages are broadcast to all connected clients regardless of which instance they are connected to.

To scale the application, you can use Docker Compose:

```bash
docker compose up --scale chat=3
```

## Troubleshooting

### Redis Connection Issues

If the application cannot connect to Redis, check:
- Redis service is running
- Environment variables are correctly set
- Network connectivity between services

### WebSocket Connection Issues

If clients cannot connect via WebSocket:
- Check browser console for errors
- Verify Nginx is properly configured for WebSocket proxying
- Ensure CORS settings are appropriate for your environment

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.