import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen import File as mFile

# path to music files to process
path = "E:\\Muziek"

print("Splitting filenames and writing to tags...")
print("")

for file in os.listdir(path):
    print('.', end='', flush=True)
    path_to_file = os.path.join(path, file)
    skip = False
    # ignore directories and only split mp3
    if not os.path.isdir(path_to_file) and re.search(r'.[mp|MP]3$', file):
        # open a file as an EasyID3 object
        tags = None
        try:
            tags = MP3(path_to_file, ID3=EasyID3)
        except ID3NoHeaderError:
            # if there are no ID3 meta tags yet
            tags = mFile(path_to_file)

            if tags:
                tags.add_tags()
        except:
            print("Something wrong with {}".format(file))
            skip = True

        if not skip:
            # if current the current file has no artist tag
            try:
                artist = tags['artist']
            except KeyError:
                # search for " - " in filename
                match = re.search(r' - ', file)

                if match:
                    # split filename in author and track
                    artist, title = file.rsplit(" - ", 1)
                    # remove extension from title
                    title = title.split(".")[0]

                    tags['title'] = u"{}".format(title)
                    tags['artist'] = u"{}".format(artist)
                    tags.save()

                    print(".")
                    print("[split] {}".format(file.encode("utf-8")))
                    print("into")
                    print("artist: {}".format(artist.encode("utf-8")))
                    print("title: {}".format(title.encode("utf-8")))
                else:
                    print(".")
                    print("ignored: {}".format(file.encode("utf-8")))
        else:
            print("Skipped it.")

print(">>> Done")
