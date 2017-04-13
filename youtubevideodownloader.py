import threading
import urllib
from tkinter import *
import youtube_dl
from urllib.request import urlopen
import base64
from tkinter import ttk
from tkinter import filedialog
from time import sleep, time
from math import trunc
from PIL import ImageTk, Image
import os
from threading import Event, Thread


def download2(data, title):
    response = urlopen(data)
    totalsize = int(response.headers['Content-Length'])  # assume correct header
    outputfile = open("video.mp4", 'wb')

    # multi = threading.Thread(target=download2)
    # multi.daemon = True
    # multi.start()

    def download_chunk(readsofar=0, chunksize=1 << 13):
        # report progress
        percent = readsofar * 1e2 / totalsize  # assume totalsize > 0
        top.title('%%%.0f %s' % (percent, title,))
        progressbar['value'] = percent

        # download chunk
        data = response.read(chunksize)
        if not data:  # finished downloading
            outputfile.close()
            root.destroy()  # close GUI
        else:
            outputfile.write(data)  # save to filename
            # schedule to download the next chunk
            root.after(0, download_chunk, readsofar + len(data), chunksize)


def data_extractor(url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    with ydl:
        result = ydl.extract_info(url, download=False)
    final_list = []
    for i in result['formats']:
        final_dict = {}
        if (i['ext'] == 'mp4' or 'webm') and not ('DASH' in i['format_note']):
            if not ('medium' in i['format_note']):
                final_dict['ext'] = i['ext']
                final_dict['height'] = i['height']
                final_dict['url'] = i['url']
                final_dict['title'] = result['title']
                final_dict['thumbnail'] = result['thumbnail']
                final_list.append(final_dict)



    return final_list




def callBack():
    value = E1.get()
    donoting(value)
    print(value)


def donoting(url):
    out = data_extractor(url)
    y = 100
    x = 2
    y1 = 2
    for i in range(len(out)):
        a = out[i]
        if i == 0:
            L2 = Label(top, text=a['title'].encode('ascii', 'ignore'))
            L2.grid(row=(x), column=y1)

            image_url = a['thumbnail']
            filename, headers = urllib.request.urlretrieve(image_url)
            os.rename(filename, filename + ".jpg")
            img = ImageTk.PhotoImage(file=filename + ".jpg")
            panel = Label(top, image=img, width=190, height=190)

            panel.image = img
            panel.grid(row=(x - 1), column=3)

            x += 1
        button = ttk.Button(top, text=str(a['ext']) + ' ' + str(a['height']),
                            command=lambda: download2(a['url'], a['title']))
        button.grid(row=x, column=y1)
        progressbar = ttk.Progressbar(top, length=400)
        progressbar.grid(row=(x), column=(y1+1))
        y += 50
        x += 1
        # progress = ttk.Progressbar(top, length=100)
        # progress.pack()

        # # Launch the loop once the window is loaded
        # progress.after(1, MAIN)

#
# def download(data, title):
#     urllib.request.urlretrieve(data, "title.mp4")


def buttonValue(data, title):
    print(data)
    print(title)


top = Tk()
top.title('YouTube Downloader')
top.geometry('800x600')
top.title('YouTube Downloader')
top.iconbitmap(top, default='icon.ico')

L1 = Label(top, text="Enter Url")
L1.grid(row=0, column=1, padx=5, pady=5)
E1 = Entry(top, width=50)
E1.grid(row=0, column=2)

B = ttk.Button(top, text="Download", command=callBack)
B.place(x=100, y=100)
B.grid(row=1, column=2, padx=10)

top.mainloop()
