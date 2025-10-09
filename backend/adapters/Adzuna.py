import http.client
import urllib.parse
import json
import requests
from bs4 import BeautifulSoup
import time, random, requests

API_KEY = "9d9dd9228d53dfd477c2e944f83a788f"
APP_ID  = "65e85814"
COUNTRY = "us"

class Adzuna:
    def __init__(self, app_id: str, api_key: str, country: str = COUNTRY):
        self._appId = app_id
        self._key = api_key
        self._country = country
        self._host = "api.adzuna.com"
        self._headers = {"User-Agent": "StackMap/1.0"}  # helpful

        self.connection = http.client.HTTPSConnection(self._host, timeout=20)

    def search(self, what: str, results_per_page: int = 20, where: str = None, page: int = 1):
        params = {
            "app_id": self._appId,
            "app_key": self._key,
            "what": what,
            "results_per_page": results_per_page,
            "content-type": "application/json",  # <-- note: as query param
        }
        if where:
            params["where"] = where

        query = urllib.parse.urlencode(params)
        path = f"/v1/api/jobs/{self._country}/search/1?{query}"

        self.connection.request("GET", path, headers=self._headers)
        resp = self.connection.getresponse()
        data = resp.read()

        # Helpful debug on non-200s
        if resp.status != 200:
            raise RuntimeError(f"Adzuna error {resp.status} {resp.reason}: {data[:300]!r}")

        return json.loads(data.decode("utf-8"))

if __name__ == "__main__":
    client = Adzuna(APP_ID, API_KEY, country="us")
    response = client.search(what="Machine Learning Engineer", results_per_page=1)
    data = response['results'][0]
    # desc = data['description']
    url = data["redirect_url"]
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    })
    time.sleep(random.uniform(0.8, 1.6))  # be gentle
    r = s.get(url, timeout=20, allow_redirects=True)
    if r.status_code == 200 and "Access Denied" not in r.text:
        soup = BeautifulSoup(r.text, "html.parser")
        full_text = soup.get_text(" ", strip=True)
        print(len(full_text))
    else:
        print("Blocked by target site; falling back to short description from API.")
        print(data.get("description", ""))

    # html = requests.get(url, timeout=20).text
    # soup = BeautifulSoup(html, "html.parser")
    # full_text = soup.get_text(" ", strip=True)  # or target the site’s job-content selector
    # print(full_text)
    