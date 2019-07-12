import dict_data as data
import pickle

# STILL MUST IMPORT DATA FROM DATABASE #

song_IDs = data.import_dictionaries('int_to_title')


def match(fingerprints, base):
    """
    Compares the recorded fingerprints to fingerprints from songs stored in the database to identify the song.

    Parameters:
    -----------
    fingerprints: List[Tuple[int, int, int]]
    List of fingerprints (freq_0, freq_1, dt) that store the fingerprints from the recorded audio file
    
    base: Dict[Tuple[int, int, int]:List[string, int]]
    Dictionary of fingerprints (freq_0, freq_1, dt) that map to a list of song names and time intervals.
    
    Returns:
    --------
    [string]: Title of the matched song in the form "(song title) by (artist)"
    """
    songs = {}

    database = base

    for song in song_IDs.values():
        songs[song] = 0

    for fp in fingerprints:
        if fp in database:
            for i in range(len(database[fp])):
                songs[database[fp][i]] += 1

    song = max(zip(songs.values(), songs.keys()))

    print(songs)

    return song[1]
