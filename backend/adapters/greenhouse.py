"""
Greenhouse Connector

Purpose:
--------
Implements a data adapter that talks to the public Greenhouse job board API.
This is one of many potential sources (Lever, Recruitee, Workday, etc.)
that all output `JobPosting` models defined in `core/models.py`.

Design Notes:
-------------
- The connector is intentionally self-contained and stateless.
- It focuses on data access only, not analysis. Single Responsbility Aamir!!
- Returns normalized job postings so the core logic doesn't depend on Greenhouse. Extendibility!!!!
- Long term: all connectors will share a common interface (IJobSource). We want maintaibnable code to look good on our resume!

"""
