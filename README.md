twardoch-itunes-scripts
=======================
**twardoch-itunes-scripts** is a small collection of iTunes/MP3-related scripts that I wrote in Python some years ago. Specifically: 

* **twardoch_autorate_itunes_tracks_using_audioscrobbler.py** — Python application that automatically assigns ratings to iTunes tracks. For all artists present in the iTunes library, the application connects to Audioscrobbler and acquires the list of the most popular tracks for each artist. Based on these top tracks lists, the application assigns ratings (from one to four stars) to the tracks present in the library. 
* **twardoch_exportimport_itunes_ratings_as_popm.py** — Python application that converts between track ratings stored in the iTunes library and those embedded inside of an MP3 file (as the 'POPM' popularimeter tag.) It also stores the played count field in the 'POPM' ID3 tag. 

**Note:** I have no idea whether these scripts still work. Feel free to modify them or clean them up, and request a pull merge. 

Software License
----------------
Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
