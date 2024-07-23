# Lasko Backend

Lasko Backend is the core server component of the Lasko Cloud Printing solution. 
It provides a RESTful API for managing printers, print jobs, and user authentication.

## Overview

This backend service is built with Python 3.11 and serves as the central hub for the Lasko cloud printing ecosystem. 
It handles communication between the web frontend and client agents, manages print jobs, and provides administrative functionalities.

## Features

- RESTful API for printer management and print job control
- WebSocket server for real-time communication with client agents
- User authentication and authorization
- Print job queueing and processing
- Printer status monitoring
- Logging and analytics

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```shell
git clone https://github.com/cedricmenec/lasko-backend.git
cd lasko-backend
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

3. Install dependencies:
```shell
pip install -r requirements.txt
```

## Configuration

1. Copy the example configuration file:
```shell
cp config.example.yml config.yml
```

2. Edit `config.yml` to set up your environment-specific configurations.

## Running the Server

To start the development server:
```shell
python run.py
```

The server will start on `http://localhost:8000` by default.

## API Documentation

API documentation is available at `/docs` when the server is running.

## Testing

Run the test suite with:

```shell
pytest
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
