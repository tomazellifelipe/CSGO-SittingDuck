# CS:GO Sitting Duck App

**The idea:** cs:go gaming integration sends data to a HTTP, and specificaly it can send data about all the players positions during a match, when in spectator mode (sadly it doesn't let your grab your own position during a match), so with that data I can plot a heatmap showing all of your position during a match and doing so it can help you understand if you are spending too much time in the same place or if you are moving more than you should.

**How:** Python Flask will handle the HTTP part of the process, and a Pandas Dataframe (maybe a sql in the future) will store the position to be ploted in one of the pages created with Flask

- save a file name in (location may change)
```
D:\Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg\gamestate_integration_sittingduck.cfg
```
- install python and all the required libs
- run a cs:go demo
- run the python file
- after the match ended open the http:localhost:5000 (probably will change the port)
- on /statiscs will be a map like de_mirage with your positions on top of it
- for map pictures and infos look at 
```
csgo\resourse\overviews 
```

Using matplotlib set the center of the coordinates system to match the one passed on de_map.txt file, this value will be diferente for each map, so I'll need to grab the map name information