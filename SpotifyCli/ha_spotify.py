from SpotifyCli.spotify_cli import runPlayPlaylistOn
import asyncio

@service
async def play_spotify_uri(uri=None, device=None):
    await runPlayPlaylistOn({
        "uri": uri,
        "device": device
    })