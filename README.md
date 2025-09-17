# High-Performance URL Shortener API

A high-performance URL shortener API built with FastAPI, SQLAlchemy, and Alembic. This project provides a simple and efficient way to create short links and redirect users to the original URL, with a focus on clean code, modern practices, and asynchronous performance.

Live Demo URL: [https://shrink.psmithdev.com/docs]

##  Key Features

- Secure User Authentication: JWT-based authentication for user registration and login.
    
- Scoped Link Management: Authenticated users can create, manage, and view analytics for their own links.
    
- Asynchronous Click Tracking: Redirects are instant. Click data is processed in the background by a Dramatiq worker, ensuring a non-blocking user experience.
    
- High-Performance Caching: Frequently accessed links are cached in Redis to minimize database latency and provide lightning-fast redirects.
    
- Detailed Analytics: A secure endpoint provides aggregated click data for each link, including total clicks and a time-series breakdown.
    
- Robust Database Management: Uses SQLAlchemy for object-relational mapping and Alembic for safe, repeatable database migrations.
    
- Fully Containerized: The entire application stack (API, worker, PostgreSQL, Redis) is managed with Docker and Docker Compose for easy and consistent local development.
    
- CI/CD Pipeline: Includes a GitHub Actions workflow for automated code linting to ensure code quality.
    

## Architecture Diagram

This project follows a modern, decoupled architecture suitable for scalable web services.

## Tech Stack

### Backend

- Framework: FastAPI
- ORM: SQLAlchemy
- Database Migrations: Alembic
- Data Validation: Pydantic
- Background Tasks: Dramatiq
- Authentication: python-jose for JWTs, passlib for password hashing

### Database & Cache

- Primary Database: PostgreSQL
- Cache & Message Broker: Redis

### DevOps & Tools
 
- Containerisation: Docker & Docker Compose
- CI/CD: GitHub Actions
- Code Style: Ruff

  
## Getting Started

### Prerequisites

- Git
- Docker and Docker Compose

### Local Development Setup

1. Clone the repository:  

```git clone git@github.com:pafsmith/url-shrinker.git  
cd url-shrinker
```   

2.  Create your environment file:  
    Copy the example environment file and fill in the details. The default values are configured to work with the docker-compose.yml setup.  
    ```cp .env.example .env  ```
    
3. Build and launch the services:  
    This command will build the Docker image for the application and start the web, worker, PostgreSQL, and Redis containers.  
    ```docker-compose up --build ``` 
      
4. Run database migrations:  
    In a new terminal window, execute the Alembic migrations inside the running web container to set up your database tables.  
    ```docker-compose exec web alembic upgrade head```  
      
5. Access the application:
	- The API will be running at http://localhost:8000.
	- Interactive API documentation (Swagger UI) is available at http://localhost:8000/docs.
    

## API Endpoints

### Authentication

| Method | Endpoint           | Description                       | Auth Required |
| ------ | ------------------ | --------------------------------- | ------------- |
| POST   | /api/auth/register | Create a new user account.        | No            |
| POST   | /api/auth/login    | Log in to get a JWT access token. | No            |

### Links

| Method | Endpoint                          | Description                                       | Auth Required |
| ------ | --------------------------------- | ------------------------------------------------- | ------------- |
| POST   | /api/links                        | Create a new shortened link for the current user. | Yes           |
| GET    | /{short_code}                     | Redirect to the original URL.                     | No            |
| GET    | /api/links/{short_code}/analytics | Get detailed click analytics for a specific link. | Yes           |

## Deployment

This application is designed for container-based hosting platforms like Render or Railway.

1. Services: You will need to provision a PostgreSQL database and a Redis instance on your hosting provider.
    
2. Web Service: Deploy the Dockerfile. The start command will be the default CMD instruction (gunicorn ...).
    
3. Worker Service: Deploy a second service from the same Dockerfile but override the start command to ```dramatiq -p 2 app.tasks```.
    
4. Environment Variables: All variables from the .env file must be configured in the environment settings for both the web and worker services, using the connection URLs provided by your host.
    
5. Migrations: Run the ```alembic upgrade head``` command in a one-off job or shell on your provider to initialise the production database.

## License

This project is licensed under the MIT License.