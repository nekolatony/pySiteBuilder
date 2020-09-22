from PIL import Image,ImageTk
import cv2 as cv2
import numpy as np
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinterhtml import HtmlFrame
import webview
import threading
import pdfkit
from pdf2image import convert_from_path
import browser

url = "Site/site.html"
global HtmlViewer

class PDFConverter(threading.Thread): # convert html to pdf

    def __init__(self ):
        threading.Thread.__init__(self)

        self.start()
    def run(self):
        pdfkit.from_url(url, 'Site/site.pdf')

class HTMLViewer(threading.Thread):

    def __init__(self ):
        threading.Thread.__init__(self)
        self.browser = None
        self.start()
    def run(self):

        self.browser = browser.new()

    def Refresh(self):
        self.browser.Refresh()
    def getBrowser(self):
       return self.browser


class Application(tk.Frame):   # tkinter window
    def __init__(self, HtmlViewer,master=None,):
        super().__init__(master)
        self.HtmlViewer = HtmlViewer
        self.master = master
        self.master.minsize(1500, 1000)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        # PDFConverter()
        self.create_widgets()



    def create_widgets(self):
        self.siteView = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.siteView, width = 512, height = 512)
        self.pages = convert_from_path('Site/site.pdf', 1)
        self.pages[0].save('Site/site.jpg','PNG')
        self.img = tk.PhotoImage(file='Site/python.png')
        self.canvas.create_image( 0,0, anchor='nw', image=self.img)
        self.canvas.grid(row=0,sticky="nsew")

        self.siteView.grid(row = 1 ,column = 2,sticky = 'nsew')

        self.h1 = tk.Frame(self.master, bg='cyan', width=250, height=80, pady=3)
        self.h2 = tk.Frame(self.master, bg='gray2', width=250, height=80, padx=3, pady=3)
        self.p = tk.Frame(self.master, bg='white', width=250, height=80, pady=3)
        self.label = tk.Frame(self.master, bg='lavender', width=250, height=200, pady=3)

        self.h1.grid(row=0, sticky="w")
        self.h2.grid(row=1, sticky="w")
        self.p.grid(row=3, sticky="w")
        self.label.grid(row=4, sticky="w")

        self.h1_label = tk.Button(self.h1,text = 'Add h1',command = lambda :self.addElement("h1"))
        self.h2_label = tk.Button(self.h2,text = 'Add h2',command = lambda :self.addElement("h2"))
        self.p_label =   tk.Button(self.p,text = 'Add Paraghraph',command = lambda :self.addElement("p"))


        self.label.grid_rowconfigure(3,weight=1)
        self.label.grid_columnconfigure(4, weight=0)
        self.label_label = tk.Label(self.label,text = 'Add Label')
        self.label_label.grid(row = 0 ,column = 0,sticky = 'nsew')

        self.checkbockLabel = tk.Button(self.label,width=25,text = 'Checkbox',command = lambda :self.addLabel('checkbox'))
        self.dateLabel = tk.Button(self.label,width=25, text='Date', command=lambda :self.addLabel('date'))
        self.emailLabel = tk.Button(self.label,width=25, text='Email', command=lambda :self.addLabel('email'))
        self.fileLabel = tk.Button(self.label, width=25,text='file', command=lambda :self.addLabel('file'))
        self.passsowrdLabel = tk.Button(self.label, width=25,text='Password', command=lambda :self.addLabel('password'))
        self.radioLabel = tk.Button(self.label, width=25,text='Radio', command=lambda :self.addLabel('radio'))
        self.searchLabel = tk.Button(self.label,width=25, text='search', command=lambda :self.addLabel('search'))
        self.textLabel = tk.Button(self.label, width=25,text='text', command=lambda :self.addLabel('text'))
        self.timeLabel = tk.Button(self.label,width=25, text='time', command=lambda :self.addLabel('time'))
        self.urlLabel = tk.Button(self.label, width=25,text='url', command=lambda :self.addLabel('url'))


        self.checkbockLabel.grid(row = 1 ,column = 0,sticky = 'ns')
        self.dateLabel.grid(row = 1 ,column = 1,sticky = 'nsew')
        self.emailLabel.grid(row = 1 ,column = 2,sticky = 'nsew')
        self.fileLabel.grid(row = 2 ,column = 0,sticky = 'nsew')
        self.passsowrdLabel.grid(row = 2 ,column = 1,sticky = 'ns')
        self.radioLabel.grid(row = 2 ,column = 2,sticky = 'ns')
        self.searchLabel.grid(row = 3 ,column = 0,sticky = 'nsew')
        self.textLabel.grid(row = 3 ,column = 1,sticky = 'nsew')
        self.timeLabel.grid(row = 3 ,column = 2,sticky = 'nsew')
        self.urlLabel.grid(row = 4 ,column = 1,sticky = 'nsew')

        self.h1_label.place(relx=0.5, rely=0.5, anchor='center')
        self.p_label.place(relx=0.5, rely=0.5, anchor='center')
        self.h2_label.place(relx=0.5, rely=0.5, anchor='center')
        self.label_label.place(relx=0.5, rely=0.0, anchor='n')




    def addElement(self,tag):
        with open(url, 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        print(len(data))
        cnt = 0
        for line in data:
            if line.find('<body>') != -1:
                break;
                print('found it')
            cnt = cnt + 1

        tag1 = "</br><"+ tag + ">Added " + tag + " succesfully</" + tag +"></br>\n"
        data.insert(cnt + 1, """                    """ +tag1)

        # and write everything back
        with open(url, 'w') as file:
            file.writelines(data)
        # PDFConverter()



    def addP(self):
        with open(url, 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        print(len(data))
        cnt = 0
        for line in data:
            if line.find('<body>')!= -1:
                break;
                print('found it')
            cnt = cnt + 1


        data.insert(cnt+1 ,"""                     </br><p>AddP is working perfectly</p></br>\n""")


        # and write everything back
        with open(url, 'w') as file:
            file.writelines(data)

        # PDFConverter()



def load_html(window):
  window.load_url("Site/site.html")


class WebviewX(threading.Thread):

    def __init__(self ,window):
        threading.Thread.__init__(self)
        self.window = window
        self.start()
    def run(self):
        webview.start(load_html, self.window)



def main():

    f = open(url, "w")

    # main html template
    f.write("""<!doctype html>

                <html lang="en">
                <head>
                    <meta charset="utf-8">

                    <title>The HTML5 Herald</title>
                    <meta name="description" content="The HTML5 Herald">
                    <meta name="author" content="SitePoint">

                     <link rel="stylesheet" href="css/styles.css?v=1.0">

                </head>

                <body>
                    <h1>This site is created in python</h1>
                    </br>
                    <img src="  """ + r"""file:///C:\Users\nekol\Documents\PycharmProjects\webSite-generator\venv\Site\python.png" alt="python" width="100" height="100">
                    </br>
                    <h2>Author: Tony Nekola</h2>
                    </br>
                </body>
                </html>""")

    f.close()


    window =webview.create_window('Load HTML Example', '<p2>Welcome</p2>', width=400, height=500)
    HtmlViewer =HTMLViewer()
    root = tk.Tk()
    app = Application(HtmlViewer,master=root)
    app.mainloop()


if __name__ == "__main__":
    main()