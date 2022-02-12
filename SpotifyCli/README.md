Spotify CLI
===========

This script automates Spotify via the command line. May break in the future as this relies heavily on undocumented apis.

Getting Started
---------------

Prerequisites: Python 3

Install the requirements: `pip install -r requirements.txt`

Usage: `python.exe spotify_cli.py -h`

To use spotify_cli, you need to acquire your sp_dc token, which you can supply via the `--sp_dc` argument, hardcode in the script or inside a file named `sp_dc.password`

Acquiring sp_dc
---------------

1. Install a cookie manager of your choice
2. Visit and log into https://open.spotify.com in your browser
3. Go into your cookie manager and copy the value for the cookie `sp_dc`

You now have everything you need to use this script!

If you don't want to specify the cookie token everytime you use this script, you can also hardcode it in the beginning of the script

Use cases
=========

Switch to a device named "Bedroom":

`python.exe spotify_cli.py switch Bedroom`

Play the track [Mr. Roboto](https://open.spotify.com/track/7C0rG4oWO7VeZcffyW1sK9) on the device "Kitchen":

`python.exe spotify_cli.py playPlaylistOn Kitchen spotify:track:7C0rG4oWO7VeZcffyW1sK9`

Not affiliated with Spotify 