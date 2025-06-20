from pop_corn.scene import Scene
from pop_corn.matrix import Matrix, Vec
from math import cos, sin, sqrt, atan2
from pop_corn.disc import Disc

class Stick(Disc):
    def __init__(self,scene,other):#,control=None):
        super().__init__(scene)
        self.other=other
        self.dist=(self.get_pos()-other.get_pos()).norm()
        
        
    def draw(self, canvas,transf_dad=Matrix.id(3),tag='stick refreshable'):
        super().draw(canvas,transf_dad=transf_dad,tag=tag)
        #canvas.poly(self.get_pos() | self.other.get_pos()| Vec(-20,-20))
        canvas.line(self.get_pos() | self.other.get_pos(),tag=tag)
        
    def stick_force(self):
        self.forces_two_disc_collision(self.other)