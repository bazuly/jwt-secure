# JWT Secure API

A secure FastAPI application with JWT authentication, IP-based token blacklisting, and role-based access control.

## Features

- 🔐 JWT-based authentication
- 🛡️ IP-based token blacklisting for enhanced security
- 👥 Role-based access control (PRIVATE, PUBLIC, ADMIN)
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 🔄 Redis for token blacklist storage
- 🐳 Docker support for easy deployment
- 📝 Comprehensive API documentation

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jwt-secure.git
cd jwt-secure
```

2. Create a `.env` file in the root directory with the following content:
```bash
python setup.py
```

3. Start the application and do migrations using Docker Compose:
```bash
docker-compose up --build -d
docker-compose exec web alembic upgread head
docker-compose exec web alembic revision --autogenerate -m "initial"
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Development

### Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

### Running Tests

```bash
docker-compose exec web python app/tests/test_token_blacklist.py
```

## API Endpoints

### Authentication
- `POST /users/register` - Register a new user
- `POST /users/login` - Login and get access token

### Content Management
- `POST /content/create` - Create new content
- `GET /content/get_content/{content_name}` - Get content by name

## Security Features

1. **JWT Authentication**
   - Access tokens expire after configured time
   - Refresh tokens for long-term sessions
   - Secure token storage and validation

2. **IP-Based Token Blacklisting**
   - Tokens are blacklisted when accessed from different IPs
   - Prevents token sharing and unauthorized access

3. **Role-Based Access Control**
   - Three access levels: PRIVATE, PUBLIC, ADMIN
   - Content visibility based on user roles
   - Secure endpoint access control

## Project Structure

```
jwt-secure/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── exceptions.py        # Custom exception handlers
│   ├── users/
│   │   └── user_profile/    # User-related models and handlers
│   └── content/            # Content-related models and handlers
├── tests/                  # Test files
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables
```