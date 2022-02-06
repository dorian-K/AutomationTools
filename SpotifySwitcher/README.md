Spotify Switcher
================

This script automates switching between devices in Spotify via Spotify Connect. May break in the future as this relies heavily on undocumented apis.

Getting Started
---------------

Prerequisites: Python 3

Install the requirements: `pip install -r requirements.txt`

Usage: `python.exe spotify_switcher.py <device name> [sp_dc cookie]`

`Device name`: Friendly device name as shown in the Spotify device chooser

`sp_dc cookie`: sp_dc cookie from a logged in session of your spotify user account

Acquiring sp_dc
---------------

1. Install a cookie manager of your choice
2. Visit and log into https://open.spotify.com in your browser
3. Go into your cookie manager and copy the value for the cookie `sp_dc`

You now have everything you need to use this script!

If you don't want to specify the cookie token everytime you use this script, you can also hardcode it in the beginning of the script


Not affiliated with Spotify 