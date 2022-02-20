from tkinter import *
from PIL import ImageTk, Image
from time import sleep
from glob import glob
from itertools import cycle

class MainApplication:
	def __init__(self, root):
		self.root = root
		root.title("Title Scanner")

		self.width, self.height = 500, 500 #root.wibnfo_screenwidth(), root.winfo_screenheight()
		self.resize_tuple = (400, 400)

		self.canv = Canvas(self.root, width=self.width, height=self.height, bg='black')
		self.canv.grid(row=0, column=0)

		self.name_entry = Entry(self.root, width=50, textvariable='Rename', font=('calibre', 10, 'normal'))
		self.name_entry.grid(row=0,column=1)

		self.root.bind('<Return>', self.ENTER_event)
		self.done = False

		self.get_photo_paths()
		self.display_photo()
		# Allow user to type a new name for the photo.

		# Notify the User when they've renamed every photo.	

	def get_photo_paths(self): # Returns a list of photos you can cycle through.
		photo_list = glob('../images/*.jpg')
		self.initial = photo_list[0]
		self.photo_cycle = cycle(_ for _ in photo_list)

	def display_photo(self):
		current_photo = next(self.photo_cycle)
		if current_photo == self.initial:
			if not self.done:
				self.done = True
			else:
				self.done_window()
		print(current_photo)
		self.load_next_image(current_photo)

	def load_next_image(self, img_path): # So you can see the image you're renaming.
		photo = Image.open(img_path)
		#img_width, img_height = photo.size
		resized_photo = photo.resize(self.resize_tuple, Image.ANTIALIAS)
		global img
		img = ImageTk.PhotoImage(resized_photo)  # PIL solution
		self.canv.create_image(20, 20, anchor=NW, image=img)

	def done_window(self):
		newWindow = Toplevel(self.root)
		newWindow.title("New Window")
		newWindow.geometry("200x200")
		Label(newWindow, text="This is a new window").pack()

	def ENTER_event(self, event): # Rename the target photo when the enter key is pressed.
		# shutil.move(input, output + str(user_input))
		self.display_photo()
		print(self.name_entry.get())
		print("You hit return.")

if __name__ == "__main__":
	root = Tk()
	MainApplication(root)

	# LET THE USER PICK AN ANGLE, THEN JUST USE IMAGEMAGIC
	mainloop()