# SimpleLinker

A simple URL shortener service built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

*   **URL Shortening:** Create short, unique slugs for long URLs.
*   **PostgreSQL Database:** Persistent storage for links using SQLAlchemy.
*   **Alembic Migrations:** Database schema management.
*   **FastAPI:** Modern, fast (high-performance) web framework for building APIs.
*   **Pydantic:** Data validation and settings management.

## Setup

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.13+**
*   **PostgreSQL:** A running PostgreSQL server.
*   **`pip`** (Python package installer)
*   **`venv`** (Python virtual environment tool)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace with your repository URL
    cd SimpleLinker
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3.13 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to generate `requirements.txt` first using `pip freeze > requirements.txt`)*

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root directory and configure your database connection.
    Example `.env` file:
    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_DATABASE=smpledb
    DB_USER=simplelinker
    DB_PASSWORD=simplelinker

    APP_HOST=127.0.0.1
    APP_PORT=8080
    ```
    *Ensure the `DB_USER` and `DB_DATABASE` exist in your PostgreSQL server and the user has appropriate permissions.*

5.  **Database Migrations (Alembic):**
    Initialize and apply database migrations to create the necessary tables.

    *   **Generate an empty base migration (if starting with an empty database):**
        ```bash
        alembic revision -m "empty base"
        ```
    *   **Stamp the database with the empty base:**
        ```bash
        alembic stamp head
        ```
    *   **Autogenerate the initial migration for your models:**
        ```bash
        alembic revision --autogenerate -m "initial"
        ```
    *   **Apply pending migrations to your database:**
        ```bash
        alembic upgrade head
        ```

## Running the Application

To start the FastAPI application:

```bash
uvicorn main:app --reload --port 8080
```

*   The `--reload` flag enables auto-reloading on code changes.
*   You can specify a different port using `--port <your_port>`.
*   The application will be accessible at `http://127.0.0.1:8080` (or your specified host/port).

## API Documentation

The API provides an endpoint for creating short URLs.

### Base URL

`http://127.0.0.1:8080` (or your application's host and port)

### Endpoints

#### `POST /link/`

Creates a new short URL for a given long URL.

*   **Description:** Submits a long URL to the service, which generates a unique short slug and stores the mapping.
*   **Request Body:** `application/json`
    *   **Schema:** `CreateShortLink`
    ```json
    {
      "link": "https://www.example.com/very/long/url/that/needs/shortening"
    }
    ```
    *   **Fields:**
        *   `link` (string, `HttpUrl`): The long URL to be shortened. Must be a valid HTTP or HTTPS URL.
*   **Response:** `201 Created` `application/json`
    *   **Schema:** `ShortLinkResponse`
    ```json
    {
      "link": "https://www.example.com/very/long/url/that/needs/shortening",
      "link_with_slug": "http://127.0.0.1:8080/your_generated_slug"
    }
    ```
    *   **Fields:**
        *   `link` (string, `HttpUrl`): The original long URL.
        *   `link_with_slug` (string): The generated short URL, including the base URL of your application and the unique slug.

#### `GET /{slug}` (Future Feature / Implied)

*(Note: This endpoint is not yet implemented in the provided router, but it is the logical next step for a URL shortener. It would redirect the user to the original long URL associated with the given slug.)*

## Testing

To run the unit tests for the project:

```bash
PYTHONPATH=. pytest
```

This will execute tests for the repository and service layers.
