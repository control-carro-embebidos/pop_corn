def collision(scene):
    self=scene
    n=len(self.discs)
    for i in range(n):
       for j in range(i):
            disc_i = self.discs[i] 
            disc_j = self.discs[j]
            #if disc_i.isparent(disc_j) or disk_j()
            dist=(disc_i.get_pos() - disc_j.get_pos()).norm()
            if dist<(disc_i.r+disc_j.r) :
                if dist<(disc_i.r+disc_j.r)/100:
                    dist=(disc_i.r+disc_j.r)/100
                f_dir_ji=(disc_i.get_pos() - disc_j.get_pos())*(1/dist)
                dist=min(dist,disc_i.r,disc_j.r)
                k_elast=(disc_i.k_elast + disc_j.k_elast)/2
                f_ji=k_elast*dist*f_dir_ji
                disc_i.add_force(f_ji) #colition
                disc_j.add_force((-1)*f_ji) #colition

def viscosity(scene):

    for disc in scene.discs:
        #f_mag=self.magnetic(disc)
        #disc.add_force(f_mag) #Magnetic Force floor
        
        #Parent attractor

        disc.add_force(-disc.k_frict*disc.get_vel())  # friction
