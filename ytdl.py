import pytube, sys, subprocess, os, ffmpy

def show_progress_bar(stream, _chunk, _file_handle, bytes_remaining):
    curSize = (stream.filesize - bytes_remaining)
    current = (curSize/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    curSizeMB = round(curSize/ (1024)**2)
    fullSize = round(stream.filesize/ (1024)**2)
    sys.stdout.write(' ↳ {}MiB / {}MiB -- {}%\r'.format(curSizeMB, fullSize, percent))
    sys.stdout.flush()

# -- Downloader --
contents = []
print("Enter another YouTube link to work with OR\npress CTRL-Z to work with what you have.".format(len(contents)))
while True:
    try:
        line = input("{} >>> ".format(len(contents)+1))
    except EOFError:
        break
    contents.append(line)

if len(contents) == 0:
    sys.exit()

print("\nWorking with the following links:")
for link in contents:
    print(link)

print("\n-----\n")
for url in contents:
    print("URL: {}".format(url))
    try:
        yt = pytube.YouTube(url)
        print("Title: {}".format(yt.title))
        yt.register_on_progress_callback(show_progress_bar)
        yt.streams.filter(file_extension='mp4').first().download()
    except:
        print("Exception with URL: {}".format(url))
    print("\n")



# -- Converter --
print("\n\n =============\n   CONVERTER\n =============")
typeTuple = (".mp4",
            ".mp4a")
fileList = []
filePath = os.path.dirname(os.path.abspath(__file__))
with os.scandir(filePath) as it:
    for item in it:
        if item.is_file() and item.name.endswith(typeTuple):
            #print(item.name)
            inputPath = "{}\\{}".format(filePath,item.name)
            outString = item.name.rsplit(".", maxsplit=1)
            outputPath = "{}\\Audio\\{}.aac".format(filePath,outString[0])
            fileList.append([inputPath, outputPath])
#print(fileList)
#print("\n\n\n\n\n---\n\n\n\n\n")

for x in fileList:  
    print(" ========")
    inputPath = x[0]
    outputPath = x[1]
    ff = ffmpy.FFmpeg(
        inputs={inputPath: None},
        outputs={outputPath: ["-vn", "-acodec", "copy", "-y"]}
    )
    print(ff.cmd)
    print("\n\n")
    try:
        ff.run()
    except:
        print("\n\n ERROR\nWith: {}\n\n\n".format(inputPath))
        #raise
    else:
        print("\n--- Created: {}\n".format(outputPath))

input("Program complete. Enter anything to close this window.\n> ")
