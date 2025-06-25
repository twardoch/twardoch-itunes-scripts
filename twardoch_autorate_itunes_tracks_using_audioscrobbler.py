"""twardoch_autorate_itunes_tracks_using_audioscrobbler.py
Version 1.0
Copyright (c) 2006 by Adam Twardoch <adam[at]twardoch[dot]com>
Licensed under the Apache 2 license.
--
Python application that automatically assigns ratings to iTunes tracks. 
For all artists present in the iTunes library, the application 
connects to Audioscrobbler and acquires the list of the most popular 
tracks for each artist. Based on these top tracks lists, the application
assigns ratings (from * to ****) to the tracks present in the library. 

The current implementation uses Windows COM interface to iTunes so it 
will not work on Mac OS X. It should be possible to rewrite the code
to use ituneslib.py from 
http://svn.subway.python-hosting.com/crackajax/trunk/ituneslib.py
Optionally, it can use the mutagen library from
https://bitbucket.org/lazka/mutagen/
and write the ratings directly into the MP3 file as the POPM 
(popularimeter) ID3 tag. 
"""
import sys
import urllib
import xml.dom.minidom
from xml.dom.minidom import Node

import urllib2

isMutagen = False

import win32com.client

try: 
	import mutagen.id3.ID3
	import mutagen.id3.POPM
	isMutagen = True
except: 
	isMutagen = False

class AudioScrobblerLookup:
	"""AudioScrobblerLookup() | (useHttpProxy as string)
  Class to perform Audioscrobbler queries through http. The optional 
  useHttpProxy parameter takes a http address for a proxy server, 
  e.g. http://proxy.myhost:1080/
METHODS
getArtistTopTracks(artistname as str)
  Connects to Audioscrobbler via http, downloads an XML file that 
  enumerates the top tracks for a given artist name, and returns
  a list with the titles. The order of elements corresponds to the
  order in the Audioscrobbler top tracks list. 
"""
	def __init__(self, useHttpProxy = None ): 
		if useHttpProxy:
			self._setProxyHandler(useHttpProxy)

	def _setProxyHandler(self, proxyurl):
		self.proxy = urllib2.ProxyHandler( {"http":proxyurl} )
		opener = urllib2.build_opener(self.proxy, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler, urllib2.HTTPSHandler, urllib2.FTPHandler)
		urllib2.install_opener(opener)
		
	def getArtistTopTracks(self, artistname): 
		artisttoptracks = []
		try: 
			url = "http://ws.audioscrobbler.com/1.0/artist/%s/toptracks.xml" % (urllib.quote(artistname))
			req = urllib2.Request(url)
			data = urllib2.urlopen(req).read()
			doc = xml.dom.minidom.parseString(data)
			for trackname in doc.getElementsByTagName("name"): 
				trackname.normalize()
				if trackname.hasChildNodes(): 
					try: 
						tracktitle = trackname.firstChild.data.encode("iso-8859-1")
					except: 
						tracktitle = trackname.firstChild.data.encode("utf-8")
					artisttoptracks.append(tracktitle.lower().lstrip().rstrip())
		except: 
			pass
		return artisttoptracks
		
class ArtistTopTracks:
	"""ArtistTopTracks(artistname as str, scrobbler as AudioScrobblerLookup)
  Class to assign ratings to the top tracks list acquired from 
  Audioscrobbler. The first three tracks get the rating ****, 
  the first 33% get the rating ***, the second 33% get ** and 
  the rest gets *. 
"""	
	def __init__(self, name, scrobbler):
		self.name = name
		self.toptracks = {}
		if scrobbler: 
			self.scrobbler = scrobbler
		else: 
			self.scrobbler = AudioScrobblerLookup()
		self.scrobblerdone = False
		
	def _getAudioScrobblerTopTracks(self): 
		toptracks = self.scrobbler.getArtistTopTracks(self.name)
		counttracks = len(toptracks)
		for tracki in range(counttracks): 
			track = toptracks[tracki]
			popm = 0
			if tracki <= 3: 
				popm = 100 # iTunes *****
			elif tracki <= 10: 
				popm = 80 # iTunes ****
			elif tracki <= 0.50 * counttracks: 
				popm = 60 # iTunes ***
			else: 
				popm = 40 # iTunes **
			self.toptracks[track] = popm
		self.scrobblerdone = True
				
	def getTopTracks(self):
		if not self.scrobblerdone: 
			self._getAudioScrobblerTopTracks()
		return self.toptracks
		
class ArtistsTopTracks: 
	"""ArtistsTopTracks(scrobbler as AudioScrobblerLookup)
  High-level class to assign ratings tracks. 
METHODS
getArtistTopTracks(artistname as str)
  High-level class to get top tracks for a given artist name. 
getArtistTrackRating(artistname, tracktitle as str)
  High-level class to get the rating for a given artist name 
  and track. 
"""
	def __init__(self, scrobbler = None):
		self.artists = {}
		if scrobbler: 
			self.scrobbler = scrobbler
		else: 
			self.scrobbler = AudioScrobblerLookup()
	
	def getArtistTopTracks(self, artistname): 
		if not artistname in self.artists: 
			self.artists[artistname] = ArtistTopTracks(artistname, self.scrobbler).getTopTracks()
		return self.artists[artistname]
	
	def getArtistTrackRating(self, artistname, tracktitle): 
		tracks = self.getArtistTopTracks(artistname)
		t = tracktitle.lower().lstrip().rstrip()
		if t in tracks: 
			rating = tracks[t]
		else: 
			rating = 20
		return rating

class iTunesAutoRating: 
	"""iTunesAutoRating(displayprogress as boolean)
  Class to get automatic track ratings from Audioscrobbler
  into the iTunes track library. The current implementation
  uses Windows COM interface to iTunes so it will not work 
  on Mac OS X. It should be possible to rewrite the code
  to use ituneslib.py from 
  http://svn.subway.python-hosting.com/crackajax/trunk/ituneslib.py
  Optionally, it can use the mutagen library and write the ratings
  directly into the MP3 file as the POPM (popularimeter) ID3 tag. 
METHODS
getRatingsForTrack(track as iTunes.Track)
  Get new Audioscrobbler rating for a particular iTunes track, 
  and write the rating into the iTunes library as well as optionally
  write it into the POPM (popularimeter) ID3 tag of the MP3 file. 
getRatingsForAllTracks() | (count as int)
  Get new Audioscrobbler ratings for all iTunes tracks in the library. 
  Optional count parameter evaluates a specific number of tracks 
  starting from the top of the library, rather than all; useful for 
  debugging. 
getRatingsForUnratedTracks() | (count as int)
  Get new Audioscrobbler ratings for iTunes tracks in the library
  that have rating = 0 (zero stars)
findMissingTopTracks(filename as str)
  For each artist found in the iTunes library, output the track 
  names that are not included in iTunes library but are among 
  the first top three tracks on Audioscrobbler. In other words, 
  if the user likes the particular artist, he should get these
  tracks. 
"""
	def __init__(self, displayprogress = True):
		self.iTunesApp = win32com.client.gencache.EnsureDispatch("iTunes.Application")
		self.library = self.iTunesApp.LibraryPlaylist
		self.tracks = self.library.Tracks
		self.track_count = self.tracks.Count
		self.toptracksdb = ArtistsTopTracks()
		self.itunestracks = {}
		self.displayprogress = displayprogress

	def _DisplayProgress(self, i):
		if self.displayprogress: 
			if not float(i) % 100: 
				sys.stdout.write(str(i))
				sys.stdout.flush()
			elif not float(i) % 20: 
				sys.stdout.write(".")
				sys.stdout.flush()

	def _storeiTunesTrack(self, track): 
		if not track.Artist in self.itunestracks: 
			self.itunestracks[track.Artist] = []
		self.itunestracks[track.Artist].append(track.Name.lower().lstrip().rstrip())

	def _storeiTunesTracks(self, c = None): 
		if not c:
			c = self.track_count
		print "  Collecting iTunes tracks..."
		for track_index in range(1, c + 1): 
			self._DisplayProgress(track_index)
			track = self.tracks.Item(track_index)
			self._storeiTunesTrack(track)
	
	def getRatingsForTrack(self, track):
		tags = None
		newRating = self.toptracksdb.getArtistTrackRating(track.Artist, track.Name)
		track.Rating = newRating
		if isMutagen: 
			try: 
				trackfile = win32com.client.CastTo(track,'IITFileOrCDTrack')
				mp3 = mutagen.id3.ID3(trackfile.Location)
				popm = mutagen.id3.POPM(rating = newRating, count = track.PlayedCount, email = "itunesrating@apple.com")
				mp3.add(popm)
				mp3.save()
			except: 
				pass
		return newRating
	
	def getRatingsForAllTracks(self, c = None):
		if not c:
			c = self.track_count
		print "  Getting ratings for tracks..."
		for track_index in range(1, c + 1): 
			self._DisplayProgress(track_index)
			track = self.tracks.Item(track_index)
			self.getRatingsForTrack(track)

	def getRatingsForUnratedTracks(self, c = None):
		if not c:
			c = self.track_count
		sys.stdout.write("  Getting ratings for tracks...\n")
		sys.stdout.flush()
		for track_index in range(1, c + 1): 
			self._DisplayProgress(track_index)
			track = self.tracks.Item(track_index)
			if track.Rating == 0: 
				oldRating = track.Rating
				newRating = self.getRatingsForTrack(track)

	def findMissingTopTracks(self, filename): 
		if not len(self.itunestracks): 
			self._storeiTunesTracks()
		outf = file(filename, "w")
		artists = self.itunestracks.keys()
		artists.sort()
		print "  Analyzing artists..."
		for artist_index in range(len(artists)): 
			self._DisplayProgress(artist_index)
			artist = artists[artist_index]
			toptracks = self.toptracksdb.getArtistTopTracks(artist)
			for track in toptracks: 
				try: 
					if toptracks[track] >= 80: 
						artisttracks = self.itunestracks[artist]
						if not track in artisttracks: 
							outf.write("%s - %s\n" % (artist, track))
				except: 
					pass
		outf.close()

it = iTunesAutoRating()
print "Updating ratings for all/unrated tracks"
#it.getRatingsForAllTracks()
it.getRatingsForUnratedTracks()
print "Finished"
