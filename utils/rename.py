# 2022-02-22 rename.py
# Carson Weaver
# GUI for rotating test set photos.

# Many of the leaf images for this project are roatated at odd angles.
# This complicates the PCA analysis beyond the scope of the project.
# This tool allows users to quickly rotate their test images for for more efficient training.

from tkinter import *
from PIL import ImageTk, Image
from time import sleep
from glob import glob
from itertools import cycle

class MainApplication:
	def __init__(self, root):
		self.root = root
		root.title("Photo Rotator")

		self.width, self.height = 650, int(445)

		self.canv = Canvas(self.root, width=self.width, height=self.height, bg='black')
		self.canv.grid(row=0, column=0)

		self.name_entry = Entry(self.root, width=50, textvariable='Rename', font=('calibre', 10, 'normal'))
		self.name_entry.grid(row=0,column=1)

		self.root.bind('<Return>', self.ENTER_event)
		self.done = False

		self.init_photo_viewer()
		self.next_photo_viewer()

	def init_photo_viewer(self): # Returns a list of photos you can cycle through.
		photo_list = glob('../images/*.jpg')
		self.initial = photo_list[0]
		self.photo_cycle = cycle(_ for _ in photo_list)

	def next_photo_viewer(self):
		current_photo = next(self.photo_cycle)
		
		# Check if you've gone through everything.
		if current_photo == self.initial:
			if not self.done:
				self.done = True
			else:
				self.done_window()

		# Load image to Tkinter interface.
		photo = Image.open(current_photo)
		resized_photo = photo.resize((200,200), Image.ANTIALIAS)

		# TODO: Overlay protractor on image.
		chart = Image.open('degree_chart.jpg')
		resized_chart = chart.resize((int(1.5*450),450), Image.ANTIALIAS)

		resized_chart.paste(resized_photo, (230, 140))
		# Convert the Image object into a TkPhoto object
		#tkimage = ImageTk.PhotoImage(imageHead)

		# panel1 = Label(self.root, image=tkimage)
		# panel1.grid(row=0, column=2, sticky=E)

		global img
		img = ImageTk.PhotoImage(resized_chart)  # PIL solution
		self.canv.create_image(0, 0, anchor=NW, image=img)

	def done_window(self):
		newWindow = Toplevel(self.root)
		newWindow.title("New Window")
		newWindow.geometry("200x200")
		Label(newWindow, text="All photos have been rotated.").pack()

	def ENTER_event(self, event): # Rename the target photo when the enter key is pressed.
		# TODO save rotated image on enter
		# TODO crop rotated image to standardized size
		
		self.next_photo_viewer()
		print(self.name_entry.get())
		print("You hit return.")

if __name__ == "__main__":
	root = Tk()
	MainApplication(root)
	mainloop()
