## Multi-User Fridge Management System

A multi-user Fridge Management system built with Python FastAPI, SQLAlchemy, and PostgreSQL, allowing users to create and manage fridge items.

## Deployed on Render
```bash
https://fastapi_fridgeElf.onrender.com
```

## Features

- User registration and authentication
- Create, read, update, and delete items
- Secure API endpoints with JWT authentication

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Environment Management**: Dotenv

## Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Setup Environment Variables
Create a .env file in the root directory and add the following variables:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_fridgeelf
SECRET_KEY=your_secret_key_here
```

## Running the Application
You can run the application using Uvicorn:
```bash
uvicorn main:app --reload

```

### Prerequisites

Make sure you have the following installed:

- Python 3.7+
- PostgreSQL
- pip

### Clone the Repository

```bash
git clone https://github.com/dc815606/fastapi_fridgeElf.git
cd fastapi_fridgeElf
