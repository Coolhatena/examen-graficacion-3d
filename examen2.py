import math
import tkinter as tk
import graflib as gl
from PIL import Image, ImageTk
from cube import Cubo

class rootApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self._frame = None
		self.switch_frame(StartPage)

	def switch_frame(self, frame_class):
		# Destroys current frame and replaces it with a new one.
		new_frame = frame_class(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()


class StartPage(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		leftSide = tk.Frame(self)
		rightSide = tk.Frame(self)
		figureControllers = tk.LabelFrame(rightSide, text="Figura")
		cameraControllers = tk.LabelFrame(rightSide, text="Camara")

		canva = Image.new("RGB", (601, 601), (255, 255, 255))

		cubo1=Cubo()
		cubo1.scale(1)
		gl.renderObject(cubo1.vertices, cubo1.triangles, canva)

		tkpic = ImageTk.PhotoImage(canva)
		label = tk.Label(leftSide, image=tkpic)
		label.image = tkpic  # Save reference to image
		label.pack(padx=10, pady=10)

		@staticmethod
		def callback(value):
			canva = Image.new("RGB", (601, 601), (255, 255, 255))
			cubo1=Cubo()
			cubo1.scale(int(scale_figure_bar.get()))
			cubo1.rotateX(math.radians(int(x_figure_bar.get())))
			cubo1.rotateY(math.radians(int(y_figure_bar.get())))
			cubo1.rotateZ(math.radians(int(z_figure_bar.get())))
			translationValues = getTraslationValues()
			cubo1.translation(translationValues)

			gl.renderObject(cubo1.vertices, cubo1.triangles, canva)
			tkpic = ImageTk.PhotoImage(canva)
			label.config(image=tkpic)
			label.image = tkpic  # Save reference to image

		@staticmethod
		def getTraslationValues():
			traslation = (int(x_camera_bar.get()) * 0.1, int(y_camera_bar.get()) * 0.1, int(z_camera_bar.get()) * 0.1 ) 

			return traslation

		x_figure_bar = tk.Scale(figureControllers, label="X" ,from_=-10, to=10, command=callback)
		x_figure_bar.pack(side=tk.LEFT)
		y_figure_bar = tk.Scale(figureControllers, label="Y" ,from_=-10, to=10, command=callback)
		y_figure_bar.pack(side=tk.LEFT)
		z_figure_bar = tk.Scale(figureControllers, label="Z" ,from_=-50, to=50, command=callback)
		z_figure_bar.pack(side=tk.LEFT)
		scale_figure_bar = tk.Scale(figureControllers, label="Scale" ,from_=-10, to=10, command=callback)
		scale_figure_bar.pack(side=tk.LEFT)

		x_camera_bar = tk.Scale(cameraControllers, label="X" ,from_=-5, to=5, command=callback)
		x_camera_bar.pack(side=tk.LEFT)
		y_camera_bar = tk.Scale(cameraControllers, label="Y" ,from_=-5, to=5, command=callback)
		y_camera_bar.pack(side=tk.LEFT)
		z_camera_bar = tk.Scale(cameraControllers, label="Z" ,from_=-5, to=5, command=callback)
		z_camera_bar.pack(side=tk.LEFT)
		
		figureControllers.pack(padx=10)
		cameraControllers.pack(padx=10)
		leftSide.pack(side=tk.LEFT)
		rightSide.pack(side=tk.RIGHT)


if __name__ == "__main__":
	app = rootApp()
	app.title("Examen 2")
	app.mainloop()      