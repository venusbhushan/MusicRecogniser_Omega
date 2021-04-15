import os,zipfile
source = r'C:\Users\KIIT\Desktop\MINOR\NewAudioFinger\zips' + '\\'
target = r'C:\Users\KIIT\Desktop\MINOR\NewAudioFinger\decompressed'+'\\'


def movefiles(source, target):

    print("Started")
    working_directory = ('C:\\Users\\KIIT\\Desktop\\MINOR\\NewAudioFinger\\zips')
    os.chdir(working_directory)
    for file in os.listdir(working_directory):
        if zipfile.is_zipfile(file):  # if it is a zipfile, extract it
            with zipfile.ZipFile(file) as item:  # treat the file as a zip
                item.extractall()  # extract it in the working directory

    for path, dir, files in os.walk(source):
        if files:
            for file in files:
                if file.endswith('.mp3'):
                    if not os.path.isfile(target + file):
                        os.rename(path + '\\' + file, target + file)
                    #os.remove(path)
                        # print(path)

    print("moved and unzipped")

movefiles(source, target)
