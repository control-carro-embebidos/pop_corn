    




if __name__ == "__main__":

    from pop_corn.matrix import Matrix, Vec
    from pop_corn.scene import Scene
    from pop_corn.mainscene import MainScene
    from pop_corn.disc import Disc
    from pop_corn.py.canvas_Tkinter import Canvas_Tkinter
    import tkinter as tk

    t_anim = 50


    master = tk.Tk()
    scene = MainScene()#bg='img/UD_@8.xbm', foreground="white", background="black")
    disc0 = Disc(scene)
    
    disc1 = Disc(scene)
    disc1.r=10
    disc1.color='blue'
    disc1.set_pos(-50,0)
    disc1.set_vel(Vec(5,0.5))

    canvas = Canvas_Tkinter(scene, tk_master=master)
    scene.subscribe_canvas(canvas)

    def anim_loop():    
        master.after(t_anim,anim_loop)
        scene.refresh()

  
    anim_loop() 
    master.mainloop()
    