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
# import browser
import webview
from HTMLParser.Parser import *

url = "Site/site.html"
global HtmlViewer
subCombonent_flag = 0
'Button', 'Text Area', 'Anchor element - <a>', 'Input', 'Select', 'Progress bar','Object'
HTML_sub_Components_names ={'Heading 1':'h1','Heading 2':'h2','Heading 3':'h3','Heading 4':'h4','Heading 5':'h5','Heading 6':'h6','Paragraph':'p','Label':'label'
                            ,'Ordered list':'ol','UnOrdered list':'ul','Audio':'audio','Image':'img','Canvas':'canvas','Picture':'picture','SVG':'svg','Video':'video','iframe':'iframe'
                            , 'Button': 'button' ,'Text Area':'textarea','Input':'input','Select':'select','Progress bar':'progress','Object':'object'
                            ,'Anchor element - <a>':'a'}

CSS_attr = {}


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(1)

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        tk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = tk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show)
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.sub_frame.pack(fill="x", expand=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='^')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')


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
    def __init__(self, HtmlViewer,master=None):
        super().__init__(master)
        self.HtmlViewer = HtmlViewer
        self.master = master
        screen_height = self.master.winfo_screenheight()
        self.master.geometry("500x"+str(screen_height-80)+"+0+0")
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        # PDFConverter()
        self.create_widgets()
        self.options_window = tk.Toplevel(self.master)
        self.create_options()

    def add_H_P(self,tag_type):
        print('add_H_P() selected ' + tag_type )
        self.CSS_frame.destroy()
        self.CSS_frame = tk.Frame(self.options_window, relief="raised")
        self.CSS_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        if self.Dicesion_frame:
            self.Dicesion_frame.destroy()

        global CSS_attr
        CSS_attr.clear()

        self.setUp_Text()

        self.setUp_Identity()

        self.setUp_Background()

        self.setUp_Border()

        self.setUp_Dimensions()

        self.setUp_Font()

        self.setUp_Margin()

        self.setUp_Padding()

        self.setUp_Dicesion(self.addElement,tag_type)

    def setUp_Text(self):
        self.Text_Frame = ToggledFrame(self.CSS_frame, text='Text', relief="flat", borderwidth=1)
        self.Text_Frame.sub_frame.grid_rowconfigure(1, weight=1)
        self.Text_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.text_label = tk.Label(self.Text_Frame.sub_frame, text='Text:', height=1, pady=2)
        self.text_text = tk.Entry(self.Text_Frame.sub_frame)
        self.text_label.grid(row=0, column=0, sticky='nsew')
        self.text_text.grid(row=0, column=1, sticky='nsew')
        self.Text_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    def setUp_Padding(self):
        # ------------------------------------Padding-----------------------------------------------------
        self.Padding_Frame = ToggledFrame(self.CSS_frame, text='Padding', relief="flat", borderwidth=1)
        self.Padding_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.Padding_Frame.sub_frame.grid_columnconfigure(4, weight=1)
        self.padding_top_label = tk.Label(self.Padding_Frame.sub_frame, text='top:', height=1, pady=2)
        self.padding_top_text = tk.Text(self.Padding_Frame.sub_frame, height=1, width=7, pady=5)
        self.padding_bottom_label = tk.Label(self.Padding_Frame.sub_frame, text='bottom:', height=1, pady=2)
        self.padding_bottom_text = tk.Text(self.Padding_Frame.sub_frame, height=1, width=7, pady=5)
        self.padding_left_label = tk.Label(self.Padding_Frame.sub_frame, text='left:', height=1, pady=2)
        self.padding_left_text = tk.Text(self.Padding_Frame.sub_frame, height=1, width=7, pady=5)
        self.padding_right_label = tk.Label(self.Padding_Frame.sub_frame, text='right:', height=1, pady=2)
        self.padding_right_text = tk.Text(self.Padding_Frame.sub_frame, height=1, width=7, pady=5)
        self.padding_top_label.grid(row=0, column=0, sticky='nsew')
        self.padding_top_text.grid(row=0, column=1, sticky='nsew')
        self.padding_bottom_label.grid(row=0, column=2, sticky='nsew')
        self.padding_bottom_text.grid(row=0, column=3, sticky='nsew')
        self.padding_left_label.grid(row=1, column=0, sticky='nsew')
        self.padding_left_text.grid(row=1, column=1, sticky='nsew')
        self.padding_right_label.grid(row=1, column=2, sticky='nsew')
        self.padding_right_text.grid(row=1, column=3, sticky='nsew')
        self.Padding_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global CSS_attr
        CSS_attr['padding-top:' ] = self.padding_top_text
        CSS_attr['padding-bottom:' ] = self.padding_bottom_text
        CSS_attr['padding-left:' ] = self.padding_left_text
        CSS_attr['padding-right:' ] = self.padding_right_text

    def setUp_Margin(self):
        # ------------------------------------Margin-----------------------------------------------------
        self.Margin_Frame = ToggledFrame(self.CSS_frame, text='Margin', relief="flat", borderwidth=1)
        self.Margin_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.Margin_Frame.sub_frame.grid_columnconfigure(4, weight=1)
        self.margin_top_label = tk.Label(self.Margin_Frame.sub_frame, text='top:', height=1, pady=2)
        self.margin_top_text = tk.Text(self.Margin_Frame.sub_frame, height=1, width=7, pady=5)
        self.margin_bottom_label = tk.Label(self.Margin_Frame.sub_frame, text='bottom:', height=1,  pady=2)
        self.margin_bottom_text = tk.Text(self.Margin_Frame.sub_frame, height=1, width=7, pady=5)
        self.margin_left_label = tk.Label(self.Margin_Frame.sub_frame, text='left:', height=1,  pady=2)
        self.margin_left_text = tk.Text(self.Margin_Frame.sub_frame, height=1, width=7, pady=5)
        self.margin_right_label = tk.Label(self.Margin_Frame.sub_frame, text='right:', height=1, pady=2)
        self.margin_right_text = tk.Text(self.Margin_Frame.sub_frame, height=1, width=7, pady=5)
        self.margin_top_label.grid(row=0, column=0, sticky='nsew')
        self.margin_top_text.grid(row=0, column=1, sticky='nsew')
        self.margin_bottom_label.grid(row=0, column=2, sticky='nsew')
        self.margin_bottom_text.grid(row=0, column=3, sticky='nsew')
        self.margin_left_label.grid(row=1, column=0, sticky='nsew')
        self.margin_left_text.grid(row=1, column=1, sticky='nsew')
        self.margin_right_label.grid(row=1, column=2, sticky='nsew')
        self.margin_right_text.grid(row=1, column=3, sticky='nsew')
        self.Margin_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global CSS_attr
        CSS_attr['margin-top:'] = self.margin_top_text
        CSS_attr['margin-bottom:'] = self.margin_bottom_text
        CSS_attr['margin-left:'] = self.margin_left_text
        CSS_attr['margin-right:'] = self.margin_right_text

    def setUp_Dicesion(self,add_elem,tag_type):
        # ------------------------------------Dicesion-----------------------------------------------------
        self.Dicesion_frame = tk.Frame(self.options_window, relief="raised")
        self.Dicesion_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="s")
        self.add_btn = tk.Button(self.Dicesion_frame, text='ADD', relief="groove", justify='right',
                                 command=lambda: add_elem(tag_type))
        self.cancel_btn = tk.Button(self.Dicesion_frame, text='CANCEL', command=lambda: print('cancel'),
                                    relief="groove", justify='left')
        self.add_btn.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.cancel_btn.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    def setUp_Font(self):
        # ------------------------------------Font-----------------------------------------------------
        self.Font_Frame = ToggledFrame(self.CSS_frame, text='Font', relief="flat", borderwidth=1)
        self.Font_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.Font_Frame.sub_frame.grid_columnconfigure(4, weight=1)
        self.font_family_label = tk.Label(self.Font_Frame.sub_frame, text='family:', height=1, pady=2)
        self.font_family_text = tk.Text(self.Font_Frame.sub_frame, height=1, width=7, pady=5)
        self.font_size_label = tk.Label(self.Font_Frame.sub_frame, text='size:', height=1, pady=2)
        self.font_size_text = tk.Text(self.Font_Frame.sub_frame, height=1, width=7, pady=5)
        self.font_style_label = tk.Label(self.Font_Frame.sub_frame, text='style:', height=1, pady=2)
        self.font_style_text = tk.Text(self.Font_Frame.sub_frame, height=1, width=7, pady=5)
        self.font_weight_label = tk.Label(self.Font_Frame.sub_frame, text='weight:', height=1, pady=2)
        self.font_weight_text = tk.Text(self.Font_Frame.sub_frame, height=1, width=7, pady=5)
        self.font_family_label.grid(row=0, column=0, sticky='nsew')
        self.font_family_text.grid(row=0, column=1, sticky='nsew')
        self.font_size_label.grid(row=0, column=2, sticky='nsew')
        self.font_size_text.grid(row=0, column=3, sticky='nsew')
        self.font_style_label.grid(row=1, column=0, sticky='nsew')
        self.font_style_text.grid(row=1, column=1, sticky='nsew')
        self.font_weight_label.grid(row=1, column=2, sticky='nsew')
        self.font_weight_text.grid(row=1, column=3, sticky='nsew')
        self.Font_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global CSS_attr
        CSS_attr['font-family:'] = self.font_family_text
        CSS_attr['font-size:'] = self.font_size_text
        CSS_attr['font-style:'] = self.font_style_text
        CSS_attr['font-weight:'] = self.font_weight_text


    def setUp_Dimensions(self):
        # ------------------------------------Dimension-----------------------------------------------------
        self.Dimension_Frame = ToggledFrame(self.CSS_frame, text='Dimensions', relief="flat", borderwidth=1)
        self.Dimension_Frame.sub_frame.grid_rowconfigure(3, weight=1)
        self.Dimension_Frame.sub_frame.grid_columnconfigure(4, weight=1)
        self.height_label = tk.Label(self.Dimension_Frame.sub_frame, text='Height:', height=1, pady=2)
        self.height_text = tk.Text(self.Dimension_Frame.sub_frame, height=1, width=7, pady=5)
        self.width_label = tk.Label(self.Dimension_Frame.sub_frame, text='Width:', height=1, pady=2)
        self.width_text = tk.Text(self.Dimension_Frame.sub_frame, height=1, width=7, pady=5)
        self.max_height_label = tk.Label(self.Dimension_Frame.sub_frame, text='Max Height:', height=1, pady=2)
        self.max_height_text = tk.Text(self.Dimension_Frame.sub_frame, height=1, width=7, pady=5)
        self.max_width_label = tk.Label(self.Dimension_Frame.sub_frame, text='Max Width:', height=1, pady=2)
        self.max_width_text = tk.Text(self.Dimension_Frame.sub_frame, height=1, width=7, pady=5)
        self.min_height_label = tk.Label(self.Dimension_Frame.sub_frame, text='Min Height:', height=1, pady=2)
        self.min_height_text = tk.Text(self.Dimension_Frame.sub_frame, height=1, width=7, pady=5)
        self.min_width_label = tk.Label(self.Dimension_Frame.sub_frame, text='Min Width:', height=1, pady=2)
        self.min_width_text = tk.Text(self.Dimension_Frame.sub_frame, height=1, width=7, pady=5)
        self.height_label.grid(row=0, column=0, sticky='nsew')
        self.height_text.grid(row=0, column=1, sticky='nsew')
        self.width_label.grid(row=0, column=2, sticky='nsew')
        self.width_text.grid(row=0, column=3, sticky='nsew')
        self.max_height_label.grid(row=1, column=0, sticky='nsew')
        self.max_height_text.grid(row=1, column=1, sticky='nsew')
        self.max_width_label.grid(row=1, column=2, sticky='nsew')
        self.max_width_text.grid(row=1, column=3, sticky='nsew')
        self.min_height_label.grid(row=2, column=0, sticky='nsew')
        self.min_height_text.grid(row=2, column=1, sticky='nsew')
        self.min_width_label.grid(row=2, column=2, sticky='nsew')
        self.min_width_text.grid(row=2, column=3, sticky='nsew')
        self.Dimension_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global CSS_attr
        CSS_attr['height:'] = self.height_text
        CSS_attr['width:'] = self.width_text
        CSS_attr['max-height:'] = self.max_height_text
        CSS_attr['max_width:'] = self.max_width_text
        CSS_attr['min-height:'] = self.min_height_text
        CSS_attr['min-width:'] = self.min_width_text

    def setUp_Border(self):   # work in progress
        # ------------------------------------Border-----------------------------------------------------
        self.Border_Frame = ToggledFrame(self.CSS_frame, text='Border', relief="flat", borderwidth=1)
        self.Border_Frame.sub_frame.grid_rowconfigure(5, weight=1)
        self.Border_Frame.sub_frame.grid_columnconfigure(4, weight=1)
        self.Border_hint_label = tk.Label(self.Border_Frame.sub_frame, text='hint : width style color\nExample : 3px dotted blue', height=2, pady=2)
        self.Border_top_label = tk.Label(self.Border_Frame.sub_frame, text='Top:', height=1, pady=2)
        self.Border_top_text = tk.Text(self.Border_Frame.sub_frame, height=1, pady=5)
        self.Border_bottom_label = tk.Label(self.Border_Frame.sub_frame, text='Bottom:', height=1, pady=2)
        self.Border_bottom_text = tk.Text(self.Border_Frame.sub_frame, height=1, pady=5)
        self.Border_left_label = tk.Label(self.Border_Frame.sub_frame, text='Left:', height=1, pady=2)
        self.Border_left_text = tk.Text(self.Border_Frame.sub_frame, height=1, pady=5)
        self.Border_right_label = tk.Label(self.Border_Frame.sub_frame, text='Right:', height=1, pady=2)
        self.Border_right_text = tk.Text(self.Border_Frame.sub_frame, height=1,  pady=5)
        self.Border_4way_label = tk.Label(self.Border_Frame.sub_frame, text='Border:', height=1, pady=2)
        self.Border_4way_text = tk.Text(self.Border_Frame.sub_frame, height=1,  pady=5)
        self.Border_hint_label.grid(row=0, sticky='nsew')
        self.Border_top_label.grid(row=2, column=0, sticky='nsew')
        self.Border_top_text.grid(row=2, column=1, sticky='nsew')
        self.Border_bottom_label.grid(row=3, column=0, sticky='nsew')
        self.Border_bottom_text.grid(row=3, column=1, sticky='nsew')
        self.Border_left_label.grid(row=4, column=0, sticky='nsew')
        self.Border_left_text.grid(row=4, column=1, sticky='nsew')
        self.Border_right_label.grid(row=5, column=0, sticky='nsew')
        self.Border_right_text.grid(row=5, column=1, sticky='nsew')
        self.Border_4way_label.grid(row=1, column=0, sticky='nsew')
        self.Border_4way_text.grid(row=1, column=1, sticky='nsew')

        self.Border_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global CSS_attr
        CSS_attr['border-color:'] = self.Border_4way_text
        CSS_attr['border-top:'] = self.Border_top_text
        CSS_attr['border-bottom:'] = self.Border_bottom_text


    def setUp_Background(self):
        # ------------------------------------Background-----------------------------------------------------
        self.Background_Frame = ToggledFrame(self.CSS_frame, text='Background', relief="flat", borderwidth=1)
        self.Background_Frame.sub_frame.grid_rowconfigure(3, weight=1)
        self.Background_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.bg_color_label = tk.Label(self.Background_Frame.sub_frame, text='background color:', height=1, pady=2)
        self.bg_color_text = tk.Text(self.Background_Frame.sub_frame, height=1, width=7, pady=5)
        self.bg_img_label = tk.Label(self.Background_Frame.sub_frame, text='background image:', height=1, pady=2)
        self.bg_img_text = tk.Text(self.Background_Frame.sub_frame, height=1, width=7, pady=5)
        self.bg_pos_label = tk.Label(self.Background_Frame.sub_frame, text='background position:', height=1, pady=2)
        self.bg_pos_text = tk.Checkbutton(self.Background_Frame.sub_frame, height=1, width=7, pady=5)
        self.bg_color_label.grid(row=0, column=0, sticky='nsew')
        self.bg_color_text.grid(row=0, column=1, sticky='nsew')
        self.bg_img_label.grid(row=1, column=0, sticky='nsew')
        self.bg_img_text.grid(row=1, column=1, sticky='nsew')
        self.bg_pos_label.grid(row=2, column=0, sticky='nsew')
        self.bg_pos_text.grid(row=2, column=1, sticky='nsew')
        self.Background_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global CSS_attr
        CSS_attr['background-color:'] = self.bg_color_text
        CSS_attr['background-image:'] = self.bg_img_text


    def setUp_Identity(self):
        # ---------------------------------Identity-----------------------------------------------------
        self.identity_Frame = ToggledFrame(self.CSS_frame, text='Identity', relief="flat", borderwidth=1)
        self.identity_Frame.sub_frame.grid_rowconfigure(3, weight=1)
        self.identity_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.id_label = tk.Label(self.identity_Frame.sub_frame, text='ID:', height=1, width=3, pady=2)
        self.id_text = tk.Text(self.identity_Frame.sub_frame, height=1, width=7, pady=5)
        self.class_label = tk.Label(self.identity_Frame.sub_frame, text='Class:', height=1, width=3, pady=2)
        self.class_text = tk.Text(self.identity_Frame.sub_frame, height=1, width=7, pady=5)
        self.hidden_label = tk.Label(self.identity_Frame.sub_frame, text='Hidden:', height=1, width=3, pady=2)
        self.Hidden_text = tk.Checkbutton(self.identity_Frame.sub_frame, height=1, width=7, pady=5)
        self.id_label.grid(row=0, column=0, sticky='nsew')
        self.id_text.grid(row=0, column=1, sticky='nsew')
        self.class_label.grid(row=1, column=0, sticky='nsew')
        self.class_text.grid(row=1, column=1, sticky='nsew')
        self.hidden_label.grid(row=2, column=0, sticky='nsew')
        self.Hidden_text.grid(row=2, column=1, sticky='nsew')
        self.identity_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")



    def onselect_subcomponent(self, event):  # define diffrent functions for every element type

        # print('onselect_subcomponent() selected ' + self.sub_components.get(self.sub_components.curselection()))
        if self.components.get(self.components.curselection()) == 'Headings and Paragragraphs':
            self.add_H_P(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])


    def onselect_component(self,event):
        # if self.sub_components.get(0) is None:
        #     return 1
        self.sub_components.delete(0, tk.END)
        if self.components.get(self.components.curselection()) == 'Headings and Paragragraphs':
            self.sub_components.insert(1, 'Heading 1', 'Heading 2', 'Heading 3','Heading 4','Heading 5','Heading 6', 'Paragraph','Label')
        if self.components.get(self.components.curselection()) == 'Lists':
            self.sub_components.insert(1, 'Ordered list', 'UnOrdered list')
        if self.components.get(self.components.curselection()) == 'Embeded content':
            self.sub_components.insert(1, 'Audio', 'Canvas','Image','Picture','SVG','Video','iframe')
        if self.components.get(self.components.curselection()) == 'Interactive content':
            self.sub_components.insert(1, 'Button', 'TextArea', 'Anchor element - <a>', 'Input', 'Select', 'Progress bar','Object')

    def create_widgets(self):
        # self.siteView = tk.Frame(self.master)
        # self.canvas = tk.Canvas(self.siteView, width = 512, height = 512)
        # self.pages = convert_from_path('Site/site.pdf', 1)
        # self.pages[0].save('Site/site.jpg','PNG')
        # self.img = tk.PhotoImage(file='Site/python.png')
        # self.canvas.create_image( 0,0, anchor='nw', image=self.img)
        # self.canvas.grid(row=0,sticky="nsew")

        # self.siteView.grid(row = 1 ,column = 2,sticky = 'nsew')



        self.components_frame = tk.Frame(self.master)
        self.components_label = tk.Label(self.components_frame,text = 'HTML componenets')
        self.components_label.pack(anchor = tk.CENTER)
        self.components = tk.Listbox(self.components_frame, selectmode=tk.SINGLE,height= 100,exportselection=0)
        self.scrollbar = tk.Scrollbar(self.components)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.components['yscrollcommand']= self.scrollbar.set
        self.components.insert(1, 'Headings and Paragragraphs','Interactive content','Embeded content','table','span','div','Lists')
        self.components_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.components.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.components.bind('<<ListboxSelect>>', self.onselect_component) #callback

        self.sub_components_frame = tk.Frame(self.master,height = 100)
        self.sub_components_label = tk.Label(self.sub_components_frame,text = 'HTML sub-componenets')
        self.sub_components_label.pack(anchor = tk.CENTER)
        self.sub_components = tk.Listbox(self.sub_components_frame, selectmode=tk.SINGLE,height= 100,exportselection=0)
        self.sub_components_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.sub_components.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.sub_components.bind('<<ListboxSelect>>', self.onselect_subcomponent)  #callback

        self.TreeView_Frame =  tk.Frame(self.master)
        self.TreeView_label = tk.Label(self.TreeView_Frame, text='components Tree')
        self.TreeView_label.pack(anchor=tk.CENTER)
        self.TreeView = tk.Listbox(self.TreeView_Frame, selectmode=tk.SINGLE, height=100)
        self.Treescrollbar = tk.Scrollbar(self.TreeView)
        self.Treescrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.TreeView['yscrollcommand'] = self.Treescrollbar.set
        self.TreeView_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.TreeView.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.TreeView.insert(1, 'to be continued ...','TreeView of the components','is a work in progress')


        # with open(url, 'r') as file:
        #     # read a list of lines into data
        #     data = file.readlines()
        # nodes = get_DOM_Tree(data)

        # self.h1_label = tk.Label(self.h1,text = 'Add h1')
        # self.h1_label.bind('<Button>',self.h1_onClick)

        # self.h2_label = tk.Button(self.h2,text = 'Add h2',command = lambda :self.addElement("h2"))
        # self.p_label =   tk.Button(self.p,text = 'Add Paraghraph',command = lambda :self.addElement("p"))


        # self.label.grid_rowconfigure(3,weight=1)
        # self.label.grid_columnconfigure(4, weight=0)
        # self.label_label = tk.Label(self.label,text = 'Add Label')
        # self.label_label.grid(row = 0 ,column = 0,sticky = 'nsew')

        # self.checkbockLabel = tk.Button(self.label,width=25,text = 'Checkbox',command = lambda :self.addLabel('checkbox'))
        # self.dateLabel = tk.Button(self.label,width=25, text='Date', command=lambda :self.addLabel('date'))
        # self.emailLabel = tk.Button(self.label,width=25, text='Email', command=lambda :self.addLabel('email'))
        # self.fileLabel = tk.Button(self.label, width=25,text='file', command=lambda :self.addLabel('file'))
        # self.passsowrdLabel = tk.Button(self.label, width=25,text='Password', command=lambda :self.addLabel('password'))
        # self.radioLabel = tk.Button(self.label, width=25,text='Radio', command=lambda :self.addLabel('radio'))
        # self.searchLabel = tk.Button(self.label,width=25, text='search', command=lambda :self.addLabel('search'))
        # self.textLabel = tk.Button(self.label, width=25,text='text', command=lambda :self.addLabel('text'))
        # self.timeLabel = tk.Button(self.label,width=25, text='time', command=lambda :self.addLabel('time'))
        # self.urlLabel = tk.Button(self.label, width=25,text='url', command=lambda :self.addLabel('url'))
        #
        #
        # self.checkbockLabel.grid(row = 1 ,column = 0,sticky = 'ns')
        # self.dateLabel.grid(row = 1 ,column = 1,sticky = 'nsew')
        # self.emailLabel.grid(row = 1 ,column = 2,sticky = 'nsew')
        # self.fileLabel.grid(row = 2 ,column = 0,sticky = 'nsew')
        # self.passsowrdLabel.grid(row = 2 ,column = 1,sticky = 'ns')
        # self.radioLabel.grid(row = 2 ,column = 2,sticky = 'ns')
        # self.searchLabel.grid(row = 3 ,column = 0,sticky = 'nsew')
        # self.textLabel.grid(row = 3 ,column = 1,sticky = 'nsew')
        # self.timeLabel.grid(row = 3 ,column = 2,sticky = 'nsew')
        # self.urlLabel.grid(row = 4 ,column = 1,sticky = 'nsew')
        #
        # # self.h1_label.place(relx=0.5, rely=0.5, anchor='center')
        # self.h1_label.grid(row = 0 ,column = 4,sticky = 'nsew')
        # self.p_label.place(relx=0.5, rely=0.5, anchor='center')
        # self.h2_label.place(relx=0.5, rely=0.5, anchor='center')
        # self.label_label.place(relx=0.5, rely=0.0, anchor='n')

    def create_options(self):
        screen_width = self.master.winfo_screenwidth() - 400
        screen_height = self.master.winfo_screenheight()
        self.options_window.geometry('400x'+str(screen_height-80)+"+"+str(screen_width)+"+0")
        self.Optionsscrollbar = tk.Scrollbar(self.options_window,orient=tk.VERTICAL)
        self.Optionsscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.CSS_frame = tk.Frame(self.options_window,relief="raised")
        self.CSS_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.Dicesion_frame = tk.Frame(self.options_window, relief="raised")
        self.Dicesion_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="s")

        # self.identity_Frame = ToggledFrame(self.CSS_frame,text='Identity', relief="flat", borderwidth=1)
        # self.identity_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        # self.identity_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        # self.id_label = tk.Label(self.identity_Frame.sub_frame, text='ID:', height=2, width=3, pady=5)
        # self.id_text = tk.Text(self.identity_Frame.sub_frame, height=2, width=7, pady=5)
        # self.class_label = tk.Label(self.identity_Frame.sub_frame, text='CLass:', height=2, width=3, pady=5)
        # self.class_text = tk.Text(self.identity_Frame.sub_frame, height=2, width=7, pady=5)
        #
        # self.id_label.grid(row=0, column=0, sticky='nsew')
        # self.id_text.grid(row=0, column=1, sticky='nsew')
        # self.class_label.grid(row=1, column=0, sticky='nsew')
        # self.class_text.grid(row=1, column=1, sticky='nsew')
        # self.identity_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        #
        #
        #
        #
        # self.position_label = ToggledFrame(self.CSS_frame,text = 'position:',relief="flat", borderwidth=1)
        # self.position_Text = tk.Listbox(self.position_label.sub_frame,selectmode = tk.SINGLE)
        # self.position_Text.insert(1,'relative','static','sticky','absolute','fixed')
        # self.position_label.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        # self.position_Text.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        #
        # self.position_Frame = ToggledFrame(self.CSS_frame,text='Position', relief="raised", borderwidth=1)
        # self.position_Frame.sub_frame.grid_rowconfigure(2,weight=1)
        # self.position_Frame.sub_frame.grid_columnconfigure(4, weight=1)
        # self.top_label = tk.Label(self.position_Frame.sub_frame,text = 'top:',height=2, width=3,pady= 5)
        # self.top_text = tk.Text(self.position_Frame.sub_frame, height=2, width=7, pady=5)
        # self.bottom_label = tk.Label(self.position_Frame.sub_frame, text='bottom:', height=2, width=3, pady=5)
        # self.bottom_text = tk.Text(self.position_Frame.sub_frame, height=2, width=7, pady=5)
        # self.left_label = tk.Label(self.position_Frame.sub_frame, text='left:', height=2, width=3, pady=5)
        # self.left_text = tk.Text(self.position_Frame.sub_frame, height=2, width=7, pady=5)
        # self.right_label = tk.Label(self.position_Frame.sub_frame, text='right:', height=2, width=3, pady=5)
        # self.right_text = tk.Text(self.position_Frame.sub_frame, height=2, width=7, pady=5)
        #
        # self.top_label.grid(row = 0 ,column = 0,sticky = 'nsew')
        # self.top_text.grid(row = 0 ,column = 1,sticky = 'nsew')
        # self.bottom_label.grid(row = 1 ,column = 0,sticky = 'nsew')
        # self.bottom_text.grid(row = 1 ,column = 1,sticky = 'nsew')
        # self.left_label.grid(row = 0 ,column = 2,sticky = 'nsew')
        # self.left_text.grid(row = 0 ,column = 3,sticky = 'nsew')
        # self.right_label.grid(row = 1 ,column = 2,sticky = 'nsew')
        # self.right_text.grid(row = 1 ,column = 3,sticky = 'nsew')
        # self.position_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        #
        # self.Dicesion_frame = tk.Frame(self.options_window,relief="raised")
        # self.Dicesion_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="s")
        # self.add_btn = tk.Button(self.Dicesion_frame, text='ADD', command=lambda :print('Add'),relief="groove",justify= 'right')
        # self.cancel_btn = tk.Button(self.Dicesion_frame, text='CANCEL', command=lambda: print('cancel'),relief="groove",justify= 'left')
        # self.add_btn.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        # self.cancel_btn.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    def h1_onClick(self,event):
        print(event)
        self.addElement('h1')

    def addElement(self,tag):
        with open(url, 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        # print(len(data))
        cnt = 0
        for line in data:
            if line.find('<body>') != -1:
                break;
                print('found it')
            cnt = cnt + 1
        print('x'*10)
        print(len(self.class_text.get("1.0",tk.END).strip()))
        print('x'*10)

        style = 'style =" '

        # if len(self.class_text.get("1.0",tk.END).strip()) != 0:
        #     style = ''.join([style,'class :'+self.class_text.get("1.0",tk.END).strip()+';'])
        # if len(self.bg_color_text.get("1.0", tk.END).strip()) != 0:
        #     style = ''.join([style,'background-color:' + self.bg_color_text.get("1.0", tk.END).strip() + ';'])
        global CSS_attr
        for attr in CSS_attr.keys():
            if len(CSS_attr[attr].get("1.0",tk.END).strip()) != 0:
                style = ''.join([style,attr+CSS_attr[attr].get("1.0",tk.END).strip(),';'])
        style= style + '"'



        tag1 = "<"+ tag +' '+style+ '>'+self.text_text.get() +"</" + tag +">\n"
        data.insert(cnt + 1, """                    """ +tag1)
        # print(tag1)
        # and write everything back
        with open(url, 'w') as file:
            file.writelines(data)
        # PDFConverter()

        # with open(url, 'r') as file:
        #     # read a list of lines into data
        #     data = file.readlines()
        #     print(data)



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
                    <meta name = "description" content = "The HTML5 Herald">
                    <meta name = "author" content = "SitePoint">
                    <link rel = "stylesheet" href = "css/styles.css?v=1.0">

                    <title>The HTML5 Herald</title>
                </head>

                <body>
                    <h1>This site is created in python</h1>
                    <br>
                    <img src="  """ + r"""file:///C:\Users\nekol\Documents\PycharmProjects\webSite-generator\venv\Site\python.png" alt="python" width="100" height="100"><img/>
                    <br>
                    <h2>Author: Tony Nekola</h2>
                    <br>
                </body>
                </html>""")


    f.close()


    # HtmlViewer =HTMLViewer()
    root = tk.Tk()
    app = Application(None,master=root)
    app.mainloop()


if __name__ == "__main__":
    main()