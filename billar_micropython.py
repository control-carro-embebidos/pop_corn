if __name__ == "__main__":

    from machine import Timer
    from pop_corn.Matrix import Matrix, Vec
    from pop_corn.Scene import Scene
    from Disc import Disc
    from Canvas_print import Canvas_print

    scene = Scene(0x00ff00)
    disc = Disc(scene)
    scene.add_disc(disc)
    
    canvas = Canvas_print()
    scene.subscribe_canvas(canvas)
    
    t_anim = 50
    
    disc = Disc(scene)
    disc.color='black'
    disc.set_pos(-15,0)
    disc.vel=Vec(0.5,0.05)
    scene.add_disc(disc)
    
    def anim(timer):
        scene.anim()
    
    timer=Timer()
    timer.init(period=2000, mode=Timer.PERIODIC, callback=anim)
 
 
