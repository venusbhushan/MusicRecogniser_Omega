import os
from hashlib import sha1

import numpy as np
from pydub import AudioSegment
from pydub.utils import audioop


class FileReader:


    def __init__(self, filename):
        # super(FileReader, self).__init__(a)
        self.filename = filename

    # pydub does not support 24-bit wav files, use wavio when this occurs
    def parse_audio(self, limit=None):
        result = None

        songname, extension = os.path.splitext(os.path.basename(self.filename))

        try:
            audiofile = AudioSegment.from_file(self.filename)

            if limit:
                audiofile = audiofile[:limit * 1000]

            data = np.fromstring(audiofile._data, np.int16)

            channels = []
            for chn in range(audiofile.channels):
                channels.append(data[chn::audiofile.channels])

            result = {
                "songname": songname,
                "extension": extension,
                "channels": channels,
                "Fs": audiofile.frame_rate,
                "file_hash": self.parse_file_hash()
            }
        except audioop.error:
            print('audioop.error')
            pass
            # fs, _, audiofile = wavio.readwav(filename)

            # if limit:
            #     audiofile = audiofile[:limit * 1000]

            # audiofile = audiofile.T
            # audiofile = audiofile.astype(np.int16)

            # channels = []
            # for chn in audiofile:
            #     channels.append(chn)
        return result

    def parse_file_hash(self, blocksize=2 ** 20):
        """ Small function to generate a hash to uniquely generate
        a file. Inspired by MD5 version here:
        http://stackoverflow.com/a/1131255/712997

        Works with large files.
        """
        s = sha1()

        with open(self.filename, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                s.update(buf)

        return s.hexdigest().upper()
