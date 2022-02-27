# 2022-02-22 rename.py
# Carson Weaver
# GUI for rotating test set photos.

# Many of the leaf images for this project are roatated at odd angles.
# This complicates the PCA analysis beyond the scope of the project.
# This tool allows users to quickly rotate their test images for for more efficient training.
# Requires that imagemagick be added to path on windows.

from tkinter import *
from PIL import ImageTk, Image
from glob import glob
from itertools import cycle
from math import atan, pi
from os import system
from os.path import basename
from pathlib import Path

class MainApplication:
	def __init__(self, root):
		root.title("Photo Rotator")
		
		# Parameters.
		self.width, self.height, self.pane_width= 810, 593, 30
		self.target_pattern = '../raw_images/*.png'
		self.dest_path = Path("../data")
		self.scale_factor = 0.4
		self.done = False

		# Initialize the script that'll contain your imagemagick commands.
		with open("process_photos.bat", 'w') as file:
			file.write("echo START SCRIPT\n")

		# Draw photo viewer box.
		self.viewer = Canvas(root, width=self.width, height=self.height, bg='black')
		self.viewer.grid(row=0, column=0)
		
		# Get your list of photos to process.
		photo_list = glob(self.target_pattern)
		self.initial = photo_list[0]
		self.photo_cycle = cycle(_ for _ in photo_list)

		self.display_next_photo(root)

		root.bind('<Button 1>', self.CLICK_event)

	def display_next_photo(self, root): # Load next image to screen, including any over/underlays.
		self.current_photo = next(self.photo_cycle)
		
		# Check if you've gone through everything.
		if self.current_photo == self.initial:
			if not self.done:
				self.done = True
			else:
				self.run_script(root)
				root.destroy()

		# Overlay image on protractor.
		chart = Image.open('degree_chart.jpg')
		photo = Image.open(self.current_photo)

		# Fix resizing so photos aren't distorted, but also squared up.
		if photo.size[0] >= photo.size[1]:
			ratio = self.scale_factor * chart.size[0] / photo.size[0]
			resize_tuple = (int(self.scale_factor * chart.size[0]), int(ratio * photo.size[1]))
		else:
			ratio = self.scale_factor * chart.size[0] / photo.size[1]
			resize_tuple = (int(ratio * photo.size[0]), int(self.scale_factor * chart.size[0]))

		# Paste photo to the middle of your chart.
		resized_photo = photo.resize(resize_tuple, Image.ANTIALIAS)
		chart.paste(resized_photo, (int(self.width/2 - resize_tuple[0]/2), int(self.height/2 - resize_tuple[1]/2)))

		# Blit to GUI.
		self.img = ImageTk.PhotoImage(chart)
		self.viewer.create_image(0, 0, anchor=NW, image=self.img)

	def CLICK_event(self, event):
		# Get coords of cursor relative to frame center.
		x = event.x - (self.width/2)
		y = (self.height/2) - event.y
		
		try:
			self.angle = atan(y / x)*(180/pi) 
		except ZeroDivisionError:
			self.angle = atan((y+0.01) / (x+0.01))*(180/pi)

		# Adjust for the weirdness of the arctan function.
		if x < 0 and y > 0:
			self.angle = 180 + self.angle
		elif x < 0 and y < 0:
			self.angle = 180 + self.angle
		elif x > 0 and y < 0:
			self.angle = self.angle + 90 + 270

		self.angle = round(self.angle, 2)

		# Save image rotation command.
		new_name = Path(self.dest_path, basename(self.current_photo))
		command_string = f"magick convert -background 'rgba(0,0,0,0)' -rotate {self.angle-90} {self.current_photo} {new_name}\n"
		with open("process_photos.bat", "a") as file:
			file.write(command_string)
		
		self.display_next_photo(root)

	def run_script(self, root):
		with open("process_photos.bat", "a") as file:
			file.write("exit")

		system(f"start cmd /k process_photos.bat")
		print(Path.resolve(self.dest_path))
		system(f"start {Path.resolve(self.dest_path)}")

if __name__ == "__main__":
	root = Tk()
	MainApplication(root)
	mainloop()
