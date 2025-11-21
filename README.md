# SimpleLinker

## Project Overview

SimpleLinker is a modern, high-performance URL shortening service built with FastAPI and PostgreSQL. It allows users to create short, memorable links that redirect to longer URLs, providing a clean and efficient way to manage web addresses.

## Features

*   **FastAPI Backend:** Robust and asynchronous API for handling link creation and redirection.
*   **PostgreSQL Database:** Reliable data storage for links and their metadata.
*   **Docker & Docker Compose:** Easy setup and deployment using containerization.
*   **Alembic Migrations:** Database schema management for seamless updates.
*   **Customizable Slugs:** Generate unique short codes for your links.

## Technologies Used

*   **Backend:** Python 3.12, FastAPI
*   **Database:** PostgreSQL 16
*   **Containerization:** Docker, Docker Compose
*   **Database Migrations:** Alembic
*   **Dependency Management:** pip

## Getting Started (Local Development)

Follow these steps to set up and run SimpleLinker on your local machine using Docker Compose.

### Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Engine and Docker Compose) installed on your system.

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/DmDogger/SimpleLinker.git
cd SimpleLinker
```

### 2. Create `.env` File

Create a `.env` file in the root directory of the project with your database configuration. This file will be used by both the FastAPI application and the PostgreSQL container.

```ini
# .env
DB_HOST=db
DB_PORT=5432
DB_DATABASE=smpledb
DB_USER=simplelinker
DB_PASSWORD=simplelinker
POSTGRES_DB=smpledb
POSTGRES_USER=simplelinker
POSTGRES_PASSWORD=simplelinker
DATABASE_URL=postgresql+asyncpg://simplelinker:simplelinker@db:5432/smpledb
```
**Note:** `DB_HOST` is set to `db` because that's the service name of the PostgreSQL container within the Docker Compose network.

### 3. Build and Run with Docker Compose

Build the Docker images and start the services (FastAPI app and PostgreSQL database) using Docker Compose:

```bash
docker-compose up --build -d
```
*   The `--build` flag ensures that your application image is rebuilt, incorporating any changes in the `Dockerfile` or your code.
*   The `-d` flag runs the services in detached mode (in the background).

### 4. Run Database Migrations

Once the services are running, you need to apply the database migrations to create the necessary tables (e.g., `links` table).

```bash
docker-compose exec app alembic upgrade head
```
This command executes `alembic upgrade head` inside your `app` container, applying all pending migrations to the PostgreSQL database.

### 5. Access the Application

Your SimpleLinker application should now be running and accessible.

*   **API Documentation (Swagger UI):** Open your web browser and navigate to `http://localhost:8000/docs`
*   **Redirection Service:** The main application will handle short link redirections.

### Stopping the Services

To stop and remove the Docker containers, networks, and volumes created by Docker Compose:

```bash
docker-compose down
```

## API Endpoints

The FastAPI application provides the following main endpoints (refer to `/docs` for full details, assuming the router is mounted at a base path like `/` or `/api/v1`):

*   `GET /{slug}`: Redirects to the original URL associated with the given `slug`. This is the core redirection service.
*   `POST /`: Creates a new short link. (The exact path depends on how the router is included in `main.py`, e.g., `/` or `/api/v1/links`).

## License

All Rights Reserved. This code is provided for demonstration and educational purposes only. Unauthorized use, reproduction, or distribution is prohibited.

## Contact

For any questions or inquiries, please contact DmDogger via [GitHub Profile](https://github.com/DmDogger).