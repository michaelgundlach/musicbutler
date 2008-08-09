from mutagen.easyid3 import EasyID3
import os
import speech
import random
import thread
import time

class MusicButler:
    def __init__(self, name):
        self._collection = {}
        self._speechlistener = None
        self._actions = None
        self.name = name

    def findmusic(self, location):
        """
        Scours the given location for all MP3s, and adds them to
        the butler's collection.
        """
        listening = self.islistening()
        self.stoplistening() # so addsong doesn't keep stopping and starting

        for (band, album, song, filename) in ID3Reader(location).read():
            band, album, song = band.strip(), album.strip(), song.strip()
            if band.lower().endswith(', the'):
                band = band[:-5]
            if band.lower().startswith('the '):
                band = band[4:]

            if not band or not album or not song: continue

            self.addsong(band, album, song, filename)

        if listening:
            self.listen()

    def addsong(self, band, album, song, filename):
        def clean(s):
            s = s.lower()
            numbers = ['zero','one','two','three','four','five','six','seven',
                       'eight','nine']
            for (number, word) in enumerate(numbers):
                s = s.replace(str(number), ' %s ' % word)

            return s.replace('/', ' slash ').strip()

        self._collection.setdefault(clean(band), {}).setdefault(
                clean(album), set()).add( (clean(song), filename) )

        if self.islistening(): # update our knowledge
            self.stoplistening()
            self.startlistening()

    def islistening(self):
        return not not self._speechlistener

    def _addaction(self, actiondict, action, commands, strings):
        for command in commands:
            command = command % strings
            actiondict["%s, %s" % (self.name, command)] = action

    def startlistening(self):
        collection = self._collection
        name = self.name
        actions = {}

        # build a list of commands and actions from our collection
        for (band, albums) in collection.items():
            self._addaction(actions, (self._playband, band),
                [ "play some %s, any album",
                  "play some %s",
                  "play %s"
                ], band)

            self._addaction(actions, (self._listalbums, band),
                [ "what albums do I have by %s?",
                  "what albums do I have by the band %s?",
                  "what %s albums do I have?"
                ], band)

            self._addaction(actions, (self._listsongs, band),
                [ "what songs do I have by %s?",
                  "what songs do I have by the band %s?",
                  "what %s songs do I have?"
                ], band)

            # album-specific commands for this band
            for (album, songs) in albums.items():
                self._addaction(actions, (self._playalbum, band, album),
                    [ "play %s by %s",
                      "play the album %s by %s",
                      "play %s by the band %s",
                      "play the album %s by the band %s"
                    ], (album, band))

                self._addaction(actions, (self._playalbum, band, album),
                    [ "play some %s, %s",
                      "play %s: %s"
                    ], (band, album))

                self._addaction(actions, (self._playalbum, band, album),
                    [ "play the album %s",
                      "play %s" ], album)

                # got to 2570
                # song-specific commands for this band and album
                for (song, filename) in songs:
                    self._addaction(actions, (self._playsong, band,album,song),
                        [ "play %s",
                          "play the song %s",
                        ], song)

                    self._addaction(actions, (self._playsong, band,album,song),
                        [ "play %s by %s",
                          "play the song %s by %s",
                          "play %s by the band %s",
                          "play the song %s by the band %s"
                        ], (song, band))

        actions["%s, what bands do i have?" % name] = (self._listbands,)
        actions["%s, what albums do i have?" % name] = (self._listalbums,)
        actions["%s, what songs do i have?" % name] = (self._listsongs,)
        actions["%s, stop playing" % name] = (self._stopthemusic,)
        actions["%s, turn off" % name] = (self._turnoff,)
        actions["%s, are you there?" % name] = (self._ping,)
        actions["%s, help!" % name] = (self._help,)
        actions["%s, more help please" % name] = (self._morehelp,)
        actions["%s, more help" % name] = (self._morehelp,)
        actions["What's your name?"] = (self._sayname,)

        if self.islistening():
            self.stoplistening()

        self._actions = actions
        self._speechlistener = speech.listenfor(
                #[x for x in actions.keys() if not x.strip().endswith('play')], self._respond_to_command)
                actions.keys(), self._respond_to_command)
        self.say("Your selection?")

    def stoplistening(self):
        if self.islistening():
            self._speechlistener.stoplistening()
        self._speechlistener = None

    def say(self, phrase):
        print phrase
        print
        speech.say(phrase)

    def _respond_to_command(self, phrase, listener):
        if phrase not in self._actions:
            # TODO: is this the right behavior?
            self.say("I don't know the phrase. '%s'" % phrase)
            return
        command = self._actions[phrase]
        function = command[0]
        args = command[1:]
        function(*args)

    def _sayname(self):
        self.say("My name is %s.  Always say my name "
                 "first to get my attention." % self.name)

    def _help(self):
        message = """
        Always say my name, %s, first.
        You can ask me what bands or albums you have,
        or you can say, %s, play the album pet sounds by beach boys.
        Or, just say, %s, play some beach boys.
        Say, %s stop playing, to stop the music.
        Say, %s more help please, if you really need to.
        """ % ((self.name,) * 5)
        self.say(message)

    def _morehelp(self):
        message = """
        Always say my name, %s, first.
        You can say, play some beach boys, any album.
        Or, play the album pet sounds by beach boys.
        Or, stop playing, to stop the music.
        Or, turn off, to turn me off entirely.
        Or, are you there?, to see if I can hear you.
        You can ask, what albums do I have by the beach boys?
        Or, what albums do I have?
        Or, what bands do I have?
        Remember, always say my name, %s, first.
        """ % (self.name, self.name)
        self.say(message)

    def _ping(self):
        self.say("Yes")

    def _playband(self, band):
        collection = self._collection
        if band in collection:
            self._playalbum(band, random.choice(collection[band].keys()))
        else:
            self.say("No such band. %s" % band)

    def _playalbum(self, band, album):
        collection = self._collection
        if band in collection.keys() and album in collection[band]:
            self.say("Playing %s by %s" % (album, band))
        else:
            self.say("Not found")

    def _playsong(self, band, album, song):
        collection = self._collection
        if band in collection and album in collection[band]:
            songs = collection[band][album]
            for (title, filename) in songs:
                if title == song:
                    self.say("Playing %s by %s" % (song, band))
                    print "Hmm hmm hmm %s" % filename
                    return

        self.say("No such song. %s" % song)

    def _stopthemusic(self):
        self.say("Stopped.")

    def _turnoff(self):
        self.say("Goodbye.")
        self.stoplistening()

    def _listthings(self, thingname, things, bandOfChoice=None):
        indexes = range(len(things))
        random.shuffle(indexes)

        if len(things) == 0:
            msg = "You don't have any %ss" % thingname
            if bandOfChoice:
                msg += " by %s" % bandOfChoice
            self.say("%s." % msg)
            return

        if len(things) == 1:
            msg = "You have one %s" % thingname
            if bandOfChoice:
                msg += " by %s" % bandOfChoice
            self.say("%s: %s" % (msg, things[0]))
            return

        if len(things) > 3:
            msg = "Here are 3 %ss out of your %d" % (thingname, len(things))
        else:
            msg = "You have %d %ss" % (len(things), thingname)
        if bandOfChoice:
            msg += " by %s" % bandOfChoice
        msg += ": "

        count = min(3, len(things))
        choices = [ things[indexes[i]] for i in range(count) ]

        while len(choices) > 1:
            choice = choices.pop()
            msg += "%s, " % choice
        msg += "and %s." % choices[0]

        self.say(msg)

    def _listbands(self):
        self._listthings("band", self._collection.keys())

    def _listalbums(self, bandOfChoice=None):
        collection = self._collection
        if bandOfChoice:
            albums = [ album for album in collection[bandOfChoice] ]
        else:
            albums = [ "%s by %s" % (album, band)
                       for band in collection
                       for album in collection[band] ]
        self._listthings("album", albums, bandOfChoice=bandOfChoice)

    def _listsongs(self, bandOfChoice=None):
        collection = self._collection
        if bandOfChoice:
            titles = [ title
                       for (album, songs) in collection[bandOfChoice].items()
                       for (title, filename) in songs ]
        else:
            titles = [ "%s by %s" % (title, band)
                       for band in collection
                       for (album, songs) in collection[band].items()
                       for (title, filename) in songs ]
        self._listthings("song", titles, bandOfChoice=bandOfChoice)

class ID3Reader(object):
    def __init__(self, location):
        self._location = location

    def read(self):
        """
        Read all mp3 tag information in our location.

        Returns a list of (artist, album, title, filename) tuples.
        """
        result = []

        for (dirname, dirs, files) in os.walk(self._location):
            mp3s = [ dirname + '/' + filename for filename in files
                     if filename.lower().endswith('.mp3') ]
            print "Adding %s" % dirname

            for mp3file in mp3s:
                try:
                    data = EasyID3(mp3file)
                except:
                    continue
                if 'album' not in data or 'artist' \
                        not in data or 'title' not in data:
                    continue
                artist, album, title = data['artist'], \
                        data['album'], data['title']

                artist = artist if type(artist) is str else artist[0]
                album = album if type(album) is str else album[0]
                title = title if type(title) is str else title[0]

                result.append((artist, album, title, mp3file))

        return result
