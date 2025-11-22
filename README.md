<img src="https://raw.githubusercontent.com/DmDogger/SimpleLinker/main/docs/logo.png" alt="SimpleLinker" width="350"/>



A simple and fast URL shortening service This project is a full-featured web application designed to demonstrate modern web development practices You can check out the live version at [simplelinker.cc](https://simplelinker.cc)


## About This Project

Hey there! I'm excited to share **SimpleLinker**, my personal project for shortening URLs I built it as a complete web application with a clean separation between the backend and frontend The entire app is containerized with Docker, which makes deployment incredibly simple


### What it does
-   Takes a long link
-   Generates a short, unique identifier (slug)
-   Gives you back a short link
-   Redirects to the original URL when someone clicks the short link

## 🧱 Technology Stack

I used the following tech stack to bring this project to life:

### Backend
-   **Python 3.12** is the core of the entire backend
-   **FastAPI** is the modern and fast web framework I chose for building the API
-   **PostgreSQL** serves as a solid relational database for storing all the links
-   **Alembic** helps me manage database migrations smoothly
-   **Uvicorn** is the ASGI server I use to run FastAPI

### Frontend
-   **React** is my choice for crafting the user interface
-   **TypeScript** adds static typing to my JavaScript, making the code more robust
-   **Vite** is a super quick and modern build tool for the frontend
-   **Axios** is what I use for making all the HTTP requests to the backend

### 🧱 Deployment & Infrastructure
-   **Docker & Docker Compose** containerize the whole application The backend, frontend, and database all run as separate but connected services
-   **Nginx** acts as a web server to serve the static frontend files and as a reverse proxy to forward API requests to the backend

## ✨ Future Features
-   Custom links
-   User registration and authentication
-   Personal account with a history of saved links
-   QR code generation

## ⚙️ How to Run

Since the project is fully containerized, getting it up and running is just one command away:

```bash
docker-compose up --build
```

After that, the application will be available locally at `http://localhost:8080`
