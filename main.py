from tkinter import *
import tkinter.scrolledtext as scrolltext
from tkinter import filedialog , END,  messagebox
from tkinter.filedialog import askopenfilename
import PIL.Image
from PIL import Image , ImageTk , ImageDraw
import pytesseract
import numpy

pytesseract.pytesseract.tesseract_cmd = 'C://Users//Mr-Robot//Desktop//Image2Text//Tesseract-OCR/tesseract'

main_window = Tk()
main_window.title("Image2Text")
main_window.iconbitmap('icon.ico')
frame1 = Frame(main_window)
textArea = scrolltext.ScrolledText(main_window,height=1000,width=500)
textArea.insert(INSERT,"Here your Text will appear")


def Imaging_2_Text(text):
    textArea.delete('1.0', END)
    textArea.insert(INSERT,text)

def binarize_image(image):
    image = image.convert('L')
    image = numpy.array(image)
    image = binarize_array(image)

    im = Image.fromarray(image)
    return im


def binarize_array(numpy_array):
    for k in range(100,230):
        countb = 0
        countw = 0
        numpy_array2 = numpy_array
        for i in range(len(numpy_array)):
            for j in range(len(numpy_array[0])):
                if numpy_array[i][j] >k:
                    numpy_array2[i][j] = 255
                    countb+=1
                else:
                    numpy_array2[i][j] = 0
                    countw+=1
        if countb>=(len(numpy_array)/2.5):
            break
    return numpy_array2


class app(Frame):
    def __init__(self,master):
        Frame.__init__(self,master=None)
        self.x = self.y = 0
        self.bounding_box = []
        self.textmain = ''
        self.frame1 = Frame(self)
        self.frame2 = Frame(self)
        self.frame3 = Frame(self)
        self.button_for_open = Button(self.frame1,text="ADD",command=self.OpenFile,height = 2, width = 20)
        self.button_for_process = Button(self.frame1,text="PROCESS IMAGE",command=self.ProcessImage,height = 2, width = 20)
        self.button_for_remove = Button(self.frame1,text="REMOVE IMAGE",command=self.clear_images,height = 2, width = 20)
        self.button_for_remove_box = Button(self.frame1,text="REMOVE BOXES",command=self.remove_box,height = 2, width = 20)
        self.button_for_open.grid(row=1,column=0,sticky=W, padx=10, pady=10)
        self.button_for_process.grid(row=2,column=0,sticky=W, padx=10, pady=10)
        self.button_for_remove.grid(row=3,column=0,sticky=W, padx=10, pady=10)
        self.button_for_remove_box.grid(row=4,column=0,sticky=W, padx=10, pady=10)
        self.im = PIL.Image.open("newadd.png")
        self.original_image = self.im
        self.im = self.im.resize((500,1000), Image.ANTIALIAS)
        self.canvas = Canvas(self.frame2,  cursor="cross",width=500, height=1000)
        self.canvas.grid(row=0,column=2)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.draw = ImageDraw.Draw(self.im)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
        self.frame1.grid(row=0,column=0,stick=E)
        self.frame2.grid(row=0,column=1)
        self.frame3.grid(row=0,column=2)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.draw.rectangle((self.start_x, self.start_y, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)), fill=None, outline="red")
        self.bounding_box.append([self.start_x, self.start_y, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)])
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
        pass

    def OpenFile(self):
        try:
            filename = askopenfilename(filetypes =(("Jpeg Files","*.jpeg" "*.jpg"),("Png Files", "*.png"),("All Files","*.*")),
                                   title = "Choose an Image.")
            self.im = Image.open(filename)
            self.original_width = self.im.width
            self.original_height = self.im.height
            self.original_image_unsized = self.im
            self.im = self.im.resize((500,1000), Image.ANTIALIAS)
            self.original_image = self.im
            self.bounding_box = []
            self.draw = ImageDraw.Draw(self.im)
            self.tk_im = ImageTk.PhotoImage(self.im)
            self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
        except:
            flag=1

    def ProcessImage(self):
        if self.bounding_box==0:
            imx = binarize_image(self.original_image)
            self.textmain = self.textmain+pytesseract.image_to_string(imx) +'\n\n\n'
        else:
            for x in self.bounding_box:
                #imx = self.im.crop()
                imx = self.original_image_unsized.crop((int((x[0]/500)*self.original_width),int((x[1]/1000)*self.original_height),int((x[2]/500)*self.original_width),int((x[3]/1000)*self.original_height)))
                imx = binarize_image(imx)
                self.textmain = self.textmain+pytesseract.image_to_string(imx) +'\n\n\n'
        Imaging_2_Text(self.textmain)

    def quit(self):
        self.root.destroy()

    def remove_box(self):
        self.bounding_box = []
        self.tk_im = ImageTk.PhotoImage(self.original_image)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

    def save_file(self):
        file = filedialog.asksaveasfile(mode='w')
        if file!=None:
            data = textArea.get('1.0',END+'-1c')
            file.write(data)
            file.close()

    def clearScreen(self):
        textArea.delete('1.0', END)

    def clear_images(self):
        self.im = Image.open('addnew.png')
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

app = app(frame1)
app.pack(side=LEFT)
textArea.pack(side=RIGHT)

main_window.mainloop()
