from pop_corn.matrix import Matrix, Vec
from pop_corn.mainscene import MainScene
from pop_corn.disc import Disc
from pop_corn.stick import Stick
from pop_corn.pub_sub import PubSub
from pop_corn.py.context_tkinter import Context_Tkinter as Context
from wall_e.wall_e import Wall_e
from wall_e.garbage import Garbage


class Host(PubSub):
    def __init__(self,zones_num,debug=False):
        super().__init__()
        self.zones_num=zones_num
        #self.pubsub = PubSub()
        pass
     
    def start(self):
        for i in range(self.zones_num[0]):
            for j in range(self.zones_num[1]):
                name=f"Walle_{i}_{j}/wheelVels"
                #self.publish(name, {"steering_angle_deg":20*i+5*j,"speed_cm_s":2, "duration_seg":30})
        #self.publish("All_Wall_es", {"steering_angle_deg":0,"speed_cm_s":20, "duration_seg":2})      
        self.publish("All_Wall_es/on_move", #{"value": "10"})
        {#"arm_ds_deg**3":[[3,10,10,10],[5,12,10,10],[10,14,10,10],[15,20,10,10]],
                       "rel_posit_ds_frontmm_rightmm_angledeg":[[8,10,10,0],[8,12,-10,0],[8,14,-10,45],[3,20,-10,45]],
         #              "catch_ds_byte":[[0,0],[10,255],[15,0]]
            })
        self.publish("Walle_0_0/on_move", #{"value": "10"})
        {"rel_posit_ds_frontmm_rightmm_angledeg":[[2,11,11,15],[2,12,10,30],[2,14,10,45],[2,20,10,60]]})

    def animate(self):
        pass
    
    def get_name(self):
        return "Host"

if __name__ == "__main__":
    
    t_anim = 100 #ms
    zones_num=(1,2)
    zones_size=(250,250)
    #debug=True#False#
    debug=False#True#
    
    host = Host(zones_num,debug)
    ctx=Context()
    scene = MainScene()#bg='img/UD_@8.xbm', foreground="white", background="black")
    disc0 = Disc(scene)
    Garbage(scene,"red",100,-80)
    Garbage(scene,"blue",100,100)
    wall_es=[]
    for i in range(zones_num[0]):
        list_tmp=[]
        for j in range(zones_num[1]):
            disc_tmp=Wall_e(scene,i,j,host,debug)
            name=disc_tmp.get_name()
            #disc_tmp.name=f"Walle_{i}_{j}"
            #disc1.color='blue'
            disc_tmp.set_pos(int((i-zones_num[0]/2 +.5)*zones_size[0]),int((j-zones_num[1]/2+0.5)*zones_size[1]))
            #disc1.set_vel(Vec(5,0.5))
            #host.subscribe(disc_tmp.name+" All_Wall_es", disc_tmp, "Command")
            list_tmp.append(disc_tmp)
            #host.publish(disc_tmp.name, {"steering_angle_deg":20*i+5*j,"speed_cm_s":15, "duration_seg":5})
            
        wall_es.append(list_tmp)
    stick1=Stick(scene,wall_es[0][0])
    stick1.set_pos(-100,-100)
    
    #host.publish("All_Wall_es", {"steering_angle_deg":0,"speed_cm_s":20, "duration_seg":2})
        
    canvas = ctx.canvas(scene,height=zones_num[1]*zones_size[1],width=zones_num[0]*zones_size[0])

    def anim_loop():
        #global debug
        if debug:
            rta=input("Debug Mode, Press ENTER")
        #    if "off"==rta:
        #        debug=False
        ctx.after_ms(t_anim,anim_loop)
        scene.refresh()
        host.animate()
  
    host.start()
    anim_loop() 
    ctx.mainloop()
    
