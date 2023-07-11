FILE_PATH = "Pink_Floyd_DB.txt"

file = open(FILE_PATH, "r")
file_content = file.read()

#Divide the data into dictionaries
albums_dict = {}
songs_dict = {}
list_of_all_data = file_content.split('#')
for i in list_of_all_data:
    if i == '':
        continue
    song_and_more = i.split('*')
    name_album = song_and_more[0]
    name_album, year = name_album.split('::')
    albums_dict[name_album] = {}
    for j in song_and_more:
        if j == song_and_more[0]:
            continue
        song_name, author, l, lyrics = j.split("::")
        albums_dict[name_album][song_name] = [lyrics, l]
        songs_dict[song_name] = [name_album, lyrics, l]

file.close()

def does_album_in_dict(album):
    '''
    The func is checking if the album is in the dict
    :param album: name of album we get from input
    :type album: string
    :return: if the album is the dict
    :rtype: bool
    '''
    if albums_dict.get(album) is None:
        return False
    return True

def does_song_in_dict(song):
    '''
    The func is checking if the song is in the dict
    :param song: name of song we get from input
    :type song: string
    :return: if the song is the dict
    :rtype: bool
    '''
    if songs_dict.get(song) is None:
        return False
    return True

def get_all_albums() -> str:
    '''
    The func returns all the albums that we have in the file
    :return: all albums from the file
    :rtype: str
    '''
    list_of_albums = ''
    for album in albums_dict.keys():
        list_of_albums += album + ', '
    return list_of_albums

def get_all_songs(album_name) -> str:
    '''
    The func returns all the songs from the current album
    :param album_name: name of the album that we want to get all the songs
    :type album_name: string
    :return: all songs in the album
    :rtype: string
    '''
    song_list = ''
    for song in albums_dict[album_name.capitalize()].keys():
        song_list += song + ', '
    return song_list

def get_song_len(song) -> str:
    '''
    The func returns the len of the song
    :param song: name of the query song
    :type song: string
    :return: the length of song
    :rtype: string
    '''
    for song_name,l in songs_dict.items():
        if song_name == song.capitalize():
            return l[2]
        
def get_lyrics(song) -> str:
    '''
    The func returns the lyrics of the song
    :param song: name of the query song
    :type song: string
    :return: lyrics of query song
    :rtype: string
    '''
    for song_name,lyrics in songs_dict.items():
        if song_name == song.capitalize():
            return lyrics[1]
    
def find_album(song) -> str:
    '''
    The func finds from which album the song is
    :param song: name of the query song
    :type song: string
    :return: album
    :rtype: string
    '''
    for song_name,album in songs_dict.items():
        if song_name == song.capitalize():
            return album[0]
        
def find_by_name(word) -> str:
    '''
    The func search in every song name the word(no metter the case) and return the name of the song
    :param word: word to find in the name of the song
    :type word: string
    :return: all song with this word in name
    :rtype: string
    '''
    songs_names = ''
    for song in songs_dict.keys():
        if (word.capitalize() in song) or (word.lower() in song):
            songs_names += song + ', '
    return songs_names

def find_by_lyrics(word) -> str:
    '''
    The func search in every song lyrics the word(no metter the case) and return the name of the song
    :param word: word to find in the lyrics of the song
    :type word: string
    :return: all song with this word in lyrics
    :rtype: string
    '''
    songs_names = ''
    for song,lyrics in songs_dict.items():
        if (word.capitalize() in lyrics[1]) or (word.lower() in lyrics[1]):
            songs_names += song + ', '
    return songs_names