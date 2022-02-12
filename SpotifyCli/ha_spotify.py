from SpotifyCli.spotify_cli import runPlayPlaylistOn
import asyncio

@service
def play_spotify_uri(uri=None, device=None):
    hass.async_add_executor_job(asyncio.run, runPlayPlaylistOn({
        "uri": uri,
        "device": device
    }))