#Stadistics:
    #Credits

#zoom in,out
#Move camera o scene
#rotar para cambiar el angulo de vista



#Falta verificar
# La tabla prerequisitos.csv pasó por ChatGPT

#To do
#show dic of the objects

# dibujar fondo con la grilla
# tablas con polas
# Lista de materias y áreas por colores
# Si letra muy grande dismin


# visualizar fuerzas cada tipo de fuerza de un color y otro color para la resultante


#Dibujar varias particulas
#Velocidad
#Fuerzas y coliciones
# visualzar la malla y poder mover materias



#Organizar los coeficientes y propiedades fisicas


# Billarpool

# Join Pop Corn
#   Context
#   Sphere

# Debugger
#  draw forces
#  Energy, momentum

# Pesrpective
# Light shadows




import csv
import tkinter as tk
import time
import math
from array import array
from typing import List, Union, Tuple
import random


class Matrix:
    def __init__(self, rows: int = None, columns: int = None, data: Union[List[List[float]], List[float]] = None):
        if isinstance(rows, list):
            data=rows
            rows=None
       
        if data is not None:
           
            if isinstance(data[0], list):
               
                self.rows = len(data)
                self.columns = len(data[0])
                self.data = array('f', [item for sublist in data for item in sublist])
            else:
                if rows*columns==len(data):
                    self.rows = rows
                    self.columns = columns
                    self.data = array('f', data)
                else:
                    raise ValueError("rows*columns!=len(data)")
        else:
            self.rows = rows
            self.columns = columns
            self.data = array('f', [0.0] * (self.rows * self.columns))

    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> float:
        if isinstance(index, int):
            if 0 <= index < self.rows * self.columns:
                return self.data[index]
            else:
                raise IndexError("Matrix indices out of range", index)
       
        if isinstance(index, tuple):
            i, j = index
            if isinstance(i, int) and isinstance(j, int):
                if 0 <= i < self.rows and 0 <= j < self.columns:
                    return self.data[i * self.columns + j]
                else:
                    raise IndexError("Matrix indices out of range", i, j)
            if isinstance(i, int) and isinstance(j, slice):
                raise IndexError("One slice is not allowed yet")
            if isinstance(i, slice) and isinstance(j, int):
                raise IndexError("One slice is not allowed yet")
            if isinstance(i, slice) and isinstance(j, slice):
                start_i, stop_i, step_i = i.indices(self.rows)
                start_j, stop_j, step_j = j.indices(self.columns)
                if step_i != 1 or step_j != 1:
                    raise IndexError("Step must be one")
                sliced_data = [self.data[r * self.columns + c] for r in range(start_i, stop_i, step_i) for c in range(start_j, stop_j, step_j)]
                return Matrix(stop_i - start_i, stop_j - start_j, sliced_data)
            else:
                raise IndexError("i,j indices are required")
        else:
            raise ValueError("i,j indices are required")

# Matrix is inmutable
    def __setitem(self, index: Tuple[int, int], value: float) -> None:
        row, col = index
        if row < 0 or row >= self.rows or col < 0 or col >= self.columns:
            raise IndexError("Invalid index")
        self.data[row * self.columns + col] = value

    def copy(self) -> 'Matrix':
        return Matrix(self.rows, self.columns, self.data.tolist())

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError("Matrices must have the same dimensions for addition.", self.rows, self.columns, other.rows, other.columns)
        result_data = [self.data[i] + other.data[i] for i in range(self.rows * self.columns)]
        return Matrix(self.rows, self.columns, result_data)

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        return self + ( other * -1)

    def __mul__(self, other: Union['Matrix', float]) -> 'Matrix':
        if isinstance(other, (int, float)):
            result = Matrix(self.rows, self.columns)
            for i in range(self.rows):
                for j in range(self.columns):
                    result.__setitem((i, j), self[i, j] * other)
            return result
        elif isinstance(other, Matrix):
            if self.columns != other.rows:
                raise ValueError("Number of columns of first matrix must be equal to number of rows of second matrix", self.rows, self.columns, other.rows, other.columns)
            result_data = [0]*(self.rows*other.columns)
            for i in range(self.rows):
                for j in range(other.columns):
                    for k in range(self.columns):
                        result_data[i*other.columns+ j]+=self[i, k] * other[k, j]
                        
            #print('mul',self,other,result)
            return Matrix(self.rows,other.columns,result_data)
        else:
            raise ValueError("Multiplication not defined for these data types",type(other))

    def __rmul__(self, other: float) -> 'Matrix':
        return other.__mul__(self)



    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        #if self.columns == other.rows:
        #    return self * other
        #elif
        if self.columns == other.rows - 1:
            return (self.tail() * other).untail()
        #elif self.columns - 1 == other.rows:
        #    return (self.untail() * other).tail()
        else:
            raise ValueError("Number of columns of first matrix must be equal to number of rows of second matrix", self.rows, self.columns, other.rows, other.columns)

    def __rmatmul__(self, other: 'Matrix') -> 'Matrix':
        return other.__matmul__(self)

    #@staticmethod
    def untail(m: 'Matrix') -> 'Matrix':
        return Matrix(m.rows, m.columns - 1, [m[i, j] for i in range(m.rows) for j in range(m.columns - 1)])
   
    #@staticmethod
    def tail(m: 'Matrix') -> 'Matrix':
        return Matrix(m.rows, m.columns + 1, [(m[i, j] if j != m.columns else 1) for i in range(m.rows) for j in range(m.columns + 1)])

    #@staticmethod
    def t(matrix: 'Matrix') -> 'Matrix':
        transposed_data = [matrix[j, i] for i in range(matrix.columns) for j in range(matrix.rows)]
        return Matrix(rows=matrix.columns, columns=matrix.rows, data=transposed_data)

    #@staticmethod
    def id(n: int) -> 'Matrix':
        data = [1.0 if i == j else 0.0 for i in range(n) for j in range(n)]
        return Matrix(rows=n, columns=n, data=data)
   
    #@staticmethod
    def Rz(rad: float) -> 'Matrix':
        data = [
            [math.cos(rad), -math.sin(rad), 0,0],
            [math.sin(rad), math.cos(rad), 0,0],
            [0, 0, 1,0],
            [0, 0, 0, 1]
        ]
        return Matrix(rows=3, columns=3, data=data)

    @staticmethod
    def rod_rot(angles_xyz):
        #Rodrigues' rotation formula
        angle=angles_xyz.norm()
        if angle > 1e-6:
            k = angles_xyz*(1/angle)
            K= Matrix([[0,    -k[2],  k[1], 0],
                       [k[2],  0,    -k[1], 0],
                       [-k[1], k[0],  0,    0],
                       [0,     0,     0,    1]])
            return ( Matrix.id(4) +
                     math.sin(angle) * K +
                     (1 - math.cos(angle)) * K * K)
        else:
            return Matrix.id(4)

    def __repr__(self) -> str:
        rows_repr = []
        for i in range(self.rows):
            row = [self.data[i * self.columns + j] for j in range(self.columns)]
            rows_repr.append("[" + ", ".join(map(str, row)) + "]")
        return "[" + ",\n ".join(rows_repr) + "]"

    def __or__(self,other):
        """
        concatenate vertically
        """
        if isinstance(other, Matrix) and self.columns == other.columns :
            return Matrix(self.rows + other.rows, self.columns,self.data+other.data)
        else:
            raise ValueError("Matrices of different columns cannot be stack", self.rows, self.columns, other.rows, other.columns)

    def __and__(self, other):
        """
        Concatenate two matrices horizontally.

        Args:
            other (Matrix): The second matrix to concatenate.

        Returns:
            Matrix: The resulting matrix after horizontal concatenation.
        """
        if self.rows != other.rows:
            raise ValueError("Matrices must have the same number of rows to concatenate horizontally")
       
        concatenated_data = []
        for i in range(self.rows):
            concatenated_data.extend(self.data[i*self.columns : (i+1)*self.columns])
            concatenated_data.extend(other.data[i*other.columns : (i+1)*other.columns])

        return Matrix(self.rows, self.columns + other.columns, concatenated_data)


    def norm(self):
        return math.sqrt(sum(a**2 for a in  self.data))
    
    def tolist(self):
        return list(self.data)


    def untail(matrix):  
        return Matrix(matrix.rows, matrix.columns-1, [matrix.data[i] for i in range(len(matrix.data)) if i % matrix.columns != matrix.columns-1])


    def tail(matrix):
        return Matrix(matrix.rows, matrix.columns+1, [(matrix.data[i * matrix.columns + j] if j != matrix.columns else 1) for i in range(matrix.rows) for j in range(matrix.columns+1)])

#     def inv(self):
# 
#         if self.rows != self.columns:
#             raise ValueError("Only square matrices can be inverted")
#         
#         n = self.rows
#         a = [[self[i, j] for j in range(n)] for i in range(n)]
#         inv = [[float(i == j) for j in range(n)] for i in range(n)]
# 
#         for i in range(n):
#             pivot = a[i][i]
#             if pivot == 0:
#                 raise ValueError("Matrix is singular and cannot be inverted")
#             
#             for j in range(n):
#                 a[i][j] /= pivot
#                 inv[i][j] /= pivot
#             
#             for k in range(n):
#                 if k != i:
#                     factor = a[k][i]
#                     for j in range(n):
#                         a[k][j] -= factor * a[i][j]
#                         inv[k][j] -= factor * inv[i][j]
#         
#         inv_data = [item for row in inv for item in row]
#         return Matrix(n, n, inv_data)
    
    


def Vec(*data,**kwargs):
    return Matrix(1,len(data),data,**kwargs)




class Scene:
    def __init__(self,transf= Matrix.id(4),**props):
        self.spheres=[]
        self.pipes=[]
        #self.canvases=[]
        self.props=props
        self.parent=None
        self.transformation =transf
        self.lin_vel=Vec(0,0,0)
        self.ang_vel=Vec(0,0,0)
        self.control=self.default_control


    def draw_spheres(self, vcam_rcanv):
        for sphere in self.spheres:
            sphere.draw(vcam_rcanv)
 

    def draw_pipes(self, vcam_rcanv):
        for pipe in self.pipes:
            pipe.draw(vcam_rcanv)
 
    def add_sphere(self,sphere):
            self.spheres.append(sphere)

    def add_pipe(self,pipe):
            self.pipes.append(pipe)




    def get_transf(self):
        return self.transformation
   
    def set_transf(self, transf:Matrix):
        self.transformation = transf
       
    def add_transf_angles(self,angles_xyz):
        #Rodrigues' rotation formula
        self.transformation=Matrix.rod_rot(angles_xyz)*self.transformation
       
   
 
    def get_pos(self):
        return self.transformation[3:,:3]   

    def set_pos(self,x,y=None,z=None):
        if y==None:
            z=x[2]
            y=x[1]
            x=x[0]
            #print('set_pos',x,y)
        self.transformation=self.transformation[0:3,:]|Vec(x,y,z,1)
       
    def add_pos(self,x,y=None,z=None):
        if y==None:
            z=x[2]
            y=x[1]
            x=x[0]
            #print('set_pos',x,y)
        self.transformation=self.transformation[0:3,:]|(self.get_pos()+Vec(x,y,z)).tail()

    def get_lin_vel(self):
        return self.lin_vel

    def set_lin_vel(self, x, y=None, z=None):
        if y is None:
            z = x[2]
            y = x[1]
            x = x[0]
        self.lin_vel = Vec([x, y, z])

    def add_lin_vel(self, x, y=None, z=None):
        if y is None:
            z = x[2]
            y = x[1]
            x = x[0]
        self.lin_vel = self.lin_vel + Vec([x, y, z])

    def get_ang_vel(self):
        return self.ang_vel

    def set_ang_vel(self, x, y=None, z=None):
        if y is None:
            z = x[2]
            y = x[1]
            x = x[0]
        self.ang_vel = Vec([x, y, z])

    def add_ang_vel(self, x, y=None, z=None):
        if y is None:
            z = x[2]
            y = x[1]
            x = x[0]
        self.ang_vel = self.ang_vel + Vec([x, y, z])

    def get_vels(self):
        return self.lin_vel & self.ang_vel

    def set_vels(self, vels):
        self.lin_vel = vels[:,:3]
        self.ang_vel = vels[:,3:]

    def add_vels(self, x, y=None, z=None):
        self.lin_vel = self.lin_vel + vels[:,:3]
        self.ang_vel = self.ang_vel + vels[:,3:]

    def update_acel_cte(self,t:float,lin_a:Matrix,ang_a:Matrix=Vec(0,0,0)):
        self.add_pos(self.get_lin_vel()*t + lin_a*(t*t/2))
        self.add_lin_vel(lin_a*t)
        self.add_transf_angles(self.get_ang_vel()*t + ang_a*(t*t/2))
        self.add_ang_vel(ang_a*t)

    @staticmethod
    def default_control(scene,t):
        lin_a=Vec(0,0,0)
        ang_a=Vec(0,0,0)
        scene.update_acel_cte(t,lin_a,ang_a)
        
    def refresh(self,t):
        for sphere in self.spheres:
            sphere.control(sphere,t)            
        

class Phisics_scene(Scene):
    
     def __init__(self,forces_params):
         super().__init__()
         self.forces_params=forces_params

     def grid_force(self,args):
        grid=(args|{'grid':50})['grid']
        for sphere_i in self.spheres:
            pos=sphere_i.get_pos().tolist()
            dx=(pos[0]%grid)-grid/2
            dy=(pos[1]%grid)-grid/2
            dz=(pos[2]%grid)-grid/2
            dif=Vec(dx,dy,dz)
            dist=dif.norm()
            dist=max(dist,grid/1000)
            f=dif*(-sphere_i.coef['grid_force']/dist)
            #print('grid',pos,dif,sphere_i.color,f)
            sphere_i.add_force( f)
        
        
     def collision_force(self,args):   
        n=len(self.spheres)
        for i in range(n):
           for j in range(i):
                disc_i = self.spheres[i]
                disc_j = self.spheres[j]
                dist=(disc_i.get_pos() - disc_j.get_pos()).norm()
                if dist<(disc_i.r+disc_j.r) :
                    dist=max(dist,(disc_i.r+disc_j.r)/100000)
                    f_dir_ji=(disc_i.get_pos() - disc_j.get_pos())*(1/dist)
                    elong=disc_i.r+disc_j.r-dist
                    k_elast=(disc_i.coef['elasticity'] + disc_j.coef['elasticity'])/2
                    f_ji=f_dir_ji * k_elast*(elong)
                    disc_i.add_force(f_ji) #colition
                    disc_j.add_force(f_ji*(-1)) #colition

            

     def viscosity_force(self,args):
        for sphere in self.spheres:
             sphere.add_force(sphere.get_lin_vel()*-sphere.coef['viscosity']) 
         
 

     def forces(self):
         if 'collision' in self.forces_params and self.forces_params['collision']['enabled'] :
             self.collision_force(self.forces_params['collision'])
         if 'viscosity' in self.forces_params and self.forces_params['viscosity']['enabled'] :
             self.viscosity_force(self.forces_params['viscosity'])
         if 'grid' in self.forces_params and self.forces_params['grid']['enabled'] :
             self.grid_force(self.forces_params['grid'])
             
             
     def refresh(self,t):
        self.forces()
        energ=0
        for sphere in self.spheres:
            #print('.',end='')
            sphere.control(sphere,t)
            energ+=sphere.get_lin_vel().norm()**2
        #print(energ,end=' ')
            

# materials= {
#     "Youngs_Modulus": {
#       "Steel": {"averaged": 200, "unit": "GPa"},
#       "Aluminum": {"averaged": 70, "unit": "GPa"},
#       "Concrete": {"averaged": 30, "min": 20, "max": 40, "unit": "GPa"},
#       "Rubber": {"averaged": 0.055, "min": 0.01, "max": 0.1, "unit": "GPa"}
#     },
#     "Poissons_Ratio": {
#       "Metals": {
#         "Steel_and_Aluminum": {"averaged": 0.3, "unit": ""}
#       },
#       "Rubber": {"averaged": 0.5, "unit": ""},
#       "Cork": {"averaged": 0, "unit": ""}
#     },
#     "Shear_Modulus": {
#       "Steel": {"averaged": 80, "unit": "GPa"},
#       "Aluminum": {"averaged": 26, "unit": "GPa"},
#       "Rubber": {"averaged": 0.0018, "min": 0.0006, "max": 0.003, "unit": "GPa"}
#     },
#     "Bulk_Modulus": {
#       "Steel": {"averaged": 160, "unit": "GPa"},
#       "Aluminum": {"averaged": 75, "unit": "GPa"},
#       "Glass": {"averaged": 45, "min": 35, "max": 55, "unit": "GPa"}
#     }
#   }


class Sphere(Scene):
    def __init__(self,scene_parent):
        super().__init__()
        self.scene_parent=scene_parent
        self.scene_parent.add_sphere(self)
        self.color='black'
        self.r = 10 
        self.force =Vec(0,0,0)
        self.torque=Vec(0,0,0)
        self.coef={
            'viscosity':0.1,
            'mass':1,
            'elasticity':1,
            'grid_force':0.1
            }
        self.label={}
        
    def add_force(self,f):
        self.force=self.force+f
 
    def clear_force(self):
        self.force=Vec(0,0,0)

    def add_torque(self,f):
        self.torque=self.force+f
 
    def clear_torque(self):
        self.torque=Vec(0,0,0)

    def r_canvas(self, vcam_rcanv):
       pos=self.get_pos()@self.scene_parent.get_transf()
       dist=(pos - vcam_rcanv.get_pos()).norm()
       [[i,j]]=vcam_rcanv.render_model(Vec(self.r,0,dist))
       return int(Vec(i,j).norm())
 
    

    def draw(self, vcam_rcanv):
       #print('*',end='')
       pos=self.get_pos()@self.scene_parent.get_transf()
       r=self.r_canvas( vcam_rcanv)
       center=vcam_rcanv.render_points(pos)
       vertex=[[center[0][0] - r, center[0][1] - r], [center[0][0] + r, center[0][1] + r]]
       #print('Sphere draw0 vertex',vertex,r,dist,pos,i,j)
       #print(self.get_pos())
       #print(dim)
       #print(self.scene_parent.get_transf())
       vcam_rcanv.oval(self,vertex, fill=self.color)
#       for poligon in self.poligons:
#           canvas.poly(poligon)

       if self.label!={}:
           vcam_rcanv.text([center[0][0] , center[0][1] + r], **self.label)

    @staticmethod
    def default_control(sphere,t):
        lin_a=sphere.force*(1/sphere.coef['mass'])
        ang_a=Vec(0,0,0)
        sphere.update_acel_cte(t,lin_a,ang_a)
        sphere.clear_force()
    
class Pipe:
    def __init__(self,scene,ini,end,color='#ccc'):
        self.ini_sphere=ini
        self.end_sphere=end
        self.color=color
        self.scene_parent=scene
        scene.add_pipe(self)




    def draw(self, vcam_rcanv):
            #z_conector=int(row['Conector'])
            ini_x,ini_y,ini_z=self.ini_sphere.get_pos().tolist()
            end_x,end_y,end_z=self.end_sphere.get_pos().tolist()
            #fin_x = int(courses[course_id]['Semestre'])*grid
            #fin_z = int(courses[course_id]['Malla Renglón'])*grid/1.5
            #ini_x = int(courses[prerequisite_id]['Semestre'])*grid
            #ini_z = int(courses[prerequisite_id]['Malla Renglón'])*grid/1.5
            
            #if ini_z==fin_z and ini_x  + grid == fin_x:
            points = Matrix(2,3,[
            ini_x, ini_y, ini_z,      
            end_x, end_y, end_z,      
            ])
            #else:
              
            
#                 if z_conector==0:
#                     if fin_z > ini_z:
#                         z_conector = ini_z + grid/2
#                     else:
#                         z_conector = ini_z-grid/2
#                 
#                 points = Matrix(6,3,[
#                     ini_x, y_conector, ini_z,      
#                     ini_x+grid/2, y_conector, ini_z,      
#                     ini_x+grid/2, y_conector, z_conector,      
#                     fin_x-grid/2, y_conector, z_conector,      
#                     fin_x-grid/2, y_conector, fin_z,      
#                     fin_x, y_conector, fin_z,      
#                 ])
#         
        
        
        #print('.')
            points3D=points@self.scene_parent.get_transf()
            points2D=vcam_rcanv.render_points(points3D)
            vcam_rcanv.line(self,points2D, fill=self.color)
        

class Mouse_Event:
    def __init__(self,x,y,state:int,z=0):
        self.x:float=x
        self.y:float=y
        self.z:float=z
        self.buttons_bin:int=buttons



class VCam_RCanv(Scene):
    '''
    Virtual Camera and Real Canvas with its Mouse 
    '''
    def __init__(self, scene: Scene,transf,height,width,fov=0,near=0.1,far=100):
        """
        for othographic use fov=0
        
        scene: Scene,  
        transf: Matrix,
        height:int, Pixels
        width:int, Pixels
        fov: Field of view — this is the vertical FOV, measured in degrees.
        near: Near clipping plane — any objects closer than this distance from the camera will not be rendered.
        far: Far clipping plane — any objects farther than this distance from the camera will not be rendered.
        """

        super().__init__(transf)
        self.scene = scene
        self.width=width
        self.height=height
        self.fov=fov
        self.near=near
        self.far=far
        self.shapes=[]
        self.last_mouse_button_event=None
        self.selected_object=None
        self.base=None

    def handle_mouse_button(self, event:Mouse_Event):
        type_event=int(event.type)
        print('mouse button event:',type_event,self.last_mouse_button_event)
        if type_event==5:
            self.last_mouse_button_event=None
            self.selected_object=None
            self.base=None
        else:
            self.last_mouse_button_event=event
            for shape in self.shapes:
                #print(shape['vertex'])
                x,y=event.x,event.y
                [[a_x,a_y],[b_x,b_y]]=shape['vertex']
                if a_x<x<b_x and a_y<y<b_y:
                    self.selected_object=shape['who']
                    print('a',self.selected_object.label['text'])
                    #self.base=Matrix(2,3,[1,0,0,0,1,0])@self.selected_object.scene_parent.get_transf().inv()
                    self.old_event=event
                    
                    break
            print('no')
            
            
        

    def handle_mouse_drag(self, event:Mouse_Event):
        print('mouse drag event:',event.type,self.last_mouse_button_event)
        x,y=event.x,event.y
        if self.selected_object:
            if isinstance(self.selected_object,Phisics_scene):
                # Transform the scene 
                print('uno')
            elif isinstance(self.selected_object,Sphere):#Falta probar
                # Add force to the sphere in terms of r
                #vec=Vec(x,y)*self.baseFaltarestarcamarayintercambiaryz
                rel=self.selected_object.r/self.selected_object.r_canvas(self)
                vec=Vec(x-self.old_event.x,0,y-self.old_event.y)*rel
                self.selected_object.add_pos(vec)
                self.old_event=event
                print('dos')
            else:
                #Print a mesage
                print('tres')
        else:
            print('no1')
 

    def draw_scene(self):
        self.delete()
        self.scene.draw_pipes(self)
        self.scene.draw_spheres(self)


    def render_model(self,points):
        d_inv=math.tan((self.fov/2)*math.pi/180)/self.height
        #print('render_model CameraMatr',points , self.transformation,d_inv)
        rows = points.rows
        result = []
        for i in range(rows):
            x3d,y3d,z3d=points[i:i+1,:].tolist()
            k=1/(1+z3d*d_inv)
            result.append([int(k*x3d),int(k*y3d)])
        #print(result)
        return result
        
    def render_points(self,points):
       #print('render_point CameraMatr',points , self.transformation,points@self.transformation)
       return self.render_model(points@self.transformation)
    
        
    def add_shape(self,shape,who,vertex):
        self.shapes.append({
            'shape':shape,
            'who':who,
            'vertex':vertex,
        })
          

    def poly(self,who,  vertex,**options)->int:
        '''
        vertex: Matrix; The first row is the top left corner
                        the second row is the bottom right corner
                        the draw is inside of the rectangle with these corners
        '''
        self.add_shape('poly',who,vertex)
        #raise NotImplementedError

    def oval(self,who, vertex, **options):        
        '''
        vertex: Matrix; The first row is the top left corner
                        the second row is the bottom right corner
                        the draw is inside of the rectangle with these corners
        '''
        self.add_shape('oval',who,vertex)
        #raise NotImplementedError


    def rect(self,who,  vertex, **options):
        '''
        vertex: Matrix; The first row is the top left corner
                        the second row is the bottom right corner
                        the draw is inside of the rectangle with these corners
        '''
        self.add_shape('rect',who,vertex)
#        raise NotImplementedError

    def line(self,who, vertex, **options):
        '''
        vertex: Matrix; The first row is the top left corner
                        the second row is the bottom right corner
                        the draw is inside of the rectangle with these corners
        '''
        self.add_shape('line',who,vertex)
        #raise NotImplementedError

    def text(self, vertex,**options):
        '''
        vertex: Matrix; The first row is the top left corner
                        the second row is the bottom right corner
                        the draw is inside of the rectangle with these corners
        '''
        #raise NotImplementedError
        pass

    def debug(self,text,**options):
        '''
        print text in the canvas in default possition
        '''
        raise NotImplementedError
   
   
    def delete(self):
        '''
        delete all objects
        '''
        self.whos={}
        #raise NotImplementedError


import tkinter as tk
class Canvas_Tkinter(VCam_RCanv):

    def __init__(self,scene,transf,**props):#transf=None,height=900,width=1800,tk_master=None,grid=10 ):
        props={'height':600,'width':600} | props
        super().__init__(scene,transf,height=props['height'],width=props['width'])
        self.props=props
        m,n=props['height'],props['width']
        if 'tk_master' not in props: 
            props['tk_master'] = tk.Tk()
        self.canvas = tk.Canvas(props['tk_master'],height=m,width=n,bg='#063')#, **subset)
        self.canvas.pack()


        # Bind mouse events to handler methods
        #self.canvas.bind("<Motion>", self.handle_mouse_move)
        self.canvas.bind("<ButtonPress>", self.handle_mouse_button)
        self.canvas.bind("<ButtonRelease>", self.handle_mouse_button)
        self.canvas.bind("<B1-Motion>", self.handle_mouse_drag)


#         if 'transf' not in props:
#             px_cm=100/100#min(m,n)/50
#             transf=Matrix(4,4, [px_cm,0,0,0,
#                                 0,px_cm,0,0,
#                                 0,0,1,0,
#                                 0,0,0,1])
#             props['transf']=transf
#         self.transf=props['transf']
# 
#
    def swap_vert(self,vertex):
        '''
        TODO: flip vertical canvas to set 0,0 the left down corner
        '''
        pass
        

    def oval(self,who, vertex,**options)->int:
        super().oval(who, vertex,**options)
        return self.canvas.create_oval(vertex,**options)

    def rect(self,who,  vertex,**options)->int:
        super().rect(who, vertex,**options)
        return self.canvas.create_rectangle(verte,**options)

    def text(self,  vertex,**options)->int:
        super().text( vertex,**options)
        options=options|{'justify':'center','anchor':'n'}
        return self.canvas.create_text(vertex,**options)

    def debug(self, text)->int:
        return self.canvas.itemconfig(self.debug_id,text=text)

    def line(self,who, vertex,**options)->int:
        super().line(who, vertex,**options)
        return self.canvas.create_line(vertex,**options)

    def poly(self,who,  vertex,**options)->int:
        super().poly(who, vertex,**options)
        return self.canvas.create_polygon(vertex,**options)

    def draw_grid(self, width, height, interval,color):
        wh=Vec(width,height)@self.transf
        width=wh[0]
        height=wh[1]
        for x in range(0, width, interval):
            self.create_line(x, 0, x, height, fill=color, dash=(2, 2))

        # Dibujar líneas horizontales
        for y in range(0, height, interval):
            self.create_line(0, y, width, y, fill=color, dash=(2, 2))



    def delete(self):
        super().delete()
        self.canvas.delete('all')

class Context:
    def __init__(self):
        pass
    

    def vcam_rcanv(self,scene,transf,**props):
        raise NotImplementedError

import tkinter as tk
class Context_Tkinter(Context):
    def __init__(self):
        super().__init__()
        self.master=tk.Tk()
        self.mainloop=self.master.mainloop
        self.after_ms=self.master.after
        self.canvases=[]

   
    def vcam_rcanv(self,scene,transf,**props):
        canvas = Canvas_Tkinter(scene,transf,tk_master=self.master,**props)
        self.canvases.append(canvas)
        return canvas


    
        


