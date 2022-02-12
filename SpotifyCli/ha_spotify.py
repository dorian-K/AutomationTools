from SpotifyCli.spotify_cli import runPlayPlaylistOn
import asyncio
import types

@service
async def play_spotify_uri(uri=None, device=None, sp_dc=None):
    await runPlayPlaylistOn(types.SimpleNamespace({
        "uri": uri,
        "device": device,
        "sp_dc": sp_dc
    }))