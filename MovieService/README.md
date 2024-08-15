# MovieService

MovieService is a microservice built using FastAPI for managing movies in the database. This service provides APIs for adding, retrieving, updating, and deleting movie records. It interacts with a PostgreSQL database to store movie data and is part of a microservices architecture where it communicates with the `CastsService`.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Service](#running-the-service)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12.1 or higher
- Docker & Docker Compose (optional, for containerized deployment)

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/MovieService.git
cd MovieService
````

### 2. Set Up a Python Virtual Environment
It is recommended to create and activate a Python virtual environment to manage dependencies separately from your global Python environment.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
With the virtual environment activated, install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up the PostgreSQL Database
Ensure you have a running PostgreSQL instance. The database tables are created automatically using SQLAlchemy's `metadata.create_all(engine)` in your `main.py` file, and there is no need to manually create the database schema using SQL queries. This automatically ensures that the necessary tables are created in the database when the application starts.


### Environment Variables
The service relies on environment variables for configuration. Create a .env file in the MovieService directory with the following content:

```plaintext
DATABASE_URI=postgresql://movie_db_username:movie_db_password@movie_db/movie_db_dev
CAST_SERVICE_HOST_URL=http://cast_service:8000/api/v1/casts/
```

- DATABASE_URI: The connection string to your PostgreSQL database.
- CAST_SERVICE_HOST_URL: The base URL for the CastsService API.

### Running the Service
1. Running Locally
Ensure your PostgreSQL instance is running and that the DATABASE_URI in your .env file points to it. Then, start the FastAPI server:

``` bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
This command starts the application on http://localhost:8000.

2. Running with Docker
To run the service using Docker, first ensure Docker and Docker Compose are installed. Then use the following command:

```bash
docker-compose up --build
```
This will start both the MovieService and its associated PostgreSQL database in Docker containers.

### Project Structure

```bash
MovieService/
├── app/
│   ├── api/
│   │   ├── movies.py      # FastAPI routes for movie-related operations
│   │   ├── db.py          # Database setup and configuration
│   │   ├── db_manager.py  # Database operations for movies
│   ├── models/            # Pydantic models for request and response validation
├── main.py                # FastAPI application setup
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not included in version control)
```

### Key Files:
- `main.py`: Initializes the FastAPI application and includes the movies API router. It also ensures that database tables are created automatically when the application starts.
- `db.py`: Configures the connection to the PostgreSQL database and defines the database schema.
- `db_manager.py`: Contains functions to interact with the database (e.g., add, fetch, update, delete movies).

### API Documentation
FastAPI automatically generates interactive API documentation. Once the service is running, you can access it at:

- Swagger UI: http://localhost:8000/api/v1/movies/docs
- ReDoc: http://localhost:8000/api/v1/movies/redoc