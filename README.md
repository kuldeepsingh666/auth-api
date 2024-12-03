# Auth API - FastAPI Authentication with RBAC

A reusable FastAPI-based authentication API with role-based access control (RBAC). This API supports user sign-up, login, profile management, JWT-based authentication, and roles such as admin, moderator, and user.

## Features

- User authentication with JWT tokens.
- Role-based access control (RBAC) for admin and other roles.
- Profile management with optional profile picture upload.
- Refresh token support (TODO).
- CRUD operations for user data.
- Secure password storage using bcrypt.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Endpoints](#endpoints)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Notes](#notes)

---

## Prerequisites

Ensure the following tools are installed before setting up the project:

- Python 3.8+
- pip (Python package manager)
- SQLite (for local database) or other relational databases
- Virtual environment (optional but recommended)

---

## Setup

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/kuldeepsingh666/auth-api.git
    cd auth-api
    ```

2. Create and activate a virtual environment:

    - **On macOS/Linux**:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - **On Windows**:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables. Create a `.env` file in the root directory of the project with the following variables:

    ```bash
    SECRET_KEY=your_secret_key
    EXPIRE_MINUTES=30
    ALGORITHM=HS256
    ```

    - **SECRET_KEY**: A secret key used for JWT encoding and decoding. It should be a secure, random string.
    - **EXPIRE_MINUTES**: The expiration time (in minutes) for access tokens.
    - **ALGORITHM**: The algorithm used for JWT signing (usually `HS256`).

    If you're using a different database (other than SQLite), you may need to specify the database URL (e.g., PostgreSQL or MySQL) in the `.env` file.

---

## Configuration

This project uses the following configuration files:

- **`.env`**: Environment variables for sensitive settings such as the secret key and JWT expiration time.
- **`database.py`**: Database connection settings and models. This project uses SQLite by default.

---

## Running the Application

### Development Mode

To start the FastAPI application in development mode, run the following command:

```bash
uvicorn app:app --reload
