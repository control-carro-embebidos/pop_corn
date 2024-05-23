from Matrix import Matrix, Vec
from Scene import Scene
import array
import random


import tkinter as tk
import math


if __name__ == "__main__":

    from Disc import Disc,Rect
    from Canvas_Tkinter import Canvas_Tkinter

    master = tk.Tk()
    scene = Scene(0x00ff00)
    disc = Disc(scene)
    scene.add_disc(disc)
    
    canvas = Canvas_Tkinter( tk_master=master)
    scene.subscribe_canvas(canvas)
    
    t_anim = 50
    
    disc = Disc(scene)
    disc.color='black'
    disc.set_pos(-15,0)
    disc.vel=Vec(0.5,0.05)
    scene.add_disc(disc)
#     disc.color='red'
#     disc.set_pos(-10,0)#Matrix(1,3,[-15,0,1])
#     disc.vel=Vec(0.5,0.05)#Matrix(1,3,[0.5,0.05,1])
#    scene.add_disc(disc)
#    disc_click = None


    def anim_loop():    
        master.after(t_anim,anim_loop)
        scene.anim()

  
    anim_loop() 
    master.mainloop()
    
    


