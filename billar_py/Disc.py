from Matrix import Matrix, Vec#, Matrix.Vec
#from Matrix.Matrix import Vec
import array
import random
import tkinter as tk
 

import math

class Disc:
    def __init__(self,scene):
        self.scene=scene
        self.color='yellow'
        self.r = 1 #radio
        self.dim =Vec(self.r,self.r)#Matrix(1,3,[self.r,self.r,1])
        self.m = 1 #masa
       # self._transf=Matrix(3,3,[1,0,0,
       #                          0,1,0,
       #                          0,0,1])
        self._pos=Vec(0,0)#Matrix(1,3,[0,0,1])
        self.vel=Vec(0,0)#Matrix(1,3,[0,0,1])
        self.k_elast=0.1 
        self.k_frict=0.01
        self.f=Vec(0,0)#Matrix(1,3,[0,0,1])
        
        self.k_magne =0.001
        self.d_magne =self.r *5

    def get_pos(self):
        return self._pos#Vec(self._transf[2,0],self._transf[2,1])

    def set_pos(self,x,y=None):
        if y==None:
            y=x[1]
            x=x[0]
            #print('set_pos',x,y)
        self._pos=Vec(x,y)
        #self._transf[2,0]=x
        #self._transf[2,1]=y

    def add_force(self,f):
        self.f=self.f+f

    def clear_force(self):
        self.f=Vec(0,0)#Matrix(1,3,[0,0,1])

    
#     def get_shapes(self):
#         print('get_shapes',self.get_pos() - self.dim)
#         return [{
#             "shape":oval,
#             #"radio":1,
#             "options":{"fill":self.color},
#             "transf":Matrix(3,3,[1,0,0,
#                                  0,1,0,
#                                  0,0,1]),
#             "vertex":(self.get_pos() - self.dim) | (self.get_pos() + self.dim)
#         }]

    def draw(self, canvas,tag):
    
       vertex=(self.get_pos() - self.dim) | (self.get_pos() + self.dim)
       #print('Disc draw vertex',vertex)
       canvas.oval(vertex, fill=self.color, tag=tag)


    def is_inside(self,pos):
        print('inside',self.get_pos(),pos,(self.get_pos()-pos).norm())
        return (self.get_pos()-pos).norm()<=self.r
    
    def is_in_border(self,pos):
        return (self.get_pos()-pos).norm()==self.r
    

    def refresh(self,t):

        self.vel = self.vel + self.f*(1/self.m)*t   
        self.set_pos( self.get_pos() + self.vel*t + self.f*(t**2/self.m/2))
        self.clear_force()
        return (self.get_pos() - self.dim) | (self.get_pos() + self.dim)
   
   
       
class Rect(Disc):

    def cut_text(self,cadena):
        # Calcula el índice del centro de la cadena
        centro = len(cadena) // 2

        # Inicializa la distancia mínima y el índice del espacio más cercano
        min_distancia = float('inf')
        n = None

        # Itera sobre cada carácter de la cadena
        for i, char in enumerate(cadena):
            if char == ' ':
                # Calcula la distancia absoluta desde el centro
                distancia = abs(centro - i)
                # Actualiza si la distancia es menor que la mínima encontrada hasta ahora
                if distancia < min_distancia:
                    min_distancia = distancia
                    n = i

        return cadena[:n] + "\n" + cadena[n:]


    def __init__(self,scene,materia,creditos):
        super().__init__(scene)
        self.dim =Vec(2*self.r,self.r)
        if len(materia) > 15:
            materia = self.cut_text(materia)
        self.text=f"{materia}\n{creditos} créditos"
        
        
    
    def get_shapes(self):
        return super().get_shapes()+[{
        #return [{
            "shape":"rectangle",
            #"dims":(2,1),
            "options":{"fill":self.color},
            "transf":Matrix(3,3,[1,0,0,
                                 0,1,0,
                                 0,0,1]),
            "vertex":(self.get_pos() - self.dim) | (self.get_pos() + self.dim)
        },{
            "shape":"text",
            "msg":self.text,
            "options":{"fill":self.color,
                       "font":("Purisa", 12-len(self.text)//5),
                       "justify":tk.CENTER
                       },
            "transf":Matrix(3,3,[1,0,0,
                                 0,1,0,
                                 0,0,1]),
            "vertex":self.get_pos()

                }]
