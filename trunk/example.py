
from musicbutler import MusicButler

collection = {'radio head':['o k computer', 'in rainbows'], 'nine inch nails':['the downward spiral', 'perfection'],
              'crosby stills nash and young':['4 disc set', 'deja vu'], 'alison krauss':['atlanta', 'new favorite'],
              'brian wilson':['smile'], 'beach boys':['pet sounds', 'endless summer', "surf's up"],
              'stabbing westward':['stabbing westward']}

jimmy = MusicButler("jimmy")

for (band, albums) in collection.items():
    for album in albums:
        jimmy.addalbum(band, album)

jimmy.listen()
