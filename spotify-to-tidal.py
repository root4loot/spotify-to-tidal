#!/usr/bin/env python3
"""
spotify-to-tidal.py - Convert Spotify track URL to Tidal track URL
"""

import re
import sys
import json
import urllib.parse
import requests


def validate_spotify_track_url(url):
    """Validate that the provided URL is a valid Spotify track URL format."""
    pattern = r"^https://open\.spotify\.com/track/[a-zA-Z0-9]+"
    return bool(re.match(pattern, url))


def convert_to_tidal(spotify_url):
    """
    Convert a Spotify track URL to its Tidal equivalent.
    
    Args:
        spotify_url (str): A valid Spotify track URL
            
    Returns:
        dict: A dictionary with original URL, Tidal URL, and status information
    """
    result = {
        "spotify_url": spotify_url,
        "tidal_url": None,
        "status": "fail",
        "message": "Track not found"
    }
    
    if not validate_spotify_track_url(spotify_url):
        result["message"] = "Invalid Spotify track URL"
        return result
    

    params = {
        'url': spotify_url,
        'country': 'auto',
        'to': 'tidal'
    }
    lucida_url = "https://lucida.to/?" + urllib.parse.urlencode(params)
    
    try:
        response = requests.get(lucida_url, allow_redirects=False, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        result["status"] = "error"
        result["message"] = "Service unavailable"
        return result
    
    if response.status_code in (301, 302, 303, 307, 308):
        redirect_url = response.headers.get('Location')
        
        parsed_url = urllib.parse.urlparse(redirect_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        if 'failed-to' in query_params:
            return result
        
        if 'url' in query_params and query_params['url'][0].startswith('https://listen.tidal.com/'):
            result["tidal_url"] = query_params['url'][0]
            result["status"] = "success"
            result["message"] = "Track found"
            return result
    
    result["status"] = "error"
    result["message"] = "Service error"
    return result


def main():
    if len(sys.argv) != 2:
        result = {
            "spotify_url": None,
            "tidal_url": None,
            "status": "fail",
            "message": "Missing Spotify URL"
        }
        print(json.dumps(result))
        sys.exit(1)
    
    spotify_url = sys.argv[1]
    result = convert_to_tidal(spotify_url)
    
    print(json.dumps(result))
    
    if result["status"] == "success":
        sys.exit(0)
    elif result["status"] == "error":
        sys.exit(2) 
    else:
        sys.exit(1)  # Track not found or invalid URL


if __name__ == "__main__":
    main()