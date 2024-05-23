import tkinter as tk
from Matrix import Matrix

class Canvas_Tkinter:
    def __init__(self,transf=None,rows=900,cols=1800,tk_master=None,grid=10 ):
        self.canvas_width = cols
        self.canvas_height = rows
        if transf == None:
            zoom=min(rows,cols)/50
            self.transf=Matrix(3,3,
                               [zoom,0,0,
                                0,zoom,0,
                                cols/2,rows/2,1],has_tail=True)
        else:
            self.transf=transf
        if tk_master == None: 
            self.tk_master = tk.Tk()
        else:
            self.tk_master = tk_master
        self.canvas = tk.Canvas(tk_master,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg="green")
        self.canvas.pack()

    
    #def render(scene,rectangle)->bytearray:
    #    pass
    
    
    def oval(self, vertex,**options)->int:
        return self.canvas.create_oval(vertex@self.transf,**options)
        
    def rect(self, vertex,**options)->int:
        return self.canvas.create_rectangle(vertex@self.transf,**options)
        
    def text(self, vertex,**options)->int:
        return self.canvas.create_text(vertex[0:1,:]@self.transf,**options)

    def	line(self, vertex,**options)->int:
        return self.canvas.create_line(vertex@self.transf,**options)
    
    #def coords(self, id_shape, list_vertex):
    #    self.canvas.coords(id_shape, list_vertex@self.transf)
            
    def background(self, parameter):
        if isintance(parameter, str):
             self.canvas.configure(bg=parameter)

    def draw_grid(self, width, height, interval,color):
        # Dibujar líneas verticales
        wh=Vec(width,height)@self.transf
        width=wh[0]
        height=wh[1]
        for x in range(0, width, interval):
            self.create_line(x, 0, x, height, fill=color, dash=(2, 2))
        # Dibujar líneas horizontales
        for y in range(0, height, interval):
            self.create_line(0, y, width, y, fill=color, dash=(2, 2))

    def delete(self):
        self.canvas.delete("all")

#     def refresh(self, scene):
#         tag="disc"
#         self.delete(tag)
#         for disc in scene.discs:
#             disc.draw(self,tag=tag)
    