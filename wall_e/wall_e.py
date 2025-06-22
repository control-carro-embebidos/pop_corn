import math
import time
from pop_corn.matrix import Matrix, Vec
from pop_corn.mainscene import MainScene
from pop_corn.disc import Disc
from pop_corn.uqueue import uQueue
from pop_corn.py.context_tkinter import Context_Tkinter as Context
from pop_corn.lib import copy



class Wall_e(Disc):
    def __init__(self,scene,i,j,host,debug=False):
        self.debug=debug
        self.host=host
        self.i,self.j=i,j
        super().__init__(scene)
        self.steering_angle_degrees=1
        self.wheelbase=200
        #self._t_circle=0
        self.set_speed(5)
        self.poligons=[
            {"points":Matrix(4,2,[3,5, 3,15, 18,15, 18,5]),"options":{}},
            {"points":Matrix(4,2,[-3,5, -3,15, -18,15, -18,5]),"options":{}},
            {"points":Matrix(4,2,[-3,-5, -3,-15, -18,-15, -18,-5]),"options":{}},
            {"points":Matrix(4,2,[3,-5, 3,-15, 18,-15, 18,-5]),"options":{}},
            {"points":Matrix(8,2,[7,-2, 20,-2, 20,-5, 30,-5, 30,5, 20,5, 20,2, 7,2]),"options":{"fill":"yellow"}},
                      ]
        host.subscribe(self.get_name()+"/wheelVels All_Wall_es/wheelVels", self, "wheelVels")
        host.subscribe(self.get_name()+"/on_move All_Wall_es/on_move", self, "on_move")


        self.queues = {}  # callback_name -> Queue()
        #self.ps=pubsub
        self.k_max_mag = 10
        self.k_mag =self.k_max_mag
        self.k_ferromag = 0
        #self.move_wall_e_conf={"arm_m":[1,1,1],"arm_b":[0,0,0],"wheels_lr_m":[1,1],"wheels_lr_b":[0,0]}
        self.move_car_data={}
        #self.move_arm_time_stamp=None
        self._pos=Vec(0,0)
        self.anim_data={}
        self.ticks=0

        # Subscribe to each topic using provided PubSub

#     def ensure_queue(self, callback_name):
#         if callback_name not in self.queues:
#             self.queues[callback_name] = uQueue(callback_name)

    def published(self, data):
        data=copy.deepcopy(data)
        #print("Who published",self.get_name(),data)
        callback_name = data.get("callback_name")
        control= data.get("control","appendlast")
        if callback_name is None:
            return
        #self.ensure_queue(callback_name)
        if callback_name not in self.queues:
            self.queues[callback_name] = uQueue(callback_name)
        if control=="appendlast":
            self.queues[callback_name].appendlast(data)
        if control=="appendfirst":
            self.queues[callback_name].appendfirst(data)
        if control=="clear_appendfirst":
            self.queues[callback_name].clear()
            self.queues[callback_name].appendfirst(data)
        self.print("Who published",self.get_name(), self.queues[callback_name]._queue)

    def process(self, callback_name,t):
        queue = self.queues.get(callback_name)
        if queue:
            #while len(queue):
                msg = queue.popfirst()
                #self.print("process",f"{self.get_name()}:{callback_name} received ->", msg)
                if callback_name=="on_move":
                    self.move_wall_e_ini(msg['data'])
        else:
            pass
            self.print("process",f"{self.get_name()}:{callback_name} No_received")


#     def set_steering_angle_degrees(self,angle_deg):
        
# import math

    def inverse_kinematics(self, front_distance, right_distance, angle=None):
        
        wheelbase = self.wheelbase
        
        # Calculate the radius of the turn
        if right_distance == 0:
            # Drive straight
            steering_angle_radians = 0.0
        else:
            # Use simple trigonometry: tan(steering_angle) = wheelbase / turn_radius
            # turn_radius = sqrt(front^2 + right^2)
            turn_radius = math.sqrt(front_distance**2 + right_distance**2)
            steering_angle_radians = math.atan(wheelbase / turn_radius)

            # Adjust sign based on direction of the turn
            if right_distance < 0:
                steering_angle_radians *= -1
        
        steering_angle_degrees = math.degrees(steering_angle_radians)
        self.print('inverse_kinematics',front_distance, right_distance, angle,steering_angle_degrees)
        return steering_angle_degrees

    def move_wall_e_ini(self,movements):
        #wall_e movemen is a dic of list of list, first item is time in ds relative to the lastime of the same key
        #movements={"arm_ds_deg**3":[[3,10,10,10],[5,12,10,10],[10,14,10,10],[15,20,10,10]],
        #           "rel_posit_ds_front_right_mm":[[3,10,10],[5,12,10],[10,14,10],[15,20,10]],
        #           "catch_ds_byte":[[0,0],[10,255],[15,0]]}
        
        for key in movements:
            if key in self.move_car_data:
                self.move_car_data[key]+=copy.deepcopy(movements[key])
            else:
                self.move_car_data[key]=copy.deepcopy(movements[key])
            #print("move_wall_e_ini",key,self.move_car_data[key])
            self.anim_data[key+"_time_stamp_ds"]=self.ticks#time.time_ns()//10**8
        self.print("move_wall_e_ini self.anim_data",self.anim_data,self.move_car_data)
        
        
        
    def move_wall_e_anim(self,t):
        #Debe mover el brazo segun lo guardado
        #Cuando termina buscaun nuevo comando
        # o borra los comandos anteriores
        #key_time_stamp_ds="_time_stamp_ds"
        #key_stored_state="_stored_state"
        
        self.ticks+=t
        key="rel_posit_ds_frontmm_rightmm_angledeg"
        if key in self.move_car_data:
            if key not in self.anim_data:
                #self.anim_data[key]={key_time_stamp_ds:0,key_stored_state:{"steering_angle_degrees":0,"speed_mm_s":0,"ticks":0}}
                self.anim_data[key]={"steering_angle_degrees":0,"speed_mm_s":0,"ticks":0}
                self.print("wall_e move_wall_e_anim: key not in self.anim_data")
                
            self.print("wall_e move_wall_e_anim:  move_car_data",self.move_car_data[key],self.anim_data[key])
                
            if  self.anim_data[key]["ticks"]>0:
                
                #ds, frontmm, rightmm, angledeg=self.move_car_data[key][key_stored_state]
                #self.steering_angle_degrees=self.anim_data[key]["steering_angle_degrees"]
                #self.set_speed(self.anim_data[key]["speed_mm_s"])
                self.anim_data[key]["ticks"]-=t
                #inverse_kinematics(self, frontmm, rightmm, angle=angledeg)#angle is ignored
                self.print("wall_e move_wall_e_anim: self.anim_data[key][ticks]>0",self.anim_data[key])
            elif len(self.move_car_data[key])>0:
                  print('move_wall_e_anim',len(self.move_car_data[key]),self.get_name())
#                   if key_stored_state not in self.move_car_data[key]:
#                       print("self.move_car_data[key]",self.move_car_data[key])
#                       print("self.anim_data",self.anim_data)
#                       self.move_car_data[key][key_stored_state]={}
                  ds,front,right,angl=self.move_car_data[key].pop(0)
                  self.anim_data[key]["steering_angle_degrees"]=self.inverse_kinematics(front, right, angl)
                  self.anim_data[key]["speed_mm_s"]=Vec(front,right).norm()/ds
                  self.anim_data[key]["ticks"]=ds
#                 ds=self.move_car_data[key][0][0]
#                 #delta_ticks=time.time_ns()//10**8
#                 self.print("move_wall_e_anim self.anim_data",self.anim_data,self.move_car_data,self.ticks)
#                 if (self.anim_data[key+key_time_stamp_ds]+ds)<= self.ticks:
#                     ds,front,right,angl=self.move_car_data[key].pop(0)
#                     self.anim_data[key+key_time_stamp_ds]=self.ticks
#                     self.add_pos(Vec(front,right))
#                     self.add_angle(angl*math.pi/180)
                  self.print("wall_e move_wall_e_anim: en(self.move_car_data[key])>0",self.anim_data[key])
            else:
                #Sería mejor disminuir la velocidad gradualmente
                self.anim_data[key]["steering_angle_degrees"]=0
                self.anim_data[key]["speed_mm_s"]=0
                self.anim_data[key]["ticks"]=0
#    
                pass
                self.print("wall_e move_wall_e_anim: Hay que frenar",self.anim_data[key])
            self.steering_angle_degrees=self.anim_data[key]["steering_angle_degrees"]
            self.set_speed(self.anim_data[key]["speed_mm_s"])
    



#    def send(self,dest,data):
#        pass
    
    def recive(self,dest,data):
        pass
        
    

    def get_name(self):
        return f"Walle_{self.i}_{self.j}"

#     def published(self, data=None):
#         print("Who published",self.get_name(),data)
#         if data["callback_name"]=="Command":
#             if "steering_angle_deg" in data["data"]:
#                 self.steering_angle_degrees=data["data"]["steering_angle_deg"]
#                 #print("steering_angle_degrees",data["data"]["steering_angle_deg"],self.steering_angle_degrees)
#             if "speed_cm_s" in data["data"]:
#                 self.set_speed(data["data"]["speed_cm_s"])
#                 #print("speed_cm_s",data["data"]["speed_cm_s"],self.get_speed())
#             if "duration_seg" in data["data"]:
#                 self._t_circle=data["data"]["duration_seg"]
#                 #print("duration_seg",data["data"]["duration_seg"],self._t_circle)        
        
    @staticmethod
    def default_control(self,t):
        self.process("on_move",t)
        self.move_wall_e_anim(t)
        self.print("default_control wall_w t",self.i,self.j,self.steering_angle_degrees)
        
        if True:#self._t_circle>0:
        
            v=self.get_speed()
            # Actualización del ángulo del carro
            self.add_angle((v / self.wheelbase) * math.tan(self.steering_angle_degrees*math.pi/180)*t)

            # Desplazamiento en el sistema global
            theta = self._angle  # orientación actual del carro
            dx = v * math.cos(theta) * t
            dy = v * math.sin(theta) * t

            desp = Matrix(1,2,[dx, dy])
            self.add_pos(desp)
            #self._t_circle-=t
            #print("wall_w t",t)



    def print(self,*args):
        if self.debug:
            print(*args,self.get_name(),self.ticks)
        


# if __name__ == "__main__":
#     
