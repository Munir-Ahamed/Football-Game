from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *
from ursina.shaders import basic_lighting_shader
import serial

app = Ursina()

# Sky
Sky(texture='sky2', texture_scale=(4,2))

# Player
player = FirstPersonController(x=3, y=0, origin_y=0, speed=10)

# Ground
ground_length = 120
ground_width = 70
ground = Entity(model='plane', scale=(ground_length,1,ground_width), texture='ground2',
                texture_scale=(1,1), collider='box', position=(0,0,0), shader=basic_lighting_shader)

# Net
net1 = Entity(model='cube', position=((ground_length*0.5)-5,2,0), scale=(0.1,4,14), texture='net', color=color.white33,
             collider='box', texture_scale=(3.5,1), rotation=(0,0,0), rigidbody='dynamic')
net2 = duplicate(net1, scale=(2,4,0.1), position=((ground_length*0.5)-6,2,7), texture_scale=(0.5,1))
net3 = duplicate(net1, scale=(2,4,0.1), position=((ground_length*0.5)-6,2,-7), texture_scale=(0.5,1))
net4 = duplicate(net1, scale=(2,0.1,14), position=((ground_length*0.5)-6,4,0), texture_scale=(1,3.5))

# Post
post1 = Entity(model='cube', position=((ground_length*0.5)-7,2,-7), scale=(0.1,4,0.1), color=color.black,
             collider='box', rotation=(0,0,0))
post2 = duplicate(post1, z=7)
post3 = duplicate(post1, scale=(0.1,0.1,14), position=((ground_length*0.5)-7,4,0))

# Boundary
wall1 = Entity(model='cube', scale=(0.1,2,ground_width), texture='ad1', position=((ground_length*0.5),1,0),
               texture_scale=(25,1), collider='box')
wall2 = duplicate(wall1, scale=(ground_length,2,0.1), position=(0,1,-(ground_width*0.5)))
wall3 = duplicate(wall1, scale=(ground_length,2,0.1), position=(0,1,(ground_width*0.5)))
wall4 = duplicate(wall1, position=(-(ground_length*0.5),1,0))

# Stadium
crowd1 = Entity(model='cube', scale=(0.1,12,ground_width+20), texture='crowd4', position=((ground_length*0.5)+7,4,0),
                texture_scale=(10,1.6), collider='box', rotation=(0,0,20))
crowd2 = duplicate(crowd1, scale=(ground_length+20,12,0.1), position=(0,4,(-ground_width*0.5)-7), rotation=(-20,0,0))
crowd3 = duplicate(crowd1, scale=(ground_length+20,12,0.1), position=(0,4,(ground_width*0.5)+7), rotation=(20,0,0))
crowd4 = duplicate(crowd1, position=((-ground_length*0.5)-7,4,0), rotation=(0,0,-20))

# Football
ball = Entity(model='sphere', scale=(0.5,0.5,0.5), position=(7,0.25,0),
               collider='sphere', texture='football', texture_scale=(2,2), rigidbody='dynamic', shader=basic_lighting_shader)
ball.velocity = Vec3(0, 0, 0)

# Obstacle
obstacle1 = Entity(model='cube', scale=(0.02,3.1,1.75), texture='target1', position=(post3.x-10,0,0)
                   ,texture_scale=(1,1), collider='box', origin_y=-0.5)
obstacle2 = duplicate(obstacle1,x=post3.x-20, z=0)
obstacle3 = duplicate(obstacle1,x=post3.x-15, z=0)
obs_vel1, obs_vel2, obs_vel3 = 7, -5, 4
obstacle1.velocity = Vec3(0,0,obs_vel1)
obstacle2.velocity = Vec3(0,0,obs_vel2)
obstacle3.velocity = Vec3(0,0,obs_vel3)

# Target
target1 = Entity(model='cube', scale=(0.1,1.5,1.5), texture='target2', position=(post1.x,post1.scale_y-0.75,post3.scale_z*0.5-0.75) 
                 ,texture_scale=(1,1), collider='box')
target2 = duplicate(target1, position=(post1.x,post1.scale_y-0.75,-post3.scale_z*0.5+0.75))
target3 = duplicate(target1, position=(post1.x,post1.scale_y-0.75,0))
target1.velocity = Vec3(0,0,0)
target2.velocity = Vec3(0,0,0)
target3.velocity = Vec3(0,0,0)

# Sun
sun = Entity(model=Cylinder(100, start=0), scale=(20,0.1,20), position=(-200,80,-180), rotation=(30,-40,90), texture='sun2')
point_light = PointLight(color = color.white, energy = 2.0, attenuation = (0, 0, 0))
point_light2 = PointLight(color = color.white, energy = 10.0, attenuation = (0, 0, 0))
point_light3 = PointLight(color = color.white, energy = 10.0, attenuation = (0, 0, 0))

# Position the light
point_light.position = (-550,120,-200)
point_light2.position = (0,2,0)
point_light3.position=(-190,80,-150)
point_light.shadow_caster = True
point_light2.shadow_caster = True
ground.receive_shadows = True

# Win pop up
text1 = Text(text='Won',  background=True, background_scale=(1.2, 1.2), scale=4, position=(-0.1,0.1), color=color.violet)
text2 = Text(text='Restart? press enter', position=(-0.1,0), color=color.red)
start = Text(text='0', position=(0,0), color=color.red)
text1.enabled=False
text2.enabled=False
start.enabled=False

# Kick
def kick(vel_xz, vel_y, dir):
    direction = dir.normalized()
    ball.velocity.x = 1.2*vel_xz*direction.x
    ball.velocity.y = vel_y
    ball.velocity.z = vel_xz*direction.z
    ball.rotation_y = 120
    ball.rotation_z = 120
    
    return ball.velocity

# Target fall intiation
def fall(entity):
    entity.velocity = Vec3(0,-0.2,0)

# Obstacle fallintiation
def drop(entity):
    entity.velocity = Vec3(0.1,0,0)

def update():
    global resistance
    global text1, text2

    if start.text=='1': start.x += 2*time.dt
    print(start.x)

    if(start.x>15 and start.x<29) :
        resistance = 0.7
        kick(30,8,Vec3(1,0,0))
        start.x = 30

    if(start.x>45 and start.x<59) :
        ball.position = (7,0.25,0)
        ball.velocity.x = 0
        ball.velocity.y = 0
        ball.velocity.z = 0
        resistance = 0.7
        kick(30,8,Vec3(7,0,-1))
        start.x = 60

    if(start.x>75 and start.x<89) :
        ball.position = (7,0.25,0)
        ball.velocity.x = 0
        ball.velocity.y = 0
        ball.velocity.z = 0
        resistance = 0.7
        kick(30,8,Vec3(7,0,1))
        start.x = 90    
    # Ball movement
    ball.y += ball.velocity.y * time.dt
    ball.x += ball.velocity.x * time.dt
    ball.z += ball.velocity.z * time.dt

    # Ball rotation
    ball_dir = ball.velocity.normalized()
    if ball.velocity.length() > 8 :
        ball.rotation_y += ball_dir.y*180* time.dt
        ball.rotation_x += ball_dir.x*180 * time.dt
        ball.rotation_z += ball_dir.z*180 * time.dt
    if ball.velocity.length() > 4 or ball.position.y>3 :
        ball.rotation_x += ball_dir.x*120 * time.dt
        ball.rotation_y += ball_dir.y*120 * time.dt
        ball.rotation_z += ball_dir.z*120 * time.dt
    if ball.velocity.length() > 2 or ball.position.y>1 :
        ball.rotation_x += ball_dir.x*60 * time.dt
        ball.rotation_y += ball_dir.y*60 * time.dt
        ball.rotation_z += ball_dir.z*60 * time.dt
    
    # Gravity
    if ball.y > 0.25:
        ball.velocity.y -= 8 * time.dt

    # Bouncing
    if ball.y < 0.25:
        ball.velocity.y = abs(ball.velocity.y) * 0.8

    # Friction
    if ball.y > 0.248 and ball.y < 0.252:
        if ball.velocity.x!=0: ball.velocity.x -= (abs(ball.velocity.x)/ball.velocity.x)*15*time.dt
        if ball.velocity.z!=0: ball.velocity.z -= (abs(ball.velocity.z)/ball.velocity.z)*15*time.dt
    if ball.y > 0.24 and ball.y < 0.25:
        if ball.velocity.x!=0: ball.velocity.x -= (abs(ball.velocity.x)/ball.velocity.x)*10*time.dt
        if ball.velocity.z!=0: ball.velocity.z -= (abs(ball.velocity.z)/ball.velocity.z)*10*time.dt
    if ball.y > 0.23 and ball.y < 0.27:
        if ball.velocity.x!=0: ball.velocity.x -= (abs(ball.velocity.x)/ball.velocity.x)*10*time.dt
        if ball.velocity.z!=0: ball.velocity.z -= (abs(ball.velocity.z)/ball.velocity.z)*10*time.dt

    # Air drag
    if ball.velocity.x >0:
        ball.velocity.x -= resistance*time.dt
    if ball.velocity.x <0:
        ball.velocity.x -= -resistance*time.dt
    if ball.velocity.z >0:
        ball.velocity.z -= resistance*time.dt
    if ball.velocity.z <0:
        ball.velocity.z -= -resistance*time.dt

    # Bounded ball
    ball.x = clamp(ball.x, -ground_length*0.5, ground_length*0.5)
    ball.z = clamp(ball.z, -ground_width*0.5, ground_width*0.5)
    
    # Deflection and collisions
    hit_info = ball.intersects()
    hit_obj = hit_info.entity
    
    if hit_info.hit:
        if hit_obj==wall2 :
            ball.velocity.z = ball.velocity.z*(-0.3)
        if hit_obj==wall3 :
            ball.velocity.z = ball.velocity.z*(-0.3)
        if hit_obj==wall1 :
            ball.velocity.x = ball.velocity.x*(-0.3)
        if hit_obj==wall4 :
            ball.velocity.x = ball.velocity.x*(-0.3)
        if hit_obj==net1 :
            ball.velocity.x = ball.velocity.x*(-0.1)
        if hit_obj==net2 :
            ball.velocity.z = ball.velocity.z*(-0.8)
        if hit_obj==net3 :
            ball.velocity.z = ball.velocity.z*(-0.8)
        if hit_obj==net4 :
            ball.velocity.y = ball.velocity.y*(-0.8)
        if hit_obj==target1 :
            fall(target1)
        if hit_obj==target2 :
            fall(target2)
        if hit_obj==target3 :
            fall(target3)
        if hit_obj==obstacle1 :
            drop(obstacle1)
        if hit_obj==obstacle2 :
            drop(obstacle2)
        if hit_obj==obstacle3 :
            drop(obstacle3)
    
    # Goal 
    if ball.position.x<net1.position.x and ball.position.x>post3.position.x+0.1 :
        if ball.position.z<net2.position.z and ball.position.z>net3.position.z :
            if ball.position.y<post3.position.y and ball.position.y>0.25:
                text1.enabled=True
                text2.enabled=True
                player.enabled = False

    # Obstacle movement and fall animation
    try : 
        if obstacle1.z>ground_width*0.5-20 : obstacle1.velocity.z = -obs_vel1
        if obstacle1.z<-ground_width*0.5+20: obstacle1.velocity.z = obs_vel1
        obstacle1.z += obstacle1.velocity.z * time.dt
        if obstacle1.velocity.x>0 and obstacle1.rotation_z<90 : obstacle1.rotation_z += 180*time.dt
        if obstacle1.rotation_z >= 90 : destroy(obstacle1)
    except:
        pass

    try : 
        if obstacle2.z>ground_width*0.5-20 : obstacle2.velocity.z = obs_vel2
        if obstacle2.z<-ground_width*0.5+20: obstacle2.velocity.z = -obs_vel2
        obstacle2.z += obstacle2.velocity.z * time.dt
        if obstacle2.velocity.x>0 and obstacle2.rotation_z<90 : obstacle2.rotation_z += 180*time.dt
        if obstacle2.rotation_z >= 90 : destroy(obstacle2)
    except:
        pass

    try : 
        if obstacle3.z>ground_width*0.5-20 : obstacle3.velocity.z = -obs_vel3
        if obstacle3.z<-ground_width*0.5+20: obstacle3.velocity.z = obs_vel3
        obstacle3.z += obstacle3.velocity.z * time.dt
        if obstacle3.velocity.x>0 and obstacle3.rotation_z<90 : obstacle3.rotation_z += 180*time.dt
        if obstacle3.rotation_z >= 90 : destroy(obstacle3)
    except:
        pass  

    # Target fall animation
    try :
        target1.y += target1.velocity.y * time.dt
        if target1.velocity.length() > 0.1 : 
            target1.rotation_z += 180 * time.dt
        if target1.position != (post1.x,post1.scale_y-0.75,post3.scale_z*0.5-0.75) :
            if target1.y > 0.25: target1.velocity.y -=  8* time.dt
            else : destroy(target1)
    except :
        pass
    try :
        target2.y += target2.velocity.y * time.dt
        if target2.velocity.length() > 0.2 : 
            target2.rotation_z += 180 * time.dt
        if target2.position != (post1.x,post1.scale_y-0.75,-post3.scale_z*0.5+0.75) :
            if target2.y > 0.25: target2.velocity.y -=  8* time.dt
            else : destroy(target2)
    except :
        pass
    try :
        target3.y += target3.velocity.y * time.dt
        if target3.velocity.length() > 0.1 : 
            target3.rotation_z += 180 * time.dt
        if target3.position != (post1.x,post1.scale_y-0.75,0) :
            if target3.y > 0.25: target3.velocity.y -=  8* time.dt
            else : destroy(target3)
    except :
        pass

def input(key):
    global resistance
    dist = (player.position - ball.position).length()
    # if key == 'x' and dist<2.5:
    #     resistance=0.2
    #     kick(50,7)

    # if key == 'c' and dist<2.5:
    #     resistance=0.7
    #     kick(13,12)
        
    # if key == 'v' and dist<2.5:
    #     resistance=0.1
    #     kick(80,2)

    if key == 'r':
        ball.position = (7,0.25,0)
        ball.velocity.x = 0
        ball.velocity.y = 0
        ball.velocity.z = 0

    if key == 'm':
        start.text = '1'

    if player.enabled==False and key=='enter' and text1 is not None:
        player.enabled = True
        text1.enabled=False
        text2.enabled=False
        ball.position=(7,0.25,0)
        ball.velocity.x = 0
        ball.velocity.y = 0
        ball.velocity.z = 0

app.run()