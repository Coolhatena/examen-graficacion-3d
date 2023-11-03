from PIL import Image,ImageDraw
import numpy as np
import math
import graflib as gl



class Cubo():
	def __init__(self):
		self.vertices = [(1, 1, 1),(-1, 1, 1),(-1, -1, 1),(1, -1, 1),
				  (1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, -1)]
	   
		# Colors
		red = (255,0,0)
		green = (0,255,0)
		blue = (0,0,255)
		yellow = (255,255,0)
		purple = (128,0,128)
		cyan = (0,255,255)
		white = (255, 255, 255)
		# Triangles
		self.triangles = [
						[0, 1, 2, red], #red
						[2, 0, 3, red], #red
						[6, 5, 3, green], #Green
						[6, 3, 0, green], #Green
						[7, 2, 4, yellow], #Yellow
						[7, 1, 2, yellow], #Yellow
						[7, 1, 0, purple], #Purple
						[7, 6, 0, purple], #Purple
						[4, 5, 3, cyan], #Cyan 
						[4, 2, 3, cyan], # cyan
						[5, 6, 7, blue], #Blue
						[7, 4, 5, blue] #Blue
					] 
		
	@staticmethod
	def _scaleP3D(p,fs):
		P=np.array([p[0],p[1],p[2],1])
		#Matriz de escala
		print(fs)
		mS=np.array([[fs,0	,0	,0],
					[0 ,fs	,0	,0],
					[0	,0 	,fs	,0],
					[0	,0 	,0	,1]])
		return np.matmul(mS,P.transpose())
	
	@staticmethod
	def _rotateP3Dz(p,alpha):
		P=np.array([p[0],p[1],p[2],1])
		#Matriz de escala
		mR=np.array([[np.cos(alpha),-np.sin(alpha), 0, 0],
					[np.sin(alpha), np.cos(alpha), 0, 0],
					[            0,             0, 1, 0],
					[            0,             0, 0, 1]])
		return np.matmul(mR,P.transpose())
		
	@staticmethod
	def _rotateP3Dx(p,alpha):
		P=np.array([p[0],p[1],p[2],1])
		#Matriz de escala
		mR=np.array([[ 1,             0,             0, 0],
					[ 0, np.cos(alpha),-np.sin(alpha), 0],
					[ 0, np.sin(alpha), np.cos(alpha), 0],
					[ 0,             0,             0, 1]])
		return np.matmul(mR,P.transpose())

	@staticmethod
	def _rotateP3Dy(p,alpha):
		P=np.array([p[0],p[1],p[2],1])
		#Matriz de escala
		mR=np.array([[np.cos(alpha),             0,np.sin(alpha), 0],
					[            0,             1,            0, 0],
					[-np.sin(alpha), 0, np.cos(alpha),            0],
					[            0,             0,            0, 1]])
		return np.matmul(mR,P.transpose())
	
	@staticmethod
	def _translateP3D(p,pt):
		P=np.array([p[0],p[1],p[2],1])
		#Matriz de escala
		mT=np.array([[1,0,0,pt[0]],
					[0,1,0,pt[1]],
					[0,0,1,pt[2]],
					[0,0,0,    1]])
		return np.matmul(mT,P.transpose())

						  
	def translation(self,position):
		self.vertices=[self._translateP3D(vertex,position) for vertex in self.vertices]
		
	def rotateX(self,ax):
		if ax != 0:
			self.vertices=[self._rotateP3Dx(vertex,ax) for vertex in self.vertices]
		
		
	def rotateY(self,ax):
		if ax != 0:
			self.vertices=[self._rotateP3Dy(vertex,ax) for vertex in self.vertices]

		
	def rotateZ(self,ax):
		if ax != 0:
			self.vertices=[self._rotateP3Dz(vertex,ax) for vertex in self.vertices]
		
	def scale(self,fs):
		if fs != 0:
			self.vertices=[self._scaleP3D(vertex,fs) for vertex in self.vertices]
		

if __name__ == "__main__":
	#Tamaño de la imagen
	width = 801
	height = 801

	#Definir un lienzo
	canvas = Image.new('RGB', (width,height), (255,255,255))

	#Puntos iniciales
	cubo1=Cubo()
	cubo1.scale(-5)
	cubo1.translation((0.5, 0.5, 0))

	gl.renderObject(cubo1.vertices,cubo1.triangles,canvas)
	print(cubo1.vertices)
	canvas.show()