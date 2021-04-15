import sys
from itertools import zip_longest as izip_longest

import numpy as np
from termcolor import colored

import libs.fingerprint as fingerprint
from libs.config import get_config
from libs.db_sqlite import SqliteDatabase
from libs.reader_microphone import MicrophoneReader

def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
        # print("Stored blob data into: ", filename, "\n")


def align_matches(matches):
    diff_counter = {}
    largest = 0
    largest_count = 0
    song_id = -1

    for tup in matches:
        sid, diff = tup

        if diff not in diff_counter:
            diff_counter[diff] = {}

        if sid not in diff_counter[diff]:
            diff_counter[diff][sid] = 0

        diff_counter[diff][sid] += 1

        if diff_counter[diff][sid] > largest_count:
            largest = diff
            largest_count = diff_counter[diff][sid]
            song_id = sid

    songM = db.get_song_by_id(song_id)
    # genreM= db.get_song_by_id(song_id)
    # artistM=db.get_song_by_id(song_id)

    nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                     fingerprint.DEFAULT_WINDOW_SIZE *
                     fingerprint.DEFAULT_OVERLAP_RATIO, 5)

    return {
        "SONG_ID": song_id,
        "SONG_NAME": songM[1],
        "CONFIDENCE": largest_count,
        "OFFSET": int(largest),
        "OFFSET_SECS": nseconds,
        "GENRE": songM[3],
        "ARTIST": songM[4],
        "ART": songM[5],
        "ALBUM": songM[6],
        "YEAR": songM[7]

    }


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values)
            for values in izip_longest(fillvalue=fillvalue, *args))


def find_matches(samples, Fs=fingerprint.DEFAULT_FS):
    hashes = fingerprint.fingerprint(1, samples, Fs=Fs)
    return return_matches(hashes)


def return_matches(hashes):
    mapper = {}
    for hash, offset in hashes:
        mapper[hash.upper()] = offset
    values = mapper.keys()

    # https://www.sqlite.org/limits.html
    # To prevent excessive memory allocations,
    # the maximum value of a host parameter number is SQLITE_MAX_VARIABLE_NUMBER, which defaults to 999 for SQLites
    for split_values in map(list, grouper(values, 999)):
        # @todo move to db related files
        query = """
    SELECT upper(hash), song_fk, offset
    FROM fingerprints
    WHERE upper(hash) IN (%s)
  """
        query = query % ', '.join('?' * len(split_values))

        x = db.executeAll(query, split_values)

        for hash_code, sid, offset in x:
            # (sid, db_offset - song_sampled_offset)
            if isinstance(offset, bytes):
                # offset come from fingerprint.py and numpy extraction/processing
                offset = np.frombuffer(offset, dtype=int)[0]
            yield sid, offset - mapper[hash_code]


if __name__ == '__main__':
    sys.stdout = open("out.txt", "w")
    config = get_config()

    db = SqliteDatabase()

    seconds = 3

    chunksize = 4096  # 2**12
    channels = 1  # int(config['channels']) # 1=mono, 2=stereo

    record_forever = False
    reader = MicrophoneReader(None)

    reader.start_recording(seconds=seconds,
                           chunksize=chunksize,
                           channels=channels)

    # msg = ' * started recording..'
    # print(colored(msg, attrs=['dark']))

    while True:
        bufferSize = int(reader.rate / reader.chunksize * seconds)

        for i in range(0, bufferSize):
            nums = reader.process_recording()

        if not record_forever:
            break

    # if visualise_plot:
    #     data = reader.get_recorded_data()[0]
    #     visual_plot.show(data)

    reader.stop_recording()

    data = reader.get_recorded_data()

    Fs = fingerprint.DEFAULT_FS
    channel_amount = len(data)

    result = set()
    matches = []

    for channeln, channel in enumerate(data):
        # TODO: Remove prints or change them into optional logging.
        # msg = '   fingerprinting channel %d/%d'
        # print(colored(msg, attrs=['dark']) % (channeln + 1, channel_amount))

        matches.extend(find_matches(channel))

        # msg = '   finished channel %d/%d, got %d hashes'
        # print(colored(msg, attrs=['dark']) % (channeln + 1,
        #                                      channel_amount, len(matches)))

    total_matches_found = len(matches)

    # print('')

    if total_matches_found > 0:
        # msg = ' ** totally found %d hash matches'
        # print(colored(msg, 'green') % total_matches_found)

        song = align_matches(matches)

        msg = ' \n=> Song: %s \n'
        msg += '   Album:%s\n'
        msg += '   Artist: %s\n'
        # msg += '    offset: %d (%d secs)\n'
        # msg += '    confidence: %d\n'
        msg += '   Year: %s\n'
        msg += '   Genre: %s\n'
        msg+='%s\n'

        print(colored(msg, 'green') % (song['SONG_NAME'], song['ALBUM'],
                                       # song['SONG_ID'],
                                       # song['OFFSET'], song['OFFSET_SECS'],
                                       # song['CONFIDENCE'],
                                       song['ARTIST'],
                                       song['YEAR'],
                                       song['GENRE'],
                                       song['SONG_NAME'] + song['ALBUM'] + song['ARTIST'] + song['YEAR']
                                       ))
        photo = song['ART']
        photoPath = "example" + ".jpg"

        writeTofile(photo, photoPath)
        # search = song['SONG_NAME'] +song['ALBUM']+ song['ARTIST']+ song['YEAR']
        # print(search)
        # kit.playonyt(search)
    sys.stdout.close()
