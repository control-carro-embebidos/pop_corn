


def control1( disc,t):
        global cont_train,train
      #if repeat:
#conntrol
        #print(disc.things['sensors'])
        sensors_d=disc.things['sensors']
        transf_dad=disc.get_transf()
        n=len(sensors_d)
        n_2=n//2
        sensors_pos = []
        for disc_i in sensors_d:
            
            items=(disc_i.get_pos()@transf_dad@Matrix(2,2,[0,1,1,0])).tolist()
            #print('items',items)
            for item in items:
                sensors_pos.append(item)
        sensors_pos=Matrix(n,2,sensors_pos)
        floor_colors = disc.scene.get_background_at(sensors_pos)
        #print('disc',disc.get_pos())
 #   if train:
        #master.after(30,train_control)
        acc_prod=0
        acc_vals=0
        for i,f_color in enumerate(floor_colors):
            f_color=255-f_color
            acc_prod += f_color*(i-n_2)
            acc_vals += f_color
        if acc_vals==0:
            index_maxval=0
        else:
            index_maxval=acc_prod/acc_vals
        #print(floor_colors,index_maxval,acc_prod,acc_vals)
        k_giro=0.5
        v_i=5 + k_giro*(index_maxval/n_2) # 5 cm/s sería la velocidad media del carro
        v_d=5 - k_giro*(index_maxval/n_2)
        motors_vel= Matrix(1,2,[v_i,v_d])


#        perceptron.train(floor_colors*(1/255), motors_vel*(1/5))
#     else:
#         master.after(10,train_control)
#         prediction=perceptron.predict(floor_colors*(1/255))*5
#         car.v_i = prediction[0,0]
#         car.v_d = prediction[0,1]
#         #print('predic', prediction)
#Cinnematicadirecta
        r=1#wheel radio
        b=1
        y=0
        x = (motors_vel[0] * r + motors_vel[1] * r) / 2* t
        omega_robot = (motors_vel[1] * r - motors_vel[0] * r) / (2 * b)* t
        desp = Matrix(1,2,[x,y])@Matrix.rot2D(disc._angle)
        disc.add_angle(omega_robot)
        disc.add_pos(desp)




if __name__ == "__main__":

    from pop_corn.matrix import Matrix, Vec
    from pop_corn.scene import Scene
    from pop_corn.mainscene import MainScene
    from pop_corn.disc import Disc
    from pop_corn.py.canvas_Tkinter import Canvas_Tkinter
    import tkinter as tk

    master = tk.Tk()
    scene = MainScene(data_grayscale=Matrix.load_file('img/UD_@8_540_483.pgm'))#bg='img/UD_@8.xbm', foreground="white", background="black")
    disc0 = Disc(scene)
    disc0.set_pos(5,0)
    #scene.add_disc(disc)
    
    
    t_anim = 50
    
    disc1 = Disc(scene)
    disc1.r=10
    sensors_ini_pos=Matrix(5,2,[
        10,10,
        10,5,
        10,0,
        10,-5,
        10,-10
        ])
    sensors_d=[]
    for i in range(sensors_ini_pos.m):
        sd=Disc(disc1)
        sd.r = 3
        sd.color='green'
        sd.set_pos(sensors_ini_pos[i,0],sensors_ini_pos[i,1])
        sensors_d.append(sd)
    disc1.things['sensors']=sensors_d
    disc1.control=control1
    disc1.color='blue'
    disc1.set_pos(10,-100)
    disc1.set_vel(Vec(0,5))

    canvas = Canvas_Tkinter(scene, tk_master=master)
    scene.subscribe_canvas(canvas)

    def anim_loop():    
        master.after(t_anim,anim_loop)
        scene.refresh()

  
    anim_loop() 
    master.mainloop()
    
    


#########################
'''    
    
    # Example usage
if __name__ == "__main__":

    from Car import Car
    from Scene import Speedway
    import tkinter as tk


    master = tk.Tk()
    
    perceptron = Perceptron(name_or_input_size=7, output_size=2)    
    
    train=True
    #repeat=True
    
    speedway = Speedway(master)
    car = Car()
    speedway.add_car(car)


    def enter(event):
        global train
        train=not(train)
        print('train: ',train)
        perceptron.save_file("car.txt")
        
    def load(event):
        global perceptron
        perceptron = Perceptron("car.txt") 
        print('load: ',load)
       

    master.bind("<Return>", enter)
    master.bind("<space>", load)

    def train_control():
        global cont_train,train
      #if repeat:
       
        floor_colors = Matrix(1,7,speedway.read_floor_color_gray(car.get_sensors_coord()))
        if train:
            master.after(30,train_control)
            maxval=0
            index_maxval=11
            for i in range(7):
                if floor_colors[0,i]>maxval:
                    maxval=floor_colors[0,i]
                    index_maxval=i-4
            car.v_i=5 - index_maxval/3
            car.v_d=5 + index_maxval/3
            motors_vel= Matrix(1,2,[car.v_i,car.v_d])

            cont_train +=1
            if cont_train%100==0:
                print(cont_train,perceptron.predict(floor_colors*(1/255))*5-motors_vel)
            if cont_train==10000:
                train=False

            perceptron.train(floor_colors*(1/255), motors_vel*(1/5))
        else:
            master.after(10,train_control)
            prediction=perceptron.predict(floor_colors*(1/255))*5
            car.v_i = prediction[0,0]
            car.v_d = prediction[0,1]
            #print('predic', prediction)
                
    cont_train =0
    speedway.anim()
    train_control()
    master.mainloop()

#     # Example usage
#     # Define training data (inputs) and their respective labels (labels)
#     inputs = Matrix(2,3, [0, 0, 1, 
#                            1, 0, 0])
#     labels = Matrix(2, 2, [0, 1,
#                            1, 0])
# 
# 
#     # Create a perceptron with 2 inputs and 2 outputs
#     perceptron = Perceptron(input_size=inputs.n, output_size=labels.n)
# 
#     # Define training data (inputs) and their respective labels (labels)
#     inputs = Matrix(2, 3, [0, 0, 1,0,1,0])
#     labels = Matrix(2, 2, [0, 1,1,0])
# 
#     # Train the perceptron
#     perceptron.train(inputs, labels,epochs=100)
# 
#     # Make predictions
#     print("Predictions after training:")
#     for i in range(inputs.m):
#         input_i=inputs[i:i+1,:]#[i*inputs.n:(i+1)*inputs.n]
#         prediction = perceptron.predict(input_i)
#         print(f"Inputs: {input_i} -> Prediction: {prediction}")



'''

