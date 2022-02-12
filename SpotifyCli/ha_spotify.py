from spotify_cli import runPlayPlaylistOn
import asyncio

@service
def play_spotify_uri(uri=None, device=None):
    asyncio.run(runPlayPlaylistOn({
        "uri": uri,
        "device": device
    }))