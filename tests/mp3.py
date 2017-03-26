# -*- coding: utf-8 -*-
# MCat.py

# An MP3 audio file cataloging program

# Written by G.D. Walters

# For Full Circle Magazine

 

from mutagen.mp3 import MP3

import os

from os.path import join,getsize,exists

import sys

import apsw

 

def MakeDataBase():

    # IF the table does not exist, this will create the table. 

    # Otherwise, this will be ignored due to the 'IF NOT EXISTS' clause

    sql = 'CREATE TABLE IF NOT EXISTS mp3 (pkID INTEGER PRIMARY KEY, title TEXT, artist TEXT, album TEXT, bitrate TEXT, '

    sql = sql + 'genre TEXT, playtime TEXT, track INTEGER, year TEXT, filesize TEXT, path TEXT, filename TEXT);'

    cursor.execute(sql)

 

def S2HMS(t):

    # Converts seconds to a string formatted H:mm:ss

    if t > 3600:

        h = int(t/3600)

        r = t-(h*3600)

        m = int(r / 60)

        s = int(r-(m*60))

        return '{0}:{1:02n}:{2:02n}'.format(h,m,s)

    else:

        m = int(t / 60)

        s = int(t-(m*60))

        return '{0}:{1:02n}'.format(m,s)

 

def WalkThePath(musicpath):

    ecntr = 0  # Error Counter

    rcntr = 0  # Folder Counter

    fcntr = 0  # File Counter

    # Open the error log file

    efile = open('errors.log',"w")

    for root, dirs, files in os.walk(musicpath):

        rcntr += 1  # This is the number of folders we have walked

        for file in [f for f in files if f.endswith(".mp3")]:

            fcntr += 1  # This is the number of mp3 files we found

            # Clear the holding variables each pass

            _title=''

            _artist=''

            _album=''

            _genre=''

            _year = ''

            _bitrate=''

            _length=''

            _fsize=''

            _track = 0

            # Combine path and filename to create a single variable.

            fn = join(root,file)  

            try:

                audio = MP3(fn)

                keys = audio.keys()

                for key in keys:

                    if key == 'TDRC':           # Year

                        _year = audio.get(key)

                    elif key == 'TALB':         # Album

                        _album = audio.get(key)

                    elif key == 'TRCK':         # Track

                        try:

                            _trk = audio.get(key)

                            if _trk[0].find("/"):

                                _trk1 = _trk[0]

                                _track=_trk1[_trk1.find("/")+1]

                            elif len(trk[0]) == 0:

                                _track = 0

                            else:

                                _track = _trk[0]

                        except:

                            track = 0

                    elif key == "TPE1":         # Artist

                        _artist = audio.get(key)

                    elif key == "TIT2":         # Song Title

                        _title = audio.get(key)

                    elif key == "TCON":         # Genre

                        _genre = audio.get(key)

                _bitrate = audio.info.bitrate   # Bitrate

                _length = S2HMS(audio.info.length)    # Audio Length

                _fsize = getsize(fn)            # File Size

                # Now write the database

                # This is a different way of doing it from last time.  Works much better.

                sql = 'INSERT INTO mp3 (title,artist,album,genre,year,track,bitrate,playtime,filesize,path,filename) VALUES (?,?,?,?,?,?,?,?,?,?,?)'

                cursor.execute(sql,(str(_title),str(_artist),str(_album),str(_genre),str(_year),int(_track),str(_bitrate),str(_length),str(_fsize),root,file))

            except ValueError:

                ecntr += 1

                efile.writelines('===========================================\n')

                efile.writelines('VALUE ERROR - Filename: %s\n' % fn)

                efile.writelines('Title: %s - Artist: %s - Album: %s\n' %(_title,_artist,_album))

                efile.writelines('Genre: %s - Year: %s - Track: %s\n' % (_genre,_year,_track))

                efile.writelines('bitrate: {0} - length: {1} \n'.format(_bitrate,_length))               

                efile.writelines('===========================================\n')

            except TypeError:

                ecntr += 1

                efile.writelines('===========================================\n')

                efile.writelines('TYPE ERROR - Filename: {0}\n'.format(fn))

                efile.writelines('Title: {0} - Artist: {1} - Album: {2}\n'.format(_title,_artist,_album))

                efile.writelines('Genre: {0} - Year: {1} - Track: {2}\n'.format(_genre,_year,_track))

                efile.writelines('bitrate: {0} - length: {1} \n'.format(_bitrate,_length))

                efile.writelines('===========================================\n')

            except:

                ecntr += 1

                efile.writelines('TYPE ERROR - Filename: {0}\n'.format(fn))

            print fcntr

        # Close the log file

        efile.close

    # Finish Up

    print ("\n")

    print ("Number of errors: {0}").format(ecntr)

    print ("Number of files processed: {0}").format(fcntr)

    print ("Number of folders processed: {0}").format(rcntr)

    # End of WalkThePath 

 

def error(message):

    print >> sys.stderr, str(message)

 

def main():

    global connection

    global cursor

    #-----------------------------------------------------------------------------

    if len(sys.argv) != 2:

        usage()

    else:

        StartFolder = sys.argv[1]

        if not exists(StartFolder): # From os.path

            print('Path {0} does not seem to exist...Exiting app.').format(StartFolder)

            sys.exit(1)

        else:

            print('About to work {0} folder(s):').format(StartFolder)            

        # Create the connection and cursor.

        connection=apsw.Connection("mCat.db3")

        cursor=connection.cursor()

        # Make the database if it doesn't exist...

        MakeDataBase()

        # Do the actual work...

        WalkThePath(StartFolder)

        # Close the cursor and connection...

        cursor.close()

        connection.close()

        # Let us know we are finished...

        print("FINISHED!")

 

def usage():

    message = (

       '=======================================================================\n'

       'mCat - Finds all *.mp3 files in a given folder (and sub-folders),\n'

       '\tread the id3 tags, and write that information to a SQLite database.\n\n'

       'Usage:\n'

       '\t{0} <foldername>\n'

       '\t WHERE <foldername> is the path to your MP3 files.\n\n'

       'Author: Greg Walters\n'

       'For Full Circle Magazine\n'

       '=======================================================================\n'

       ).format(sys.argv[0])

    error(message)

    sys.exit(1)

 

if __name__ == '__main__':

    main()