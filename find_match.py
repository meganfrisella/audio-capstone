import dict_data as data
import pickle

# STILL MUST IMPORT DATA FROM DATABASE #

song_IDs = data.import_dictionaries('int_to_title')


def match(fingerprints, base):
    """
    Compares the recorded fingerprints to fingerprints from songs stored in the database to identify the song.

    :param fingerprints: a list of tuples that store the fingerprints from the recorded audio file
    :return: a string indicating the matched song in the form '(song title) by (artist)'
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
