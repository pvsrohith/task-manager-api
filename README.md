# Task Manager API

A RESTful backend API for managing tasks and projects, built with **FastAPI** and **SQLAlchemy**. A clean example of backend service architecture: layered routing, ORM models, request validation, and token-based auth.

## Features

- Full CRUD for tasks (create, read, update, delete, filter by status/priority)
- Project grouping - tasks belong to projects
- Simple token-based authentication middleware
- SQLite persistence via SQLAlchemy ORM (swappable for Postgres/MySQL)
- Request/response validation with Pydantic schemas
- Auto-generated interactive API docs (Swagger UI via FastAPI)

## Tech Stack

Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn, SQLite

## Project Structure

task-manager-api/
- main.py - FastAPI app, routes, auth middleware
- models.py - SQLAlchemy models (Task, Project)
- schemas.py - Pydantic request/response schemas
- database.py - DB engine/session setup
- requirements.txt

## Getting Started

pip install -r requirements.txt
uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs for interactive API docs.

## API Overview

- GET /tasks - List all tasks (filterable by status/priority)
- POST /tasks - Create a task
- GET /tasks/{id} - Get a single task
- PUT /tasks/{id} - Update a task
- DELETE /tasks/{id} - Delete a task
- POST /projects - Create a project
- GET /projects/{id}/tasks - List tasks in a project

## Roadmap

- Replace token auth with full JWT + refresh tokens
- Add pagination and sorting
- Dockerize for one-command deployment
