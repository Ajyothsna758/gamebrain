import requests
from django.conf import settings
from django.core.cache import cache

def get_igdb_token():
    token=cache.get("igdb_token")
    if token:
        return token
    
    payload={
        "client_id":settings.IGDB_CLIENT_ID,
        "client_secret": settings.IGDB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    res= requests.post(settings.IGDB_AUTH_URL, data=payload)
    res.raise_for_status()
    
    data= res.json()
    token= data["access_token"]
    cache.set("igdb_token",token, timeout=data["expires_in"])
    return token
    
def get_igdb_data(endpoint, query):
    token= get_igdb_token()
    headers={
        "Client-ID": settings.IGDB_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    } 
    url= f"{settings.IGDB_API_URL}/{endpoint}"
    res= requests.post(url, data=query, headers=headers)
    res.raise_for_status()
    return res.json()   