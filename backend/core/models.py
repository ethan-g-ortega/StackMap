"""
Core Domain Models

Purpose:
--------
Defines the main data structures used across the project.
They represent our "business domain" — job postings, skill statistics,
and report outputs.

Design Notes:
-------------
- Use Pydantic for type safety and validation.
- Other layers import these models, but they dont import FastAPI or adapters.
- This separation keeps the domain independent from frameworks.

"""
