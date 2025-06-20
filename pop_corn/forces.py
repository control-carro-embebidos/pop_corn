def collision(scene):
    self=scene
    n=len(self.discs) #No. total de objetos de Discen scene
    for i in range(n): #Itera desde el primer disco hasta el último
       for j in range(i): #itera desde el primer disco (índice 0) hasta el disco anterior al disco i actual (índice i-1).
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

def magnetic(scene):
#     u = 4*(3.1416)*10**(-7)
#     N = 70
#     I = 0.8
#     A = 2
    #k_mag = 1
    min_dist = 0.001
    self=scene
    n=len(self.discs) #No. total de objetos de Discen scene
    for i in range(n): #Itera desde el primer disco hasta el último
       for j in range(i): #itera desde el primer disco (índice 0) hasta el disco anterior al disco i actual (índice i-1).
            disc_i = self.discs[i] 
            disc_j = self.discs[j]
            dist=(disc_i.get_pos() - disc_j.get_pos()).norm()+ min_dist
    
            #1er caso: 2 son magneticos
            F_mm = disc_i.k_mag*disc_j.k_mag/(dist**2) 
            #2caso: i es magnetico j ferromagnetico
            F_mf = disc_i.k_mag*disc_j.k_ferromag/(dist**2) 
            #3er caso: i es ferro y j es magnetico
            F_fm = disc_i.k_ferromag*disc_j.k_mag/(dist**2)
            
            F_total = F_mm + F_mf + F_fm
            #dist=min(disc_i.r,disc_j.r)
            disc_i.add_force((-1)*F_total)  # Atraction force  
            disc_j.add_force(F_total)  # Atraction force  

            pass
            
            #F= uo*N*I*A/(2*(r)**2)
    


    
    