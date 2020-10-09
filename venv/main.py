from PIL import Image,ImageTk
import cv2 as cv2
import numpy as np
try:
    import tkinter as tk
    from tkinter import ttk
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
                            , 'Button': 'button' ,'Text Area':'textarea','Input -(form)':'input','Select':'select','Progress bar':'progress','Object':'object'
                            ,'Anchor element - <a>':'a'}

CSS_attr = {}
HTML_attr= {}

top_level_widgets = []

HTML_ready_code = {'progress':""""<label for="">  </label>

                  <progress id="" max="" value="" > </progress>"""
                   ,"datalist":"""<datalist id="">
                     <option value="">
                    </datalist>"""
                   ,'ul':"""<ul>         </ul>"""
                   ,'ol':"""<ol>         </ol>"""
                   ,'picture':'''
                   <picture>
                    <source media="" srcset="">
                   <img src="" alt="" /></picture>'''
                   ,'object':'''<object  data="" type=""></object>''',
                   'input':'''<label for=""></label>
                                <input  type="" id="" name="" required ><br>'''
                   ,'select':'''<label for=""></label>

                                <select name="" id="">
                                    <option value="">--Please choose an option--</option>
                                    <option value=""></option>
                               </select>'''}


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
        screen_width = self.master.winfo_screenwidth() - 400
        screen_height = self.master.winfo_screenheight()
        self.options_window.geometry('400x'+str(screen_height-80)+"+"+str(screen_width)+"+0")


        self.create_options()

    def add_Select(self, tag_type):

        self.add_Global_Attributes(tag_type)
        self.add_btn['command'] = lambda: self.addPreDefinedElement(tag_type)

        self.Select_Frame = ToggledFrame(self.canv, text='Select data', relief="flat", borderwidth=1)
        self.Select_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Select_Frame.sub_frame.grid_rowconfigure(3, weight=1)
        self.name_label = tk.Label(self.Select_Frame.sub_frame, height=1, text="Name:")
        self.name_text = tk.Text(self.Select_Frame.sub_frame, height=1)
        self.example_label = tk.Label(self.Select_Frame.sub_frame, height=1, text="Enter the value and name of \neach option on a seperate line")
        self.options_label = tk.Label(self.Select_Frame.sub_frame, height=1, text="Options")
        self.options_text = tk.Text(self.Select_Frame.sub_frame, height=3)
        self.name_label.grid(row=0, column=0, sticky='nsew')
        self.name_text.grid(row=0, column=1, sticky='nsew')
        self.options_label.grid(row=1, column=0, sticky='nsew')
        self.options_text.grid(row=1, column=1, sticky='nsew')
        self.example_label.grid(row=2, sticky='nsew')
        self.Select_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Select_Frame, self.name_label, self.example_label, self.options_label, self.options_text])

        global HTML_attr
        HTML_attr['name'] = self.name_text
        HTML_attr['options'] = self.options_text

    def add_Form(self, tag_type):

        self.add_Global_Attributes(tag_type)
        self.add_btn['command'] = lambda: self.addPreDefinedElement(tag_type)

        self.Form_Frame = ToggledFrame(self.canv, text='Form data', relief="flat", borderwidth=1)
        self.Form_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Form_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.type_label = tk.Label(self.Form_Frame.sub_frame, height=1,text="Type")
        self.type_text = ttk.Combobox(self.Form_Frame.sub_frame,values=['color', 'progress','button', 'checkbox','date', 'datetime-local', 'email','file', 'image', 'month','number', 'password', 'radio','search', 'tel','text', 'time', 'url','week'],state="readonly")
        self.others_label = tk.Label(self.Form_Frame.sub_frame, height=1, text="Other attributes")
        self.others_text = tk.Text(self.Form_Frame.sub_frame, height=3)
        self.type_label.grid(row=0, column=0, sticky='nsew')
        self.type_text.grid(row=0, column=1, sticky='nsew')
        self.others_label.grid(row=1, column=0, sticky='nsew')
        self.others_text.grid(row=1, column=1, sticky='nsew')
        self.Form_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Form_Frame, self.type_label, self.type_text,self.others_label,self.others_text])

        global HTML_attr
        HTML_attr['type'] = self.type_text
        HTML_attr['other'] = self.others_text

    def add_List(self, tag_type):

        self.add_Global_Attributes(tag_type)
        self.add_btn['command'] = lambda: self.addPreDefinedElement(tag_type)

        self.Lists_Frame = ToggledFrame(self.canv, text='Data', relief="flat", borderwidth=1)
        self.Lists_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Lists_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.items_hint_text = tk.Label(self.Lists_Frame.sub_frame, height=1,text="enter items with a comma (,) between them")
        self.items_label = tk.Label(self.Lists_Frame.sub_frame, text='Items', height=1, pady=2)
        self.items_text = tk.Text(self.Lists_Frame.sub_frame)
        self.items_hint_text.grid(row=0, column=0, sticky='nsew')
        self.items_label.grid(row=1, column=0, sticky='nsew')
        self.items_text.grid(row=1, column=1, sticky='nsew')
        self.Lists_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Lists_Frame, self.items_hint_text, self.items_label, self.items_text])

        global HTML_attr
        HTML_attr['items number'] = self.items_number_text
        HTML_attr['items'] = self.items_text

    def add_Progress_Bar(self, tag_type):

        self.add_Global_Attributes(tag_type)
        self.add_btn['command']= lambda : self.addPreDefinedElement(tag_type)

        self.Progress_Bar_Frame = ToggledFrame(self.canv, text='Data', relief="flat", borderwidth=1)
        self.Progress_Bar_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Progress_Bar_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.max_label = tk.Label(self.Progress_Bar_Frame.sub_frame, text='Max:', height=1, pady=2)
        self.max_text = tk.Text(self.Progress_Bar_Frame.sub_frame, height=1)

        self.value_label = tk.Label(self.Progress_Bar_Frame.sub_frame, text='Value', height=1, pady=2)
        self.vlaue_text = tk.Text(self.Progress_Bar_Frame.sub_frame, height=1)
        self.max_label.grid(row=0, column=0, sticky='nsew')
        self.max_text.grid(row=0, column=1, sticky='nsew')
        self.value_label.grid(row=1, column=0, sticky='nsew')
        self.vlaue_text.grid(row=1, column=1, sticky='nsew')
        self.Progress_Bar_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Progress_Bar_Frame, self.max_label, self.max_text, self.value_label,self.vlaue_text])

        global HTML_attr
        HTML_attr['max'] = self.max_text
        HTML_attr['value'] = self.vlaue_text


    def add_Embeded_Content(self, tag_type):

        self.add_Global_Attributes(tag_type)

        self.Image_Frame = ToggledFrame(self.canv, text='Data', relief="flat", borderwidth=1)
        self.Image_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Image_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.source_label = tk.Label(self.Image_Frame.sub_frame, text='Source:', height=1, pady=2)
        self.source_text = tk.Text(self.Image_Frame.sub_frame, height=1)

        self.alt_label = tk.Label(self.Image_Frame.sub_frame, text='alternative text:', height=1, pady=2)
        self.alt_text = tk.Text(self.Image_Frame.sub_frame, height=1)
        self.source_label.grid(row=0, column=0, sticky='nsew')
        self.source_text.grid(row=0, column=1, sticky='nsew')
        self.alt_label.grid(row=1, column=0, sticky='nsew')
        self.alt_text.grid(row=1, column=1, sticky='nsew')
        self.Image_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Image_Frame, self.source_label, self.source_text, self.alt_label,self.alt_text])

        global HTML_attr
        HTML_attr['src'] = self.source_text
        if tag_type == "img":
            HTML_attr['alt'] = self.alt_text
        elif tag_type == 'object' :
            self.alt_label['text']= 'Type:'
            HTML_attr['type'] = self.alt_text
            self.add_btn['command'] = lambda: self.addPreDefinedElement(tag_type)
        else:
            self.alt_label['text'] = 'Title:'
            HTML_attr['title'] = self.alt_text




    def add_Button(self, tag_type):

        self.add_Global_Attributes(tag_type)

        self.Callback_Frame = ToggledFrame(self.canv, text='Callback', relief="flat", borderwidth=1)
        self.Callback_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Callback_Frame.sub_frame.grid_rowconfigure(2, weight=1)
        self.onClick_label = tk.Label(self.Callback_Frame.sub_frame, text='onClick:', height=1, pady=2)
        self.onClick_text = tk.Text(self.Callback_Frame.sub_frame, height=1)
        self.btnType_label = tk.Label(self.Callback_Frame.sub_frame, text='Type:', height=1, pady=2)
        self.btnType_text = ttk.Combobox(self.Callback_Frame.sub_frame,values=['button', 'reset', 'submit'],state="readonly")
        self.onClick_label.grid(row=0, column=0, sticky='nsew')
        self.onClick_text.grid(row=0, column=1, sticky='nsew')
        self.btnType_label.grid(row=1, column=0, sticky='nsew')
        self.btnType_text.grid(row=1, column=1, sticky='nsew')
        self.Callback_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        global top_level_widgets
        top_level_widgets.extend(
            [self.Callback_Frame, self.onClick_label, self.onClick_text, self.btnType_label,self.btnType_text])

        global HTML_attr
        HTML_attr['type'] = self.btnType_text
        HTML_attr['onclick'] = self.onClick_text

    def add_Anchor(self, tag_type):

        self.add_Global_Attributes(tag_type)

        self.Href_Frame = ToggledFrame(self.canv, text='Reference', relief="flat", borderwidth=1)
        self.Href_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.Href_label = tk.Label(self.Href_Frame.sub_frame, text='Href:', height=1, pady=2)
        self.Href_text = tk.Text(self.Href_Frame.sub_frame, height=1)
        self.Href_label.grid(row=0, column=0, sticky='nsew')
        self.Href_text.grid(row=0, column=1, sticky='nsew')
        self.Href_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Href_Frame, self.Href_label, self.Href_text])

        global HTML_attr
        HTML_attr['href'] = self.Href_text



    def add_Global_Attributes(self,tag_type):
        print('add_H_P() selected ' + tag_type )
        self.CSS_frame.destroy()
        self.CSS_frame = tk.Frame(self.canv, relief="raised")
        self.CSS_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        if self.Dicesion_frame:
            self.Dicesion_frame.destroy()

        global HTML_attr
        HTML_attr.clear()
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
        # ------------------------------------Text-----------------------------------------------------

        self.Text_Frame = ToggledFrame(self.canv, text='Text', relief="flat", borderwidth=1)
        self.Text_Frame.sub_frame.grid_rowconfigure(1, weight=1)
        self.Text_Frame.sub_frame.grid_columnconfigure(2, weight=1)
        self.text_label = tk.Label(self.Text_Frame.sub_frame, text='Text:', height=1, pady=2)
        self.text_text = tk.Text(self.Text_Frame.sub_frame,height = 4)
        self.text_direction_label = tk.Label(self.Text_Frame.sub_frame, text='Direction:', height=1, pady=2)
        self.text_direction_text = tk.Text(self.Text_Frame.sub_frame)
        self.text_decoration_label = tk.Label(self.Text_Frame.sub_frame, text='Decoration:', height=1, pady=2)
        self.text_decoration_text = tk.Text(self.Text_Frame.sub_frame)
        self.text_overflow_label = tk.Label(self.Text_Frame.sub_frame, text='Overflow:', height=1, pady=2)
        self.text_overflow_text = ttk.Combobox(self.Text_Frame.sub_frame,values = ['hidden','clip','ellipsis','initial','inherit'],state="readonly")
        self.text_whiteSpace_label = tk.Label(self.Text_Frame.sub_frame, text='White space:', height=1, pady=2)
        self.text_whiteSpcae_text = ttk.Combobox(self.Text_Frame.sub_frame,values=['normal', 'pre', 'nowrap','pre-wrap' ,'pre-line','initial', 'inherit'],state="readonly")
        self.text_label.grid(row=0, column=0, sticky='nsew')
        self.text_text.grid(row=0, column=1, sticky='nsew')
        self.Text_Frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Text_Frame, self.text_label, self.text_direction_label, self.text_direction_text,
             self.text_decoration_label,
             self.text_decoration_text, self.text_overflow_label, self.text_overflow_text, self.text_whiteSpace_label,self.text_whiteSpcae_text])

    def setUp_Padding(self):
        # ------------------------------------Padding-----------------------------------------------------
        self.Padding_Frame = ToggledFrame(self.canv, text='Padding', relief="flat", borderwidth=1)
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

        global top_level_widgets
        top_level_widgets.extend(
            [self.Padding_Frame, self.padding_top_label, self.padding_top_text, self.padding_bottom_label, self.padding_bottom_text,
             self.padding_left_label, self.padding_left_text, self.padding_right_label, self.padding_right_text])

        global CSS_attr
        CSS_attr['padding-top:' ] = self.padding_top_text
        CSS_attr['padding-bottom:' ] = self.padding_bottom_text
        CSS_attr['padding-left:' ] = self.padding_left_text
        CSS_attr['padding-right:' ] = self.padding_right_text

    def setUp_Margin(self):
        # ------------------------------------Margin-----------------------------------------------------
        self.Margin_Frame = ToggledFrame(self.canv, text='Margin', relief="flat", borderwidth=1)
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

        global top_level_widgets
        top_level_widgets.extend(
            [self.Margin_Frame, self.margin_top_label, self.margin_top_text, self.margin_bottom_label, self.margin_bottom_text,
             self.margin_left_label, self.margin_left_text, self.margin_right_label, self.margin_right_text])

        global CSS_attr
        CSS_attr['margin-top:'] = self.margin_top_text
        CSS_attr['margin-bottom:'] = self.margin_bottom_text
        CSS_attr['margin-left:'] = self.margin_left_text
        CSS_attr['margin-right:'] = self.margin_right_text

    def setUp_Dicesion(self,add_elem,tag_type):
        # ------------------------------------Dicesion-----------------------------------------------------
        self.Dicesion_frame = tk.Frame(self.canv, relief="raised")
        self.Dicesion_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="s")
        self.add_btn = tk.Button(self.Dicesion_frame, text='ADD', relief="groove", justify='right',
                                 command=lambda: add_elem(tag_type))
        self.cancel_btn = tk.Button(self.Dicesion_frame, text='CANCEL', command=lambda: print('cancel'),
                                    relief="groove", justify='left')
        self.add_btn.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.cancel_btn.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        global top_level_widgets
        top_level_widgets.extend(
            [self.Dicesion_frame, self.add_btn, self.cancel_btn])

    def setUp_Font(self):
        # ------------------------------------Font-----------------------------------------------------
        self.Font_Frame = ToggledFrame(self.canv, text='Font', relief="flat", borderwidth=1)
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

        global top_level_widgets
        top_level_widgets.extend(
            [self.Font_Frame, self.font_family_label, self.font_family_text, self.font_size_label, self.font_size_text,
             self.font_style_label, self.font_style_text, self.font_weight_label, self.font_weight_text])

        global CSS_attr
        CSS_attr['font-family:'] = self.font_family_text
        CSS_attr['font-size:'] = self.font_size_text
        CSS_attr['font-style:'] = self.font_style_text
        CSS_attr['font-weight:'] = self.font_weight_text


    def setUp_Dimensions(self):
        # ------------------------------------Dimension-----------------------------------------------------
        self.Dimension_Frame = ToggledFrame(self.canv, text='Dimensions', relief="flat", borderwidth=1)
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

        global top_level_widgets
        top_level_widgets.extend(
            [self.Dimension_Frame, self.height_label, self.height_text, self.width_label, self.width_text,
             self.max_height_label, self.max_height_text, self.max_width_label, self.max_width_text, self.min_height_label,
             self.min_height_text, self.min_width_label,self.min_width_text])

        global CSS_attr
        CSS_attr['height:'] = self.height_text
        CSS_attr['width:'] = self.width_text
        CSS_attr['max-height:'] = self.max_height_text
        CSS_attr['max_width:'] = self.max_width_text
        CSS_attr['min-height:'] = self.min_height_text
        CSS_attr['min-width:'] = self.min_width_text

    def setUp_Border(self):   # work in progress
        # ------------------------------------Border-----------------------------------------------------
        self.Border_Frame = ToggledFrame(self.canv, text='Border', relief="flat", borderwidth=1)
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

        global top_level_widgets
        top_level_widgets.extend(
            [self.Border_Frame, self.Border_hint_label, self.Border_top_label, self.Border_top_text, self.Border_bottom_label,
             self.Border_bottom_text, self.Border_left_label, self.Border_left_text, self.Border_right_label, self.Border_right_text,
             self.Border_4way_label, self.Border_4way_text])

        global CSS_attr
        CSS_attr['border-color:'] = self.Border_4way_text
        CSS_attr['border-top:'] = self.Border_top_text
        CSS_attr['border-bottom:'] = self.Border_bottom_text
        CSS_attr['border-right:'] = self.Border_right_text
        CSS_attr['border-left:'] = self.Border_right_text


    def setUp_Background(self):
        # ------------------------------------Background-----------------------------------------------------
        self.Background_Frame = ToggledFrame(self.canv, text='Background', relief="flat", borderwidth=1)
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

        global top_level_widgets
        top_level_widgets.extend(
            [self.Background_Frame, self.bg_color_label, self.bg_color_text, self.bg_img_label, self.bg_img_text,self.bg_pos_label,self.bg_pos_text])

        global CSS_attr
        CSS_attr['background-color:'] = self.bg_color_text
        CSS_attr['background-image:'] = self.bg_img_text


    def setUp_Identity(self):
        # ---------------------------------Identity-----------------------------------------------------
        self.identity_Frame = ToggledFrame(self.canv, text='Identity', relief="flat", borderwidth=1)
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

        global HTML_attr
        HTML_attr['id'] = self.id_text
        HTML_attr['class'] = self.class_text

        global top_level_widgets
        top_level_widgets.extend(
            [self.identity_Frame, self.id_label, self.class_label, self.class_text, self.hidden_label,self.Hidden_text,self.id_text])

    def onselect_subcomponent(self, event):  # define diffrent functions for every element type

        # print('onselect_subcomponent() selected ' + self.sub_components.get(self.sub_components.curselection()))
        global top_level_widgets
        for widget in top_level_widgets:
            widget.destroy()
        top_level_widgets.clear()
        self.create_options()

        if self.components.get(self.components.curselection()) == 'Headings and Paragragraphs':
            self.add_Global_Attributes(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.sub_components.get(self.sub_components.curselection()) == 'Text Area':
            self.add_Global_Attributes(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.components.get(self.components.curselection()) == 'Lists':
            self.add_List(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.sub_components.get(self.sub_components.curselection()) == 'Anchor element - <a>':
            self.add_Anchor(HTML_sub_Components_names['Anchor element - <a>'])
        if self.sub_components.get(self.sub_components.curselection()) == 'Button':
            self.add_Button(HTML_sub_Components_names['Button'])
        if self.components.get(self.components.curselection()) == 'Embeded content' :
            self.add_Embeded_Content(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.sub_components.get(self.sub_components.curselection()) == 'Progress bar':
            self.add_Progress_Bar(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.sub_components.get(self.sub_components.curselection()) == 'Object':
            self.add_Embeded_Content(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.sub_components.get(self.sub_components.curselection()) == 'Input -(form)':
            self.add_Form(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])
        if self.sub_components.get(self.sub_components.curselection()) == 'Select':
            self.add_Select(HTML_sub_Components_names[self.sub_components.get(self.sub_components.curselection())])



    def onselect_component(self,event):

        self.sub_components.delete(0, tk.END)
        if self.components.get(self.components.curselection()) == 'Headings and Paragragraphs':
            self.sub_components.insert(1, 'Heading 1', 'Heading 2', 'Heading 3','Heading 4','Heading 5','Heading 6', 'Paragraph','Label')
        if self.components.get(self.components.curselection()) == 'Lists':
            self.sub_components.insert(1, 'Ordered list', 'UnOrdered list')
        if self.components.get(self.components.curselection()) == 'Embeded content':
            self.sub_components.insert(1, 'Audio', 'Canvas','Image','Picture','Video','iframe')
        if self.components.get(self.components.curselection()) == 'Interactive content':
            self.sub_components.insert(1, 'Button', 'Text Area', 'Anchor element - <a>', 'Input -(form)', 'Select', 'Progress bar','Object')

    def create_widgets(self):

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



    def create_options(self):
        self.canv = tk.Canvas(self.options_window,bg = 'green')
        self.Optionsscrollbar = tk.Scrollbar(self.options_window,command = self.canv.yview)
        # self.Optionsscrollbar.config(command=self.canv)
        self.canv.config(yscrollcommand = self.Optionsscrollbar.set,scrollregion=self.canv.bbox("all"))
        self.canv.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.Optionsscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.CSS_frame = tk.Frame(self.canv,relief="raised")
        self.CSS_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.Dicesion_frame = tk.Frame(self.canv, relief="raised")
        self.Dicesion_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="s")

        global top_level_widgets
        top_level_widgets.extend([self.canv,self.Optionsscrollbar,self.CSS_frame,self.Dicesion_frame])



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
        attributes = ''
        global HTML_attr
        global CSS_attr


        for attr in CSS_attr.keys():
            if len(CSS_attr[attr].get("1.0",tk.END).strip()) != 0:
                style = ''.join([style,attr,CSS_attr[attr].get("1.0",tk.END).strip(),';'])
        style= style + '"'

        for attr in HTML_attr.keys():
            # if attr == 'onclick':
            #     attributes = ''.join([attributes, attr, '="', HTML_attr[attr].get("1.0", tk.END).strip(), '" '])
            if HTML_attr[attr].winfo_class() != 'TCombobox':
                if len(HTML_attr[attr].get("1.0", tk.END).strip()) != 0:
                    attributes = ''.join([attributes, attr, '="', HTML_attr[attr].get("1.0", tk.END).strip(), '" '])
            else:
                if len(HTML_attr[attr].get().strip()) != 0:
                    attributes = ''.join([attributes, attr, '="', HTML_attr[attr].get().strip(), '" '])

        if tag == 'audio':
            attributes = ''.join(['controls ',attributes])


        add_styles = lambda style:style if style != 'style =" "' else ''

        tag1 = "<"+ tag+' ' + attributes +' '+add_styles(style)+ '>'+self.text_text.get('1.0',tk.END) +"</" + tag +">\n"
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


    def addPreDefinedElement(self, tag):

        with open(url, 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        cnt = 0
        for line in data:
            if line.find('<body>') != -1:
                break;
                print('found it')
            cnt = cnt + 1

        style = ' style =" '
        attributes = ''
        global HTML_attr
        global CSS_attr
        global HTML_ready_code

        for attr in CSS_attr.keys():
            if len(CSS_attr[attr].get("1.0",tk.END).strip()) != 0:
                style = ''.join([style,attr,CSS_attr[attr].get("1.0",tk.END).strip(),';'])
        style= style + '"'
        add_styles = lambda style:style if style != 'style =" "' else ''

        code = str('')
        code = HTML_ready_code[tag]

        if tag == 'ol' or tag == 'ul':
            items = str('')
            items = HTML_attr['items'].get("1.0", tk.END).strip()
            items_list = items.split(',')

            for item in items_list:
                if tag == 'ul':
                    code = code[:code.find('<ul>') + len('<ul>')] +'<li>'+item+'</li>' + code[code.find('<ul>') + len('<ul>'):]
                else:
                    code = code[:code.find('<ol>') + len('<ol>')] + '<li>' + item + '</li>' + code[code.find('<ol>') + len('<ol>'):]
            code = code[:code.find('>') ] + add_styles(style) + code[code.find('>') :]

        if tag == 'progress':
            code = code[:code.find('<label for="">') + len('<label for="">')] + self.text_text.get('1.0',tk.END) + code[ code.find('<label for="">') + len('<label for="">'):]
            code = code[:code.find('for=""') + len('for=""')] + add_styles(style) + code[code.find('for=""') + len('for=""'):]
            code = code[:code.find('for="') + len('for="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('for="') + len('for="'):]
            code = code[:code.find('id="') + len('id="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('id="') + len('id="'):]
            code = code[:code.find('value="') + len('value="')] + HTML_attr['value'].get("1.0", tk.END).strip() + code[code.find( 'value="') + len('value="'):]
            code = code[:code.find('max="') + len('max="')] + HTML_attr['max'].get("1.0", tk.END).strip() + code[code.find('max="') + len('max="'):]

        if tag == 'object':
            code = code[:code.find('<object ') + len('<object ')] + add_styles(style) + code[code.find('<object ') + len('<object '):]
            code = code[:code.find('type="') + len('type="')] + HTML_attr['type'].get("1.0", tk.END).strip() + code[code.find('type="') + len('type="'):]
            code = code[:code.find('data="') + len('data="')] + HTML_attr['src'].get("1.0", tk.END).strip() + code[code.find('data="') + len('data="'):]
        if tag == 'input':
            code = code[:code.find('<label for="">') + len('<label for="">')] + self.text_text.get('1.0',tk.END) + code[code.find('<label for="">') + len('<label for="">'):]
            code = code[:code.find('<input ') + len('<input ')] + add_styles(style) + code[code.find('<input ') + len('<input '):]
            code = code[:code.find('type="') + len('type="')] + HTML_attr['type'].get().strip() + code[code.find('type="') + len('type="'):]
            code = code[:code.find('id="') + len('id="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('id="') + len('id="'):]
            code = code[:code.find('for="') + len('for="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('for="') + len('for="'):]
            code = code[:code.find('name="') + len('name="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('name="') + len('name="'):]
            code = code[:code.find('required ') + len('required ')] + HTML_attr['other'].get("1.0", tk.END).strip() + code[code.find('required ') + len('required '):]

        if tag == 'select':
            options = HTML_attr['options'].get("1.0", tk.END).strip()
            options_list = options.split('\n')
            code_to_add = ''
            for option in options_list:
                code_to_add =code_to_add+'<option value="'+ option.split(' ')[0]+'">'+ option.split(' ')[1]+'</option>\n'

            code = code[:code.find('<option value="">--Please choose an option--</option>') + len('<option value="">--Please choose an option--</option>')]\
                   + code_to_add+ code[code.find('<option value="">--Please choose an option--</option>') + len('<option value="">--Please choose an option--</option>'):]
            code = code[:code.find('for="') + len('for="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('for="') + len('for="'):]
            code = code[:code.find('id="') + len('id="')] + HTML_attr['id'].get("1.0", tk.END).strip() + code[code.find('id="') + len('id="'):]
            code = code[:code.find('name="') + len('name="')] + HTML_attr['name'].get("1.0", tk.END).strip() + code[code.find('name="') + len('name="'):]

        data.insert(cnt + 1, """                    """ +code)

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
                    <meta name = "description" content = "pySIteBuilder">
                    <meta name = "author" content = "Tony Nekola">
                    <link rel = "stylesheet" href = "css/styles.css?v=3.0">

                    <title>The HTML5 Herald</title>
                </head>

                <body>
                    <h1>This site is created in python</h1>
                    
                    <h2>Author: Tony Nekola</h2>
                </body>
                </html>""")


    f.close()


    # HtmlViewer =HTMLViewer()
    root = tk.Tk()
    app = Application(None,master=root)
    app.mainloop()


if __name__ == "__main__":
    main()