"""
SkillMap – FastAPI Entry Point

Purpose:
--------
This file exposes the HTTP interface for our app. It defines the `/analyze` endpoint
which orchestrates the flow:
    1. Fetch job postings from one or more connectors (starting with Greenhouse)
    2. Run skill extraction and aggregation
    3. Return a JSON report to the client (our frontend)

Design Notes:
-------------
- Keep this layer simple: it shouldnt contain business logic.
- It will later use dependency injection to swap in different sources.
- The goal is to make `app/` the “interface adapter” layer in a clean architecture.
"""
from fastapi import FastAPI

