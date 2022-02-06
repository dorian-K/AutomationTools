import sys
from requests import post, get, put
import asyncio
import json
from websockets import connect

###########################
# insert your sp_dc cookie here
sp_dc = "your cookie goes here!"
###########################

# feel free to re-generate this number, it's just a random 40-character hex string
myDeviceId = "a08ad7ab697dcbc67f2f7cc6c48f0ddd55cebd3e"
# replace with your local urls
dealer = "gew1-dealer.spotify.com"
spclient = "gew1-spclient.spotify.com"

###########################

def grabAccessToken(sp_dc): 
    endpoint = "https://open.spotify.com/"
    cookies = {
        "sp_dc": sp_dc
    }
    r = get(endpoint, cookies=cookies)

    start = r.text.find('"accessToken":"')
    if start == -1:
        raise ValueError("no access token")

    acc = r.text[start+15:]
    end = acc.find('","accessTokenExpirationTimestampM')

    if end == -1:
        raise ValueError("no access token")
    acc = acc[:end]

    print("access token acquired")
    return acc

async def withConnectionId(accessToken, callback):
    # connect to the websocket via the access token and wait for the connection id
    async with connect("wss://"+dealer+"/?access_token="+accessToken) as ws:
        rec = await ws.recv()
        
        parsed = json.loads(rec)

        conId = parsed['headers']['Spotify-Connection-Id']
        print("connection id acquired")
        callback(accessToken, conId)

        # time.sleep(5)
        return conId
    raise ValueError("no connection id")

def transferDevice(accessToken, fromD, to):
    headers = {
        "Authorization": "Bearer "+accessToken,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    }
    obj = {
        "transfer_options": {
            "restore_paused": "restore"
        }
    }
    payload = json.dumps(obj)
    x = post("https://"+spclient+"/connect-state/v1/connect/transfer/from/"+fromD+"/to/"+to, payload, headers=headers)

    print(x.status_code)

def registerDevice(accessToken, connectionId):
    headers = {
        "Authorization": "Bearer "+accessToken,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    }
    obj = {
        "client_version": "harmony:4.22.0-57290db",
        "connection_id": connectionId,
        "outro_endcontent_snooping": False,
        "volume": 65535,
        "device": {
            "brand": "spotify",
            "capabilities": {
                "audio_podcasts": False,
                "change_volume": False,
                "disable_connect": True,
                "enable_play_token": False,
                "supports_file_media_type": False,
                "video_playback": False,
                "manifest_formats": [],
                "play_token_lost_behavior": "pause"
            },
            "device_id": myDeviceId,
            "device_type": "computer",
            "is_group": False,
            "metadata": {},
            "model": "web_player",
            "name": "Python Audio Switcher",
            "platform_identifier": "web_player windows 10;chrome 97.0.4692.99;desktop"
        }
    }
    payload = json.dumps(obj)
    x = post("https://"+spclient+"/track-playback/v1/devices", payload, headers=headers)

    print(x.status_code)

def listAllDevices(accessToken, connectionId):
    headers = {
        "Authorization": "Bearer "+accessToken,
        "content-type": "application/json",
        "x-spotify-connection-id": connectionId
    }
    obj = {
        "member_type": "CONNECT_STATE",
        "device": {
            "device_info": {
                "capabilities": {
                    "can_be_player": True,
                    "hidden": True,
                }
            }
        }
    }
    payload = json.dumps(obj)
    x = put("https://"+spclient+"/connect-state/v1/devices/hobs_"+myDeviceId, payload, headers=headers)
    
    print(x.status_code)
    re = json.loads(x.text)

    return re

def doWork(targetDevice):

    def cb(accessToken, connectionId):
        registerDevice(accessToken, connectionId)
        devs = listAllDevices(accessToken, connectionId)
        active = devs["active_device_id"]
        print("Active device:", active)

        allDevices = devs["devices"]
        targetDeviceActivated = False
        for dev in allDevices.keys():
            d = allDevices[dev]
            print("Device:", d["name"])
            if targetDeviceActivated:
                continue # also print all other devices
            if dev == active:
                print("^^^^^^ active device")
            if d["name"] == targetDevice:
                if dev == active:
                    print("Target device is already active!")
                    targetDeviceActivated = True
                    continue
                transferDevice(accessToken, active, dev)
                targetDeviceActivated = True
                
        if targetDeviceActivated == False:
            print("Target device not found!!!")
        
    return cb

async def run():
    global sp_dc

    if len(sys.argv) < 2:
        print("Usage: <target device name> [sp_dc]")
        return
    if len(sp_dc) < 25 and len(sys.argv) < 3:
        print("sp_dc is not set! Read the manual before using this program!")
        return
    
    if len(sys.argv) >= 3:
        sp_dc = sys.argv[2]

    target = sys.argv[1]

    print("Retrieving token...")
    tok = grabAccessToken(sp_dc)
    await withConnectionId(tok, doWork(target))

if __name__ == "__main__":
    asyncio.run(run())
