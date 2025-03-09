Convert Spotify track URL to Tidal track URL

## Requirements

- Python 3.6+
- `requests` library

## Installation

### Using Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

## Usage

### Python 

```bash
python spotify-to-tidal.py "https://open.spotify.com/track/6s803Mds01E3KGc3sIx0kO"
```

#### Example Output (Track Found)

```json
{"spotify_url": "https://open.spotify.com/track/6s803Mds01E3KGc3sIx0kO", "tidal_url": "https://listen.tidal.com/track/397707547", "status": "success", "message": "Track found"}
```

#### Example Output (Track Not Found)

```json
{"spotify_url": "https://open.spotify.com/track/6s803Mds01E3KGc3sIx0k1", "tidal_url": null, "status": "fail", "message": "Track not found"}
```

### Docker

```bash
docker run --rm -it $(docker build -q .) "https://open.spotify.com/track/6s803Mds01E3KGc3sIx0kO"
```

## Exit Codes

- `0`: Success (track found)
- `1`: Fail (track not found or invalid URL)
- `2`: Error (service unavailable or other errors)

## Notes

- Only handles Spotify track URLs (not albums or playlists)
