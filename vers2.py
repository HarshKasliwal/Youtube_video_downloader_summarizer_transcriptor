from tkinter import *
from tkinter.filedialog import *
from pytube import *
from pytube import YouTube
from PIL import Image
from PIL import ImageTk
from tkinter.messagebox import *
import threading
from threading import Thread
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

# total size container according to size of video
file_size=0
length=0
x=""

# called for updating percentage
def progress(chunk: None, file_handler: None, bytes_remaining: None):
    global file_size
    downloaded=(file_size-bytes_remaining)
    percent=(downloaded/file_size)*100
    btnd.config(text="{:00.0f} % Downloaded".format(percent))


def search():
    global length
     # get the url
    url=urlEntry.get()
    obj=YouTube(url)
    try:
        # obj.streams.all() returns a list of objects in all the streamable formats
        #formats include only audio or video , as mp4 or webm , resolution , fps ..etc
        #obj.streams.first() returns the first object
        #example: <Stream: itag="18" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">
        streams=obj.streams.filter(file_extension='mp4',progressive=True).all()

        for x in streams:
            length =length + 1
            str="{0},{1}".format(x.type,x.resolution)
            listbox.insert(END,str)
        listbox.place(x=500,y=400)    

    except Exception as e:
        print("could not display list")

def hellojustthread(a):
    url=urlEntry.get()
    obj=YouTube(url)
    streams=obj.streams.filter(file_extension='mp4',progressive=True).all()
    for f in streams:
        if(a.find(str(f.type)) and a.find(str(f.resolution))):
            return f


def hello(evt):
    x=str(listbox.get(ACTIVE))


def startDownload():
    global file_size,length,x
    try:
        url=urlEntry.get()
            #changing button text
        btnd.config(text="Please Wait..") 
        btnd.config(state=DISABLED)
        snew=hellojustthread(x)
            # askdirectory() returns the path which you selected
        path=askdirectory()
        if(path is None):
            return
            # create youtube class object
            # we can fetch videos using obj
            # progress function is called repeatedly until video is downloaded
        obj=YouTube(url,on_progress_callback=progress)
        file_size=snew.filesize
        print(file_size)
            #getting title of the video
        title=snew.title
        guiTitle.config(text="Title : "+title)
        guiTitle.place(x=500,y=100)

            #downloading the video and saves to the path mentioned
        snew.download(path)
        
            #changing button text
        btnd.config(text="Download Now") 
        btnd.config(state=NORMAL)
        showinfo("CONGRATS","Downloaded Successfully")
        urlEntry.delete(0,END)
        listbox.delete(0,END)
        guiTitle.place_forget()

    except Exception as e:
        print(e)

# created  downloading on a new thread otherwise it starts on gui thread only 
def threadsearch():
    # creating a new thread
    thread=Thread(target=search)
    thread.start()

def threadDownload():
    # creating a new thread
    thread=Thread(target=startDownload)
    thread.start()

def transcript():
    vid_id=idEntry.get()
    #vid_id='o9xH6v_vfDg'
    print(vid_id)
    data=yta.get_transcript(vid_id)
    transcript = ''
    for value in data:
        for  key,val in value.items():
            if key == 'text':
                transcript +=val+"."

    file=open("gari.txt",'w')
    file.write(transcript)

def summary():
    def read_article(file_name):
        file = open(file_name, "r")
        filedata = file.readlines ()
        article = filedata[0].split(".")
        sentences = []
        for sentence in article:
            sentences.append(sentence.replace("[^a-ZA-Z]"," ").split(" "))
        sentences.pop()
        return sentences
    def sentence_similarity(sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords=[]
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
        all_words = list(set(sent1+sent2))

        vector1= [0]*len(all_words)
        vector2= [0]*len(all_words)
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1
        return 1-cosine_distance(vector1,vector2)

    def gen_sim_matrix(sentences,stop_words):
        similarity_matrix=np.zeros((len(sentences),len(sentences)))
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue
                similarity_matrix[idx2]=sentence_similarity(sentences[idx1],sentences[idx2],stop_words)
        return similarity_matrix
    def generate_summary(file_name,top_n=5):
        stop_words=stopwords.words('english')
        summarize_text=[]
        sentences=read_article(file_name)
        sentence_similarity_matrix=gen_sim_matrix(sentences,stop_words)
        sentence_similarity_graph=nx.from_numpy_array(sentence_similarity_matrix)
        scores=nx.pagerank(sentence_similarity_graph, max_iter=6000)
        ranked_sentence=sorted(((scores[i],s)for i,s in enumerate(sentences)),reverse=True)
        
        for i in range(top_n):
                summarize_text.append(" ".join(ranked_sentence[i][1]))
        print("Summary\n",".  ".join(summarize_text))
    generate_summary("gari.txt",10)
# GUI PART
root=Tk()
# setting the icon with our title
root.iconbitmap('youtube.ico')

# setting the title of our window
root.title("Youtube Video Downloader/Transcripter/Summarizer")

root.geometry('1600x800+0+0')

# for the image to display in window
width = 1600
height = 800
img = Image.open("yt.png")
img = img.resize((width,height), Image.ANTIALIAS)
photoImg =  ImageTk.PhotoImage(img)
icon=Label(root,image=photoImg)
icon.place(x=0,y=0)

# img2 = Image.open("logo.png")
# img2 = img2.resize((250,250), Image.ANTIALIAS)
# photoImg2 =  ImageTk.PhotoImage(img2)
# icon2=Label(root,image=photoImg2)
# icon2.place(x=500,y=100, width=250, height=100)

urllabel=Label(root,text="ENTER THE URL BELOW",font=("verdana",20))
urllabel.place(x=500,y=275)
# url entry 
urlEntry=Entry(root,font=("verdana",20),width=25)
urlEntry.place(x=500,y=325)



searchbtn=Button(root,text="SEARCH STREAMS",font=("verdana",15),bg="black",fg="gold",relief=RIDGE,command=threadsearch)
searchbtn.place(x=1000,y=300)

scrollbar=Scrollbar(root)
scrollbar.place(x=920,y=400,height=200,width=20)

listbox=Listbox(root,yscrollcommand=scrollbar.set,selectmode=BROWSE,width=45,height=10,font=('arial',12,'italic bold'),relief="ridge",highlightcolor='blue',highlightthickness=2)
listbox.bind('<<ListboxSelect>>',hello)
listbox.place(x=500,y=400)

# download button
btnd=Button(root,text="DOWNLOAD NOW",font=("verdana",15),bg="black",fg="gold",relief=RIDGE,command=threadDownload)
btnd.place(x=1000,y=350)

guiTitle=Label(root,text="")


idlabel=Label(root,text="ENTER THE ID(for summary) ",font=("verdana",20))
idlabel.place(x=500,y=630)
# id entry 
idEntry=Entry(root,font=("verdana",20),width=25)
idEntry.place(x=500,y=680)

btnd2=Button(root,text="Summarize",font=("verdana",15),bg="black",fg="gold",relief=RIDGE,command=summary)
btnd2.place(x=1000,y=650)


btnd3=Button(root,text="Transcript",font=("verdana",15),bg="black",fg="gold",relief=RIDGE,command=transcript)
btnd3.place(x=1000,y=600)

root.mainloop()