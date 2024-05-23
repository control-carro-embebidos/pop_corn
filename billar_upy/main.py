from Matrix import Matrix, Vec
from Scene import Scene
import array
import random
from machine import Timer


#import tkinter as tk
import math


if __name__ == "__main__":

    from Disc import Disc,Rect
    #from Mouse_Tkinter import Mouse_Tkinter
    from Canvas_print import Canvas_print

    #master = tk.Tk()
    scene = Scene(0x00ff00)
    disc = Disc(scene)
    scene.add_disc(disc)
    
    canvas = Canvas_print()#, tk_master=master)
    scene.subscribe_canvas(canvas)
    
    t_anim = 50
    
    disc = Disc(scene)
    disc.color='black'
    disc.set_pos(-15,0)#Matrix(1,3,[-15,0,1])
    disc.vel=Vec(0.5,0.05)#Matrix(1,3,[0.5,0.05,1])
    scene.add_disc(disc)
    
    def anim(timer):
        scene.anim()
    
    timer=Timer()
    timer.init(period=2000, mode=Timer.PERIODIC, callback=anim)
 
 
#     disc.color='red'
#     disc.set_pos(-10,0)#Matrix(1,3,[-15,0,1])
#     disc.vel=Vec(0.5,0.05)#Matrix(1,3,[0.5,0.05,1])
#    scene.add_disc(disc)
#    disc_click = None


#     screen_w =scene.canvas_width = 1800
#     screen_h =scene.canvas_height = 900
#     margin= 20
#     box_w=screen_w//12
#     box_h=screen_h//12

#         def espacio_mas_cercano_al_centro(cadena):
#             # Calcula el índice del centro de la cadena
#             centro = len(cadena) // 2
# 
#             # Inicializa la distancia mínima y el índice del espacio más cercano
#             min_distancia = float('inf')
#             espacio_mas_cercano = None
# 
#             # Itera sobre cada carácter de la cadena
#             for i, char in enumerate(cadena):
#                 if char == ' ':
#                     # Calcula la distancia absoluta desde el centro
#                     distancia = abs(centro - i)
#                     # Actualiza si la distancia es menor que la mínima encontrada hasta ahora
#                     if distancia < min_distancia:
#                         min_distancia = distancia
#                         espacio_mas_cercano = i
# 
#             return espacio_mas_cercano
#         
                

# 
#     def on_mouse_button(event):
#         global disc_click
#         #print(event.time)        
#         #print(f"Mouse button event: {event.type} at ({event.x}, {event.y})")
#         pos=Vec(event.x,event.y)@scene.get_transf_inv()#Matrix(1,3,[event.x,event.y,1])*scene.get_transf_inv()
#         #print('button',pos)
#         if event.type=='4':
#             for disc_dic in scene.discs:
#                 #print('button2',pos, disc_dic['disc'].get_pos())
#                 if disc_dic['disc'].is_inside(pos):
#                     print('*******************')
#                     disc_click = disc_dic
#                     break
#         elif event.type=='5':
#             
#             disc_click = None
# 
# 
#     def on_mouse_drag(event):
#         #print(f"Mouse dragged to ({event.x}, {event.y})",)
#         if disc_click != None:
#             pos=Vec(event.x,event.y)@scene.get_transf_inv()#Matrix(1,3,[event.x,event.y,1])*scene.get_tranf_inv()
#             #print('button',pos)
#             disc_click['disc'].set_pos(pos)
#             


#     mouse_handler = Mouse_Tkinter(scene.canvas)#scene.get_transf_inv(),
# #    mouse_handler.subscribe_to_move(on_mouse_move)
#     mouse_handler.subscribe_to_button(on_mouse_button)
#     mouse_handler.subscribe_to_drag(on_mouse_drag)
# 
#     def anim_loop():    
#         master.after(t_anim,anim_loop)
#         scene.anim()
# 
#   
#     anim_loop() 
#     master.mainloop()
    
    


