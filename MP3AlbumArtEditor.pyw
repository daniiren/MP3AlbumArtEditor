import os
from os import remove
import sys
import shutil
import eyed3
import re
import urllib.request, urllib.error, urllib.parse
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from tkinter import Button, Image, Label, messagebox, PhotoImage
import tkinter as tk 
from tkinter import filedialog
import time

folderPath = ""
MP3FilePath = ""
imagePath = ""

root = tk.Tk()
root.geometry("405x155")
root.title("MP3 AlburArt Editor")
root.resizable(False, False)

def chooseFolder() :
    global folderPath
    path = filedialog.askdirectory()
    if (len(path)) :
        folderPath = path + "/"
        root.destroy()


def chooseMP3File() :
    global MP3FilePath
    path = filedialog.askopenfilename(filetypes = (("MP3 Files", "*.mp3"), ("Any File", "*.*")))
    if (len(path)) :
        MP3FilePath = path + "/"
        root.destroy()


def chooseImageFile() :
    global imagePath
    imagePath = filedialog.askopenfilename(filetypes = (("JPG Files", "*.jpg"), ("Any File", "*.*")))
    if (len(imagePath)) :
        imageLabel = tk.Label(root, text = "(Image Selected)", font = "Helvetica 8 bold italic",fg = "white", bg = "gray24")
        imageLabel.place(relx = 0.49, rely = 0.94, anchor = "center")


def openReadMe() :
    os.startfile(os.getcwd() + "/Read me.txt")


def Mp3TagsEditor(folderPath) :
    if (len(folderPath)) :
        for item in os.listdir(folderPath) :
            if (not os.path.isdir(folderPath + item)) :
                songName = item[:-4]
                setImageToMP3File(songName, folderPath + item)
                
    elif (len(MP3FilePath)) :
        songName = ""
        for char in range(len(MP3FilePath) - 6, 0, -1) :    # We find the name of the song from the path
            if (MP3FilePath[char]) == "/" :
                break
            else :
                songName += MP3FilePath[char]
        songName = songName[::-1]

        setImageToMP3File(songName, MP3FilePath)

    if (not len(imagePath)) :
        time.sleep(2)                                       # That time sleep is because the program (sometimes) runs so fast and
        os.remove("googleImageResult.html")                 # when it comes on the "os.remove" lines the image file is still open to be set as 
        os.remove("albumArtImage.jpg")                      # album art. For that reason we wait for 2 seconds just to be sure that the image is set correctly on the mp3 file.


def setImageToMP3File(songName, path) :
    audioFile = eyed3.load(path)    # Load the mp3 file

    if (audioFile.tag == None):     # If the mp3 file doesn't have tags,
        audioFile.initTag()         # we initialize a new tag
    if (len(imagePath)) :
        audioFile.tag.images.set(3, open(imagePath, "rb").read(), "images/jpg")    
    else :
        GoogleImageFinder(songName)
        audioFile.tag.images.set(3, open("albumArtImage.jpg", "rb").read(), "images/jpg")

    audioFile.tag.save()
    

def GoogleImageFinder(query) :
    url = "http://images.google.com/search?q=" + query + "&tbm=isch&sout=1"

    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    
    opener = AppURLopener()
    response = opener.open(url)
    webContent = response.read()                                                        

    f = open("googleImageResult.html", "wb")   # We save the html page with the photos of the mp3 file name
    f.write(webContent)
    f.close()

    imageLink = ""
    openedQuote = False
    closedQuote = True

    with open("googleImageResult.html", "r", encoding = "UTF-8") as page :  # We seach for the first photo link from the html file we downloaded 
        text = page.read()                                                  # and then we extract the photo and save it where the program's path is. 
        srcIndexes = [i.start() for i in re.finditer("src", text)]

        for char in text[srcIndexes[1]:] :
            if (char == "\"" and openedQuote) :
                openedQuote = False
                closedQuote = True
                break

            if (char == "\"" and closedQuote) :
                openedQuote = True
                closedQuote = False

            if (openedQuote) :
                if (char != "\"") :
                    imageLink += char

    urllib.request.urlretrieve(imageLink, "albumArtImage.jpg")

# GUI
root.configure(background = "gray24")
welcomeLabel = tk.Label(root, text = "MP3 AlbumArt Editor", font = "Helvetica 20 bold italic",fg = "white", bg = "gray24")
creatorName = tk.Label(root, text = "Made by Daniel Ren.", font = "Helvetica 8 italic",fg = "white", bg = "gray24")
welcomeLabel.place(relx = 0.0, rely = 0.0, anchor = "nw")
creatorName.place(relx = 0.0, rely = 0.20, anchor = "nw")

FolderButton = tk.Button(text = "Choose folder", width = 20, fg = "black", command = chooseFolder).place(x = 0, y = 70)
mp3FileButton = tk.Button(text = "Choose MP3 file", width = 20, fg = "black", command = chooseMP3File).place(x = 0, y = 100)
ImageFileButton = tk.Button(text = "Choose your Image file", width = 20, fg = "black", command = chooseImageFile).place(x = 0, y = 130)
helpButton = tk.Button(text = "Help", fg = "black", command = openReadMe).place(x = 370, y = 130)

root.mainloop()

if (len(folderPath) or len(MP3FilePath)) :
    Mp3TagsEditor(folderPath)
