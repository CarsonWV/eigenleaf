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
from math import atan, pi
from os import system
from os.path import basename
from statistics import mean
from pathlib import Path

class MainApplication:
	def __init__(self, root):
		self.root = root
		root.title("Photo Rotator")
		
		# Parameters.
		self.scale_factor = 0.4
		self.width, self.height, self.pane_width= 810, 593, 30
		self.dest_path = "../data"
		self.done = False

		# Draw photo viewer box.
		self.canv = Canvas(self.root, width=self.width, height=self.height, bg='black')
		self.canv.grid(row=0, column=0)

		# Draw entry box.
		self.name_entry = Entry(self.root, width= self.pane_width, textvariable='Rename', font=('calibre', 10, 'normal'))
		self.name_entry.grid(row=0,column=1)

		self.root.bind('<Return>', self.ENTER_event)
		self.root.bind('<Button 1>', self.CLICK_event)

		self.init_photo_viewer()
		self.next_photo_viewer()

	def init_photo_viewer(self): # Fetch the list of photos.
		photo_list = glob('../images/*.jpg')
		#photo_list = glob("C:\\Users\\carso\\Pictures\\2012-2013 Actual Pictures\\*.jpg")
		self.initial = photo_list[0]
		self.photo_cycle = cycle(_ for _ in photo_list)

	def next_photo_viewer(self): # Load next image to screen, including any over/underlays.
		self.current_photo = next(self.photo_cycle)
		
		# Check if you've gone through everything.
		if self.current_photo == self.initial:
			if not self.done:
				self.done = True
			else:
				self.done_window()

		# Overlay image on protractor.
		chart = Image.open('degree_chart.jpg')
		photo = Image.open(self.current_photo)

		if photo.size[0] >= photo.size[1]:
			# Fix resizing so photos aren't distorted, but also squared up.
			ratio = self.scale_factor * chart.size[0] / photo.size[0]
			resize_tuple = (int(self.scale_factor * chart.size[0]), int(ratio * photo.size[1]))
		else:
			# Fix resizing so photos aren't distorted, but also squared up.
			ratio = self.scale_factor * chart.size[0] / photo.size[1]
			resize_tuple = (int(ratio * photo.size[0]), int(self.scale_factor * chart.size[0]))
		
		resized_photo = photo.resize(resize_tuple, Image.ANTIALIAS)

		# Paste in the middle of the chart.
		chart.paste(resized_photo, (int(self.width/2 - resize_tuple[0]/2), int(self.height/2 - resize_tuple[1]/2)))
		resized_chart = chart

		global img
		img = ImageTk.PhotoImage(resized_chart)  # PIL solution
		self.canv.create_image(0, 0, anchor=NW, image=img)

	def done_window(self):
		newWindow = Toplevel(self.root)
		newWindow.title("All Done!")
		newWindow.geometry("200x200")
		Label(newWindow, text="All photos have been rotated.").pack()

	def CLICK_event(self, event):
		x = event.x
		y = event.y

		x = x - (self.width/2)
		y = (self.height/2) - y
		print(x, y)
		
		try:
			self.angle = atan(y / x)*(180/pi) 
		except ZeroDivisionError:
			self.angle = atan((y+0.01) / (x+0.01))*(180/pi)

		if x < 0 and y > 0:
			self.angle = 180 + self.angle
		elif x < 0 and y < 0:
			self.angle = 180 + self.angle
		elif x > 0 and y < 0:
			self.angle = self.angle + 90 + 270

		self.angle = round(self.angle, 2)
		print(self.angle)

		# TODO save rotated image on enter
		new_name = Path(self.dest_path, 'ROTATED_' + str(basename(self.current_photo)))
		command_string = f"magick convert -background 'rgba(0,0,0,0)' -rotate {self.angle-90} {self.current_photo} {new_name}"
		print(command_string)
		system(command_string)
		self.next_photo_viewer()

	def ENTER_event(self, event): # Rename the target photo when the enter key is pressed.
		
		self.next_photo_viewer()
		print(self.name_entry.get())
		print("You hit return.")

if __name__ == "__main__":
	root = Tk()
	MainApplication(root)
	mainloop()
