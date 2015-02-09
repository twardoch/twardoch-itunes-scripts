"""twardoch_exportimport_itunes_ratings_as_popm.py
Version 1.01
Copyright (c) 2006 by Adam Twardoch <adam[at]twardoch[dot]com>
Licensed under the Apache 2 license.
--
Python application that converts between track ratings 
stored in the iTunes library and those embedded inside of an MP3 file
(as the 'POPM' popularimeter tag.) It also stores the played count
field in the 'POPM' ID3 tag. 

Example use:

itr = iTunesRatings()
# Export all iTunes library ratings into MP3 files:
itr.ExportRatingsForAlliTunesTracks()
# Import ratings from MP3 files into the iTunes library:
itr.ImportRatingsForAlliTunesTracks() 

Notes: 

1. While the POPM tag supports ratings from 0 to 255, the iTunes 
library supports ratings from 0 to 100. This script always uses the iTunes 
rating scale so the values 0-100 are stored in the POPM tag. 
2. The POPM tag requires an e-mail address that identifies the source of 
the rating. This script uses the fantasy address 'itunesrating@apple.com'.
3. The application works on Windows and Mac OS X. On Windows, it uses 
COM automation through the win32all extensions. On Mac, it uses 
AppleScript through the appscript package. It also uses the mutagen 
package for reading and writing ID3 tags. 
"""

import os, os.path, sys

if sys.platform == "darwin": 
	try: 
		import appscript, macfile
	except ImportError: 
		print "On Mac OS X, you need to install appscript from http://appscript.sourceforge.net/"
		raise SystemExit
elif sys.platform == "win32":
	try: 
		import win32com.client
	except ImportError: 
		print "On Windows, you need to install win32all from http://sourceforge.net/projects/pywin32/"
		raise SystemExit
else: 
	print "This script only runs on Mac OS X or Windows"
	raise SystemExit

try: 
	import mutagen.id3
except ImportError: 
	print "You need to install mutagen from https://bitbucket.org/lazka/mutagen/"
	raise SystemExit

class iTunesRatings: 
	def __init__(self, displayprogress = True): 
		if sys.platform == "win32": 
			self.iTunesApp = win32com.client.gencache.EnsureDispatch("iTunes.Application")
			self.iTunesLibrary = self.iTunesApp.LibraryPlaylist
			self.iTunesTracks = self.iTunesLibrary.Tracks
		elif sys.platform == "darwin": 
			self.iTunesApp = appscript.app('iTunes')
			self.iTunesLibrary = self.iTunesApp.sources['Library'].library_playlists['Library']
			self.iTunesTracks = self.iTunesLibrary.file_tracks.get()
		self.POPMemail = "itunesrating@apple.com" # e-mail address used with the POPM tag to store rating
		self.displayprogress = displayprogress

	def _ResetProgress(self, all): 
		self.progresspercentage = 0
		self.progressall = all
		if self.displayprogress: 
			sys.stdout.write("Processing %s tracks... " % (all))
			if sys.platform == "win32":
				sys.stdout.flush()

	def _DisplayProgress(self, current):
		if self.displayprogress: 
			progresspercentage = int(float(current)/self.progressall * 100 + 0.5)
			if progresspercentage > self.progresspercentage: 
				self.progresspercentage = progresspercentage
				if progresspercentage % 10 == 0:
					sys.stdout.write("#")
					if sys.platform == "win32":
						sys.stdout.flush()

	def ReadPOPMFromFile(self, path): 
		mp3 = None
		if not os.path.splitext(path)[1].lower() == ".mp3": 
			return (0, 0)
		if not os.path.exists(path): 
			return (0, 0)
		try: 
			mp3 = mutagen.id3.ID3(path)
		except: 
			return (0, 0)
		if not mp3: 
			return (0, 0)
		if not mp3.has_key("POPM:%s" % (self.POPMemail)): 
			return (0, 0)
		return (mp3["POPM:%s" % (self.POPMemail)].rating, mp3["POPM:%s" % (self.POPMemail)].count)

	def WritePOPMToFile(self, path, trackrating, playedcount):
		if not os.path.splitext(path)[1].lower() == ".mp3": 
			return False
		if not os.path.exists(path): 
			return False
		try: 
			mp3 = mutagen.id3.ID3(path)
			mp3.add(mutagen.id3.POPM(rating = trackrating, count = playedcount, email = self.POPMemail))
			mp3.save()
			return True
		except: 
			return False

	def ReadPOPMForiTunesTrack(self, track): 
		try: 
			if sys.platform == "win32": 
				trackfile = win32com.client.CastTo(track,'IITFileOrCDTrack')
				if not trackfile.Location: 
					return False
				if track.Rating == 0: 
					track.Rating = self.ReadPOPMFromFile(trackfile.Location)[0]
			elif sys.platform == "darwin": 
				trackfile = track.location.get()
				if trackfile == appscript.k.MissingValue:
					return False
				rating = track.rating.get()
				if rating == 0: 
					track.rating.set(self.ReadPOPMFromFile(trackfile.path)[0])
			return True
		except: 
			return False

	def WritePOPMForiTunesTrack(self, track):
		try: 
			if sys.platform == "win32": 
				trackfile = win32com.client.CastTo(track,'IITFileOrCDTrack')
				if not trackfile.Location: 
					return False
				return self.WritePOPMToFile(trackfile.Location, track.Rating, track.PlayedCount)
			elif sys.platform == "darwin": 
				trackfile = track.location.get()
				if trackfile == appscript.k.MissingValue:
					return False
				return self.WritePOPMToFile(trackfile.path, track.rating.get(), track.played_count.get())
		except: 
			return False

	def ImportRatingsForAlliTunesTracks(self): 
		print "Importing ratings from MP3 files into the iTunes library..."
		if sys.platform == "win32": 
			track_count = self.iTunesTracks.Count
		elif sys.platform == "darwin": 
			track_count = len(self.iTunesTracks)
		self._ResetProgress(track_count)
		for track_index in range(track_count): 
			self._DisplayProgress(track_index)
			if sys.platform == "win32": 
				track = self.iTunesTracks.Item(track_index + 1)
			elif sys.platform == "darwin": 
				track = self.iTunesTracks[track_index]
			self.ReadPOPMForiTunesTrack(track)

	def ExportRatingsForAlliTunesTracks(self): 
		print "Exporting iTunes library ratings into MP3 files..."
		if sys.platform == "win32": 
			track_count = self.iTunesTracks.Count
		elif sys.platform == "darwin": 
			track_count = len(self.iTunesTracks)
		self._ResetProgress(track_count)
		for track_index in range(track_count): 
			self._DisplayProgress(track_index)
			if sys.platform == "win32": 
				track = self.iTunesTracks.Item(track_index + 1)
			elif sys.platform == "darwin": 
				track = self.iTunesTracks[track_index]
			self.WritePOPMForiTunesTrack(track)

itr = iTunesRatings()
#itr.ExportRatingsForAlliTunesTracks()
itr.ImportRatingsForAlliTunesTracks()
print " Finished!"
