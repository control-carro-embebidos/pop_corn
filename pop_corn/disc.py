#todo
#En draw dibujat pologonos
from pop_corn.scene import Scene
from pop_corn.matrix import Matrix, Vec
from math import cos, sin, sqrt, atan2

class Disc(Scene):
    def __init__(self,scene):#,control=None):
        super().__init__()
        self.scene=scene
        scene.add_disc(self)
        self.color='black'
        self.r = 10 #radio
        #self.dim =Vec(self.r,self.r)#Matrix(1,3,[self.r,self.r,1])
        self.m = 1 #masa
        self._pos=Vec(0,0)#Matrix(1,3,[0,0,1])
        self._angle=0
        self._vel=0
        self.vel=Vec(0,0)#Matrix(1,3,[0,0,1])
        self.k_elast=0.1 
        self.k_frict=0.02
        self.f=Vec(0,0)#Matrix(1,3,[0,0,1])
        self.k_magne =1
        self.d_magne =self.r *5
        self.tag_disc='disc'
#         if control==None:
#             control=self.default_control
        self.control=self.default_control
        self.things={}
        r=self.r
        self.poligons=[]

    def get_angle(self):
        return self._angle
    
    def set_angle(self,angle):
        self._angle=angle

    def add_angle(self, angle):
        self._angle += angle

    def get_speed(self):
        return self._vel
    
    def set_speed(selg,vel):
        self._vel=vel

    def get_vel(self):
        return Vec(self._vel*cos(self._angle),self._vel*sin(self._angle))

    def set_vel(self,vel_vec):
        self._vel=sqrt(vel_vec[1]*vel_vec[1]+vel_vec[0]*vel_vec[0])
        if self._vel != 0:
            self._angle=atan2(vel_vec[1],vel_vec[0])

    def add_vel(self,vel_vec):
        self.set_vel(self.get_vel()+vel_vec)


    def get_pos(self):
        return self._pos#Vec(self._transf[2,0],self._transf[2,1])

    def set_pos(self,x,y=None):
        if y==None:
            y=x[1]
            x=x[0]
            #print('set_pos',x,y)
        self._pos=Vec(x,y)

    def add_pos(self,pos):
        self._pos  = self._pos +pos

#     def get_transf(self):
#         return Matrix.trans2D(self._pos)@Matrix.rot2D(self._angle)

    def get_transf(self):
        return Matrix.rot2D(self._angle)@ Matrix.trans2D(self._pos)

    def add_force(self,f):
        self.f=self.f+f

    def clear_force(self):
        self.f=Vec(0,0)#Matrix(1,3,[0,0,1])

    def draw(self, canvas,transf_dad=Matrix.id(3),tag='disc'):
       #print('*',end='')
       dim=Vec(self.r,self.r)
       vertex=((self.get_pos()@transf_dad - dim) | (self.get_pos()@transf_dad + dim))
       #print('Disc draw vertex',vertex)
       canvas.oval(vertex, fill=self.color, tag=tag)
       for poligon in self.poligons:
           canvas.poly(poligon,tag=tag)
       transf=transf_dad@self.get_transf()

       for disc in self.discs:
            #canvas.delete(disc.tag_disc)
            disc.draw(canvas,transf)
  

    def is_inside(self,pos):
        print('inside',self.get_pos(),pos,(self.get_pos()-pos).norm())
        return (self.get_pos()-pos).norm()<=self.r
    
    def is_in_border(self,pos):
        return (self.get_pos()-pos).norm()==self.r
    
    @staticmethod
    def default_control(disc,t):
        disc.add_vel(disc.f*(1/disc.m)*t)
        disc.add_pos(disc.get_vel()*t + disc.f*(t**2/disc.m/2))
        pass
        #return pos,vel

    def refresh(self,t):
        
   


    #def refresh(self):

        self.control(self,t)

        #self.vel = vel   
        #self.set_pos( pos)
        self.clear_force()
        #return (self.get_pos() - self.dim) | (self.get_pos() + self.dim)


        self.forces()
        
        
        for disc in self.discs:
            #print('.',end='')
            disc.refresh(t)            
#         for canvas in self.subscribers_canvas:
#             #print('#',end='')
#             canvas.delete("disc")
#             for disc in self.discs:
#                 #canvas.delete(disc.tag_disc)
#                 disc.draw(canvas)
    
