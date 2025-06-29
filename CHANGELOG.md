# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-01-29

### Recent Changes
- Auto-commit: Save local changes (5ccf87b)
- Fix implementation (e9a659a) 
- Initial commit of iTunes scripts (52272fa)
- Initial repository setup (04cbd04)

### Current State
- Repository contains two Python scripts for iTunes library management:
  - `twardoch_autorate_itunes_tracks_using_audioscrobbler.py` - Automatically rates iTunes tracks based on Audioscrobbler (Last.fm) popularity data
  - `twardoch_exportimport_itunes_ratings_as_popm.py` - Exports/imports iTunes ratings to/from MP3 files using POPM ID3 tags
- Scripts were written in 2006 and use outdated Python patterns and libraries
- Windows support via COM automation, partial Mac OS X support via appscript
- No dependency management, testing, or modern packaging
- Apache License 2.0

### Known Issues
- Scripts may not work with modern iTunes/Music app versions
- Audioscrobbler API endpoints are likely deprecated
- Dependencies on unmaintained libraries (win32com, appscript)
- No Python 3 compatibility guarantees
- No error handling or logging
- Platform-specific code without proper abstraction