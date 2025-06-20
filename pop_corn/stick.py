from pop_corn.scene import Scene
from pop_corn.matrix import Matrix, Vec
from math import cos, sin, sqrt, atan2
from pop_corn.disc import Disc

class Stick(Disc):
    def __init__(self,scene,other):#,control=None):
        super().__init__(scene)
        self.other=other
        self.dist=(self.get_pos()-other.get_pos()).norm()
        #self.f_dir_ji=(self.get_pos() - other.get_pos())*(1/self.dist)
        print("Stick",self.dist)
        
        
    def draw(self, canvas,transf_dad=Matrix.id(3),tag='stick refreshable'):
        super().draw(canvas,transf_dad=transf_dad,tag=tag)
        #canvas.poly(self.get_pos() | self.other.get_pos()| Vec(-20,-20))
        canvas.line(self.get_pos() | self.other.get_pos(),tag=tag)
        
    def stick_force(self):
    #    self.forces_two_disc_collision(self.other)
        
    #def forces_two_disc_collision(disc_i,disc_j):
            disc_i=self
            disc_j=self.other
            dist=(disc_i.get_pos() - disc_j.get_pos()).norm()
            #if dist<(disc_i.r+disc_j.r) :
            if dist<(disc_i.r+disc_j.r)/100:
                dist=(disc_i.r+disc_j.r)/100
            f_dir_ji=(disc_i.get_pos() - disc_j.get_pos())*(1/dist)
            dist=max(dist,disc_i.r,disc_j.r)
            k_elast=(disc_i.k_elast + disc_j.k_elast)/2
            f_ji=1*(self.dist-dist)*f_dir_ji
            disc_i.add_force(f_ji) #colition
            disc_j.add_force((-1)*f_ji) #colition
            #print("forces:",f_ji)
