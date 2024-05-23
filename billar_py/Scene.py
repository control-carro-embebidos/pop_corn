#HeredardeDiscoslos rectangulos de las materias de la malla
#A medida que se leese van diparando desde la izquierda
#Guardar y leer
#Prerequisitos
#
#Leer ADC y trasnmitirlo por sockets a tkinter 






from Matrix import Matrix, Vec
#import array
#import random


#import tkinter as tk
#import math

class Scene:
    
    def __init__(self,background):
        self.discs=[]
        self.background=background
        self.subscribers_canvas=[]
        
    def get_background_at(self,positions:Matrix):
        if isinstance(self.background,int):
            return self.background
        elif isinstance(self.background,type(get_background_at)):
            return self.background(positions)

    def add_disc(self,disc):
            self.discs.append(disc)

    def subscribe_canvas(self, canvas):
        if canvas not in self.subscribers_canvas:
            self.subscribers_canvas.append(canvas)


    def anim(self):    
        #self.canvas.after(self.t_anim,self.anim)
        #print('.',end='')
        
        n=len(self.discs)
        for i in range(n):
           for j in range(i):
                disc_i = self.discs[i] 
                disc_j = self.discs[j] 
                dist=(disc_i.get_pos() - disc_j.get_pos()).norm()
                if dist<(disc_i.r+disc_j.r) :
                    if dist<(disc_i.r+disc_j.r)/100:
                        dist=(disc_i.r+disc_j.r)/100
                    f_dir_ji=(disc_i.get_pos() - disc_j.get_pos())*(1/dist)
                    dist=min(dist,disc_i.r,disc_j.r)
                    k_elast=(disc_i.k_elast + disc_j.k_elast)/2
                    f_ji=k_elast*dist*f_dir_ji
                    disc_i.add_force(f_ji) #colition
                    disc_j.add_force((-1)*f_ji) #colition
        for disc in self.discs:

            dx=(disc.get_pos()[0]%disc.d_magne)-disc.d_magne/2
            dy=(disc.get_pos()[1]%disc.d_magne)-disc.d_magne/2
            dif=Vec(dx,dy)#Matrix(1,3,[dx,dy,1])
            dist=dif.norm()
            if dist==0:
                dist=disc.d_magne/1000
            f_mag=(disc.k_magne/dist)*dif
            disc.add_force((disc.k_magne/dist)*dif) #Magnetic Force

            disc.add_force(-disc.k_frict*disc.vel)  # friction

     
 
            disc.refresh(1)            
        tag="disc"
        for canvas in self.subscribers_canvas:
            canvas.delete()
            for disc in self.discs:
                disc.draw(canvas,tag)
            
#             for shape_dic in disc.get_shapes():
#                 self.canvas.coords(canvas_shape, disc_shape['vertex']@self._transf)
#  

