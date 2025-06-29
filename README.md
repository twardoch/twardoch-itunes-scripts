# twardoch-itunes-scripts

**twardoch-itunes-scripts** is a collection of Python scripts designed to enhance your iTunes experience by automating track ratings and managing rating data between your iTunes library and your MP3 files. These scripts were originally developed by Adam Twardoch (circa 2006) and are aimed at music enthusiasts and iTunes users looking for more control over their music library.

**Note from the Original Author (paraphrased):** _"I have no idea whether these scripts still work. Feel free to modify them or clean them up, and request a pull merge."_ This highlights the age of the scripts and the potential need for updates for compatibility with modern systems.

## Table of Contents

*   [What do these scripts do and why are they useful?](#what-do-these-scripts-do-and-why-are-they-useful)
    *   [`twardoch_autorate_itunes_tracks_using_audioscrobbler.py`](#twardoch_autorate_itunes_tracks_using_audioscrobblerpy)
    *   [`twardoch_exportimport_itunes_ratings_as_popm.py`](#twardoch_exportimport_itunes_ratings_as_popmpy)
*   [Who are these scripts for?](#who-are-these-scripts-for)
*   [Installation](#installation)
    *   [Prerequisites](#prerequisites)
    *   [Dependencies](#dependencies)
    *   [Important Considerations](#important-considerations)
*   [How to Use the Scripts](#how-to-use-the-scripts)
    *   [`twardoch_autorate_itunes_tracks_using_audioscrobbler.py`](#usage-twardoch_autorate_itunes_tracks_using_audioscrobblerpy)
    *   [`twardoch_exportimport_itunes_ratings_as_popm.py`](#usage-twardoch_exportimport_itunes_ratings_as_popmpy)
*   [Technical Details](#technical-details)
    *   [`twardoch_autorate_itunes_tracks_using_audioscrobbler.py` - Technical](#technical-twardoch_autorate_itunes_tracks_using_audioscrobblerpy)
    *   [`twardoch_exportimport_itunes_ratings_as_popm.py` - Technical](#technical-twardoch_exportimport_itunes_ratings_as_popmpy)
*   [Coding and Contribution Guidelines](#coding-and-contribution-guidelines)
    *   [License](#license)
    *   [Authors and Contributors](#authors-and-contributors)
    *   [Contributing](#contributing)

## What do these scripts do and why are they useful?

This collection includes two main Python scripts:

### <a name="twardoch_autorate_itunes_tracks_using_audioscrobblerpy"></a>`twardoch_autorate_itunes_tracks_using_audioscrobbler.py`

*   **What it does:** Automatically assigns star ratings to tracks in your iTunes library.
*   **How it works:** It identifies artists in your library, queries the Audioscrobbler (now Last.fm) service to find the most popular tracks for each artist, and then applies ratings to your tracks based on this popularity.
*   **Why it's useful:** If you have a large library with many unrated tracks, this script can save you significant time by providing a baseline rating based on general popularity. This can help you discover or rediscover good music within your own collection.

### <a name="twardoch_exportimport_itunes_ratings_as_popmpy"></a>`twardoch_exportimport_itunes_ratings_as_popm.py`

*   **What it does:** This script allows you to synchronize track ratings and play counts between your iTunes library and the metadata embedded within your MP3 files (specifically, the 'POPM' or popularimeter ID3 tag).
*   **Why it's useful:**
    *   **Backup your ratings:** Store your carefully curated iTunes ratings directly in your music files.
    *   **Portability:** If you use other music players that support POPM tags, your ratings can be visible and usable across different software.
    *   **Restore ratings:** If your iTunes library gets corrupted or you move to a new system, you can re-import your ratings from the MP3 files back into iTunes.

## Who are these scripts for?

*   iTunes users who want to automate the process of rating their music.
*   Music collectors who want to ensure their ratings are embedded in their MP3 files for backup and portability.
*   Users comfortable with running Python scripts and potentially troubleshooting minor compatibility issues due to the age of the scripts.

## Installation

These scripts are written in Python and have some external dependencies.

### Prerequisites

1.  **Python:** You'll need a Python interpreter. The scripts were originally written for Python 2.x. Running them with modern Python 3.x might require modifications.
2.  **iTunes:** A working installation of iTunes is required.

### Dependencies

1.  **`mutagen`**: Both scripts can use the `mutagen` library to interact with MP3 ID3 tags.
    ```bash
    pip install mutagen
    ```
2.  **Platform-Specific Dependencies:**
    *   **For Windows Users:**
        *   The scripts use Windows COM automation to interact with iTunes. You'll need the `pywin32` extensions.
            ```bash
            pip install pywin32
            ```
    *   **For macOS Users (for `twardoch_exportimport_itunes_ratings_as_popm.py`):**
        *   This script uses the `appscript` package to communicate with iTunes via AppleScript. The original documentation mentions installing it from `http://appscript.sourceforge.net/`. Availability and installation for modern macOS might require research and may not work out of the box.
            ```bash
            # Example, may need adjustment or alternative
            pip install appscript
            ```

### Important Considerations

*   **Virtual Environments:** It's highly recommended to use a Python virtual environment (e.g., `venv`) to manage dependencies for these scripts, especially if you're adapting them.
*   **Version Compatibility:** Given the age of the scripts (circa 2006), you might encounter issues with the latest versions of Python or the libraries. You may need to find older versions of libraries or update the script code.
*   **Audioscrobbler/Last.fm API:** The `twardoch_autorate_itunes_tracks_using_audioscrobbler.py` script uses a very old Audioscrobbler API endpoint. This will likely require updating to the current Last.fm API, which involves obtaining an API key.

## How to Use the Scripts

The scripts are designed to be run directly from the command line. Their primary behavior is often embedded in the main execution block of each script, which you might need to modify.

### <a name="usage-twardoch_autorate_itunes_tracks_using_audioscrobblerpy"></a>`twardoch_autorate_itunes_tracks_using_audioscrobbler.py`

*   **Functionality:** Assigns ratings to iTunes tracks based on Audioscrobbler/Last.fm data.
*   **Platform:** Primarily Windows-only due to its reliance on Windows COM to interact with iTunes. The script notes `ituneslib.py` as a potential (unimplemented) path for macOS compatibility.
*   **Usage (Command Line):**
    ```bash
    python twardoch_autorate_itunes_tracks_using_audioscrobbler.py
    ```
    By default, the script is configured to update ratings for *unrated* tracks. You can modify the script (lines `it.getRatingsForUnratedTracks()` or `it.getRatingsForAllTracks()`) to rate all tracks.
*   **Programmatic Usage:**
    ```python
    from twardoch_autorate_itunes_tracks_using_audioscrobbler import iTunesAutoRating

    auto_rater = iTunesAutoRating(displayprogress=True)
    # For unrated tracks (default behavior in script)
    auto_rater.getRatingsForUnratedTracks()
    # Or, for ALL tracks (first N if count specified)
    # auto_rater.getRatingsForAllTracks(count=None)
    # To find top tracks missing from your library
    # auto_rater.findMissingTopTracks("missing_top_tracks.txt")
    ```

### <a name="usage-twardoch_exportimport_itunes_ratings_as_popmpy"></a>`twardoch_exportimport_itunes_ratings_as_popm.py`

*   **Functionality:** Exports iTunes track ratings and play counts to POPM tags in MP3 files, or imports them from MP3 files into the iTunes library.
*   **Platform:** Supports both Windows (via COM) and macOS (via AppleScript, if `appscript` works).
*   **Usage (Command Line):**
    The script needs to be edited to choose between exporting and importing.
    ```bash
    python twardoch_exportimport_itunes_ratings_as_popm.py
    ```
    By default, the script is configured to *import* ratings from MP3s to iTunes. To switch to export mode, you need to comment the line `itr.ImportRatingsForAlliTunesTracks()` and uncomment `itr.ExportRatingsForAlliTunesTracks()` at the end of the script.
*   **Programmatic Usage:**
    ```python
    from twardoch_exportimport_itunes_ratings_as_popm import iTunesRatings

    ratings_manager = iTunesRatings(displayprogress=True)
    # To export all iTunes library ratings into MP3 files:
    # ratings_manager.ExportRatingsForAlliTunesTracks()
    # To import ratings from MP3 files into the iTunes library (default in script):
    ratings_manager.ImportRatingsForAlliTunesTracks()
    ```

## Technical Details

This section provides a more in-depth look at how each script functions.

### <a name="technical-twardoch_autorate_itunes_tracks_using_audioscrobblerpy"></a>`twardoch_autorate_itunes_tracks_using_audioscrobbler.py`

*   **Core Functionality:** Iterates artists in iTunes, queries Audioscrobbler API for top tracks, assigns ratings locally, and optionally writes POPM ID3 tags using `mutagen`.
*   **Key Classes:**
    *   `AudioScrobblerLookup`: Handles Audioscrobbler API queries (uses `http://ws.audioscrobbler.com/1.0/artist/.../toptracks.xml` - **likely needs update to modern Last.fm API**). Parses XML track data.
    *   `ArtistTopTracks`: Retrieves top tracks for an artist and assigns ratings based on rank. The ratings are on a 20-100 scale, corresponding to 1-5 iTunes stars:
        *   Top 3 tracks: Rating 100 (iTunes *****)
        *   Tracks 4-10: Rating 80 (iTunes ****)
        *   Tracks up to 50% of list: Rating 60 (iTunes ***)
        *   Remaining tracks in list: Rating 40 (iTunes **)
        *   Tracks not found in Audioscrobbler list receive a base rating of 20 (iTunes *) if processed.
    *   `ArtistsTopTracks`: Manages `ArtistTopTracks` instances, caching results. Provides `getArtistTrackRating` which defaults to rating 20 (1 star) if a track isn't in the fetched popular list.
    *   `iTunesAutoRating`: Main class. Uses `win32com.client` for iTunes on Windows. Methods include `getRatingsForTrack`, `getRatingsForAllTracks`, `getRatingsForUnratedTracks`, `findMissingTopTracks`.
*   **`mutagen` Integration:** If available, writes rating and play count to `POPM:itunesrating@apple.com` tag in MP3s.

### <a name="technical-twardoch_exportimport_itunes_ratings_as_popmpy"></a>`twardoch_exportimport_itunes_ratings_as_popm.py`

*   **Core Functionality:** Synchronizes ratings and play counts between iTunes and MP3 POPM tags.
*   **Key Class:** `iTunesRatings`
    *   **iTunes Interaction:**
        *   Windows: `win32com.client`.
        *   macOS: `appscript` library (may require updates/alternatives).
    *   **POPM Tag Handling (`mutagen`):** Reads/writes `POPM:itunesrating@apple.com` tag. `ReadPOPMFromFile` and `WritePOPMToFile` handle file I/O.
    *   **Synchronization:**
        *   `ImportRatingsForAlliTunesTracks()`: Updates iTunes tracks with rating 0 from POPM tags.
        *   `ExportRatingsForAlliTunesTracks()`: Writes iTunes ratings/play counts to POPM tags.
    *   **Rating Scale:** Uses iTunes 0-100 scale for POPM tag values (POPM itself supports 0-255).
    *   **File Types:** Processes only `.mp3` files.

## Coding and Contribution Guidelines

### License

This project is licensed under the **Apache License, Version 2.0**. See the `LICENSE` file.

### Authors and Contributors

*   Copyright holders: `AUTHORS` file.
*   Contributors: `CONTRIBUTORS` file.

### Contributing

Contributions to modernize, fix, or enhance these scripts are welcome! Given their age, they are prime candidates for updates.

**Potential Areas for Contribution:**

1.  **Modernization:**
    *   **Python 3 Compatibility:** Full Python 3.x support.
    *   **Dependency Updates:** Compatibility with current `mutagen`, `pywin32`. For macOS, investigate `appscript` viability or alternatives like `pyobjc`'s ScriptingBridge.
    *   **Last.fm API Update:** Modify `twardoch_autorate_itunes_tracks_using_audioscrobbler.py` to use the current Last.fm API (requires API key registration).
2.  **Cross-Platform `twardoch_autorate_itunes_tracks_using_audioscrobbler.py`:** Enable macOS support.
3.  **Error Handling & Robustness:** Improve error handling (network, file access, API issues) and add logging.
4.  **User Experience:**
    *   Implement command-line arguments (e.g., `argparse`) to replace script editing for options.
    *   Improve user feedback during execution.
5.  **Code Quality:** Refactor for readability (PEP 8), add comments.
6.  **Testing:** Develop unit/integration tests (mocking iTunes/API interactions).
7.  **Documentation:** Keep this README updated.

**How to Contribute:**

*   Fork the repository.
*   Create a feature/bugfix branch.
*   Make and test your changes thoroughly.
*   Submit a pull request with a clear description.

By contributing, you agree that your contributions will be licensed under the Apache License, Version 2.0.
