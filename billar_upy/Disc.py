from Matrix import Matrix, Vec
import array
 

import math

class Disc:
    def __init__(self,scene):
        self.scene=scene
        self.color='yellow'
        self.r = 1 #radio
        self.dim =Vec(self.r,self.r)
        self.m = 1 #masa
        self._pos=Vec(0,0)
        self.vel=Vec(0,0)
        self.k_elast=0.1 
        self.k_frict=0.01
        self.f=Vec(0,0)
        
        self.k_magne =0.001
        self.d_magne =self.r *5

    def get_pos(self):
        return self._pos

    def set_pos(self,x,y=None):
        if y==None:
            y=x[1]
            x=x[0]
            #print('set_pos',x,y)
        self._pos=Vec(x,y)

    def add_force(self,f):
        self.f=self.f+f

    def clear_force(self):
        self.f=Vec(0,0)#Matrix(1,3,[0,0,1])

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
   
   
       