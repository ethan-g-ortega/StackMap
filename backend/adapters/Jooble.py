"""
Jooble Connector

Purpose:
--------
Implements a data adapter that talks to the public Greenhouse job board API.
This is one of many potential sources (Lever, Recruitee, Workday, etc.)
that all output `JobPosting` models defined in `core/models.py`.

Design Notes:
-------------
- The connector is intentionally self-contained and stateless.
- It focuses on data access only, not analysis. Single Responsbility Aamir!!
- Returns normalized job postings so the core logic doesn't depend on Jooble. Extendibility!!!!
- Long term: all connectors will share a common interface (IJobSource). We want maintaibnable code to look good on our resume!

"""
import http.client

class Jooble:
    def __init__(self):
        self._host = 'jooble.org'
        self._key = '32a0bea6-7def-4665-8184-992e14b14773'
        self._headers = {"Content-type": "application/json"}

    
    def initiate_connection(self):
        self.connection = http.client.HTTPConnection(self._host)

    def send_request(self, body):
        self.connection.request('POST','/api/' + self._key, body, self._headers)
        return self.connection.getresponse()
    
test = Jooble()

test.initiate_connection()
response = test.send_request('{ "keywords": "Machine Learning Engineer ", "location": "California"}')
        
print(response.status, response.reason)
print(response.read())