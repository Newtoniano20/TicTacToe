import requests
PROFILE = {
    "user": "MOLA",
    "match_id": None,
    "Match": None
}
print(requests.post(url="http://localhost:3000/auth", data=PROFILE).content)