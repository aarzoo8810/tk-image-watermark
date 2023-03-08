import os
from tkinter import *
from tkinter import filedialog, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WaterMark:
    def __init__(self) -> None:
        self.background = "#2A2E32"
        BTN_BG = "black"
        opened_img = None
        img_to_save = None
        self.fixed_height = 400
        self.home_dir = os.path.expanduser("~")

        self.window = Tk()
        self.window.title("Not Your Image")
        self.window.geometry("1200x950")
        self.window.configure(bg=self.background)\

        self.frame1 = Frame(self.window, bg=self.background, padx=30, pady=30)
        self.frame1.pack(side=LEFT, fill=BOTH)

        self.show_image = Button(self.frame1,
                                 text="Pick an Image",
                                 command=self.display_img, width=40)
        self.show_image.grid(column=0, row=0, pady=3, columnspan=2)
        self.show_image.focus()

        self.watermark_text_label = Label(self.frame1,
                                          text="Enter Watermark Text: ",
                                          bg=self.background, fg="white")
        self.watermark_text_label.grid(column=0, row=1)

        self.watermark_text = Entry(self.frame1, textvariable=Text, bg="white")
        self.watermark_text.grid(column=1, row=1, pady=10)

        watermark_text_color = Label(
            self.frame1, text="Pick_color: ", bg=self.background, fg="white")
        watermark_text_color.grid(column=0, row=2)

        self.pick_color = Button(self.frame1,
                                 text="Pick a Color",
                                 bg=self.background,
                                 command=self.choose_color,
                                 activebackground=self.background,
                                 activeforeground="white",
                                 width=17)
        self.pick_color.grid(column=1, row=2, pady=5)

        self.watermark_text_size_label = Label(self.frame1,
                                               text="Size of Watermark: ",
                                               bg=self.background,
                                               fg="white")
        self.watermark_text_size_label.grid(column=0, row=3)

        self.watermark_text_size = Entry(self.frame1,
                                         textvariable=Text,
                                         bg="white")
        self.watermark_text_size.grid(column=1, row=3)

        self.watermark_text_coordinates_label = Label(self.frame1,
                                                      text="Coordinations of watermark: ",
                                                      bg=self.background,
                                                      fg="white")
        self.watermark_text_coordinates_label.grid(column=0, row=4, pady=8)

        self.watermark_text_x = Entry(self.frame1,
                                      textvariable=Text,
                                      bg="white")
        self.watermark_text_x.grid(column=1, row=4)
        self.watermark_text_x.insert(0, "x")

        self.watermark_text_y = Entry(self.frame1,
                                      textvariable=Text,
                                      bg="white")
        self.watermark_text_y.grid(column=1, row=5)
        self.watermark_text_y.insert(0, "y")

        self.img_scrollbar = Scrollbar(self.window, background=self.background)
        self.img_scrollbar.pack(side=RIGHT, fill=Y)

        self.frame2 = Frame(self.window, bg=self.background, padx=30, pady=30)
        self.frame2.pack(fill=BOTH, side=LEFT)

        self.preview_image = Button(
            self.frame1, text="preview image", command=self.process_img)
        self.preview_image.grid(column=0, row=6, columnspan=2, pady=8)

        self.window.mainloop()

    def choose_color(self):
        """This functions for taking values of colors in (r, g, b, a) format"""
        color = colorchooser.askcolor()
        r = color[0][0]
        g = color[0][1]
        b = color[0][2]
        a = int(simpledialog.askinteger(title="How transparent text should be?",
                                        prompt="Enter a number from 1 to to 10 for full transparency: ",
                                        minvalue=1,
                                        maxvalue=10) * 25.6)

        picked_color = (r, g, b, a)
        self.pick_color.config(text=picked_color, bg=color[1])

    def display_img(self):
        """this function lets you pick an image and displays it in interface"""
        global opened_img, img

        image_name = filedialog.askopenfile(initialdir=self.home_dir,
                                            title="pick an image",
                                            filetypes=[("images", ".png")]
                                            ).name
        opened_img = Image.open(fp=image_name)

        # find what percent of the height we are subtracting,
        # then subtract that percentage from the width
        width, height = (int((opened_img.size[0]/100) * ((self.fixed_height / opened_img.size[1]) * 100)),
                         self.fixed_height)
        img = ImageTk.PhotoImage(opened_img.resize((width, height)))

        img_label = Label(self.frame2,
                          image=img,
                          bg=self.background)
        img_label.grid(column=0, row=0, pady=5)

    # function for watermarking Image

    def process_img(self):
        """this function will take an image and watermark it"""
        global out_img, img_to_save

        text = self.watermark_text.get()
        color = tuple([int(num)
                      for num in self.pick_color.cget("text").split(" ")])
        size = int(self.watermark_text_size.get())
        x = int(self.watermark_text_x.get())
        y = int(self.watermark_text_y.get())

        # make a blank transparent image for text
        txt = Image.new("RGBA", opened_img.size, (255, 255, 255, 0))
        # get a font
        fnt = ImageFont.truetype("DejaVuSerif-Bold", size=size)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        # draw text half opacity
        d.text((x, y), text=text, font=fnt, fill=color)
        open_img = Image.alpha_composite(opened_img.convert("RGBA"), txt)

        img_to_save = open_img

        # find what percent of the height we are subtracting,
        # then subtract that percentage from the width
        width, height = (int((open_img.size[0]/100) * ((self.fixed_height / open_img.size[1]) * 100)),
                         self.fixed_height)

        out_img = ImageTk.PhotoImage(image=open_img.resize((width, height)))

        img_out = Button(self.frame2,
                         image=out_img,
                         bg=self.background,
                         borderwidth=0,
                         command=open_img.show,
                         activebackground=self.background
                         )
        img_out.grid(column=0, row=1, pady=15)

        save_img = Button(self.frame2, text="Save Image", bg=self.background,
                          borderwidth=0, command=self.save_image)
        save_img.grid(column=0, row=2)

    def save_image(self):
        """"this function will show you file browser to save image as"""
        file_name = filedialog.asksaveasfilename(
            initialdir=self.home_dir, filetypes=[("image", ".png")])
        img_to_save.save(file_name)
