# Osu Match Results Parser
~~0) download link: http://www.mediafire.com/file/77airezait0yvsv/OsuMatchResultsParser-2.0.1-amd64.msi/file
(or run yourself with ```pip install --user --requirement requirements.txt```)~~
~~1) Open installation location and run `main.exe`~~

0) old version is broken, generate interface code by running
`generate_interface_code.bat`  file
1) run main.py after installing dependencies ( ```pip install --user --requirement requirements.txt```)
2) Copy paste beatmap url or multiple urls, separated by "|".

Example: ```https://osu.ppy.sh/community/matches/58998314|https://osu.ppy.sh/community/matches/58995507```

3) Enter a creative `filename`
4) Press `Make Excel` button
5) Wait
6) ???
7) Profit

A `filename`.xlsx file will be created with scores and names of all players sorted from highest to lowest. Useful for qualifier results and such.

Extra information:
Tested on win10 64bit. Made with python 3.7 and PyQt5

