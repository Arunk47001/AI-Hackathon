# importing the libraries
import os
import requests


def get_search_place(query: str) -> str:
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key="
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text