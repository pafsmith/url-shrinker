# Python FastAPI URL Shortener

A high-performance URL shortener API built with FastAPI, SQLAlchemy, and Alembic. This project provides a simple and efficient way to create short links and redirect users to the original URL, with a focus on clean code, modern practices, and asynchronous performance.

### Features

- Create Short Links: Submit any valid URL and receive a unique, 7-character short code.
- Fast Redirection: Near-instant redirection from a short code to the original destination URL.
- Collision Handling: The backend automatically handles hash collisions to guarantee unique codes.
- Duplicate URL Detection: If a URL has already been shortened, the existing short code is returned to prevent duplicate entries.
- Automatic API Documentation: Interactive API documentation is available at ```/docs``` thanks to FastAPI and Swagger UI.

### Tech Stack

- Backend: Python 3.9+
- API Framework: FastAPI
- Database ORM: SQLAlchemy (with asyncio support)
- Database Driver: psycopg (for PostgreSQL)
- Database Migrations: Alembic
- Data Validation: Pydantic
- Configuration: pydantic-settings (for .env management)
- ASGI Server: Uvicorn
- Package Management: uv

### Setup & Installation

Follow these steps to set up the project locally.

#### 1. Clone the Repository

```
git clone <your-repository-url>
cd url-shrinker
```

#### 2. Create a Virtual Environment and Install Dependencies

This project uses ```uv``` for package management.

```
# Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate

# Install all required packages using uv
uv pip install -r requirements.txt

# Or if you don't have a requirements.txt yet
uv add "fastapi" "sqlalchemy[asyncio]" "alembic" "psycopg[binary]" "pydantic-settings" "python-dotenv" "uvicorn[standard]
```

#### 3. Set Up the Environment File


Create a ```.env``` file in the root of the project directory. This file will store your database connection strings.

 
```
# .env


# Asynchronous URL for FastAPI
DATABASE_URL="postgresql+psycopg_async://user:password@host/database_name"

# Synchronous URL for Alembic
SYNC_DATABASE_URL="postgresql+psycopg://user:password@host/database_name"

```


#### 4. Run Database Migrations

With your database server running, apply the database migrations to create the necessary tables. 

```
uv run alembic upgrade head
```


### Running the Application

To start the development server, run the following command from the project root:

```uv run uvicorn app.main:app --reload```


The API will be available at ```http://127.0.0.1:8000```. 

API Usage

You can interact with the API using any HTTP client or by visiting the interactive documentation at ```http://127.0.0.1:8000/docs```.
##### Example: Create a Short Link

Here is an example of how to create a new short link using ```curl```

```
curl -X POST "[http://127.0.0.1:8000/api/links](http://127.0.0.1:8000/api/links)" \
-H "Content-Type: application/json" \
-d '{"original_url": "https://www.example.com/a-very-long-url-to-shorten"}'
```

##### Successful Response:
```
{
  "id": 1,
  "short_code": "xY_z1aB",
  "original_url": "[https://www.example.com/a-very-long-url-to-shorten](https://www.example.com/a-very-long-url-to-shorten)",
  "visit_count": 0
}
```


