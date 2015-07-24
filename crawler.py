'''
Quadruped robot test program

RegisHsu
2015-07-20

'''

from visual import *

body_x = 70
body_y = 70
body_z = 25

coxa_len = 28
femur_len = 55
tibia_len = 81

x_offset = body_x / 2
y_offset = body_y / 2
z_offset = body_z / 2

z_ground = - z_offset
z_stand = -tibia_len/2

x_default = (coxa_len + femur_len) * cos(pi/4)
y_default = (coxa_len + femur_len) * cos(pi/4)
z_default = z_stand

x_current = 0
y_current = 0
z_current = 0

STAY = 255

coxa = [0,1,2,3]
femur = [0,1,2,3]
tibia = [0,1,2,3]


'''
    draw global X/Y/Z axis
'''
golbal_frame = frame()
curve(frame=golbal_frame, pos=[(0,0,0),(0,0,250)], color=color.red)
curve(frame=golbal_frame, pos=[(0,0,0),(0,250,0)], color=color.green)
curve(frame=golbal_frame, pos=[(0,0,0),(250,0,0)], color=color.blue)


'''
    create legs
'''
def create_legs(i):
    #coxa_frame = frame(pos=(body_x/2,body_y/2,body_z/2),axis=(1,0,0))
    coxa_frame = frame(pos=(0,0,0),axis=(1,0,0))
    cylinder(frame=coxa_frame, pos=(0,0,0), length=coxa_len, radius=6, color=color.red)

    femur_frame = frame(frame = coxa_frame, pos=(coxa_len,0,0),axis=(1,0,0))
    cylinder(frame=femur_frame, pos=(0,0,0), length=femur_len, radius=6, color=color.green)

    tibia_frame = frame(frame = femur_frame, pos=(femur_len,0,0),axis=(0,0,-1))
    cylinder(frame=tibia_frame, pos=(0,0,0), length=tibia_len, radius=6, color=color.blue)
    return (coxa_frame, femur_frame, tibia_frame)

'''
axis to angle calculation
'''
def axis_to_angle(x,y,z):

    if (x >=0):
        w = sqrt(pow(x, 2) + pow(y, 2))
    else:
        w = -1 * (sqrt(pow(x, 2) + pow(y, 2)))

    v = w - coxa_len
    alpha = atan2(z, v) + acos((pow(femur_len, 2) - pow(tibia_len, 2) + pow(v, 2) + pow(z, 2)) / 2 / femur_len / sqrt(pow(v, 2) + pow(z, 2)))
    beta = acos((pow(femur_len, 2) + pow(tibia_len, 2) - pow(v, 2) - pow(z, 2)) / 2 / femur_len / tibia_len)

    if (w >= 0):
        gamma = atan2(y, x)
    else:
        gamma = atan2(-y, -x)
    return (alpha, beta, gamma)

'''
    draw legs
'''
def draw_legs(leg,a,b,g):
    x_dir = 1
    y_dir = 1
    z_dir = -1

    if (leg == 0):
        x_dir = 1
        y_dir = 1
        z_dir = -1
    if (leg == 1):
        x_dir = 1
        y_dir = -1
        z_dir = -1
    if (leg == 2):
        x_dir = -1
        y_dir = 1
        z_dir = -1
    if (leg == 3):
        x_dir = -1
        y_dir = -1
        z_dir = -1

    coxa[leg].axis = (x_dir * cos(g), y_dir * sin(g), 0)
    femur[leg].axis = (cos(a),0,sin(a))
    tibia[leg].axis = (-cos(b),0,-sin(b))

    coxa[leg].pos = (x_dir*x_offset, y_dir*y_offset, z_offset)
    #femur[leg].pos = (cos(a),0,sin(a))
    #tibia[leg].pos = (-cos(b),0,-sin(b))


    # for test, Regis
    #coxa_frame.rotate(angle=(g/180*pi),axis=(0,0,1))
    #femur_frame.rotate(angle=(a/180*pi),axis=(0,1,0))
    #tibia_frame.rotate(angle=(b/180*pi),axis=(0,1,0))
    return

'''
    set the legs position
'''
def set_legs(leg,x,y,z):
    global x_current,y_current,z_current

    if (x != STAY):
        xx = x
    else:
        xx = x_current

    if (y != STAY):
        yy = y
    else:
        yy = y_current

    if (z != STAY):
        zz = z
    else:
        zz = z_current


    z_current = zz
    y_current = yy
    x_current = xx

    a,b,g = axis_to_angle(xx,yy,zz)
    #print "alpha, beta, gamma =%f %f %f" %(a, b, g)
    draw_legs(leg,a,b,g)
    return

'''
    sit down
'''
def sit():
    for leg in range(0,4):
        set_legs(leg, STAY, STAY, z_ground)

'''
    stand up
'''
def stand():
    for leg in range(0,4):
        set_legs(leg, STAY, STAY, z_stand)

def set_body(x,y,z):
    set_legs(0, x_default - x, y_default - y, z_default - z)
    set_legs(1, x_default - x, y_default + y, z_default - z)
    set_legs(2, x_default + x, y_default - y, z_default - z)
    set_legs(3, x_default + x, y_default + y, z_default - z)


def set_body_dt(dx,dy,dz):
    set_site(0, site_now[0][0] - dx, site_now[0][1] - dy, site_now[0][2] - dz)
    set_site(1, site_now[1][0] - dx, site_now[1][1] + dy, site_now[1][2] - dz)
    set_site(2, site_now[2][0] + dx, site_now[2][1] - dy, site_now[2][2] - dz)
    set_site(3, site_now[3][0] + dx, site_now[3][1] + dy, site_now[3][2] - dz)


def body_move_test(move_length, move_up, m_delay):
    for i in range(0,move_length,2):
        set_body(0, i, 0)
        sleep(m_delay)

    set_body(-move_length, 0, move_up)
    sleep(m_delay)
    set_body(0, -move_length, 0)
    sleep(m_delay)
    set_body(move_length, 0, move_up)
    sleep(m_delay)
    set_body(0, move_length, 0)
    sleep(m_delay)

    set_body(move_length, 0, move_up)
    sleep(m_delay)
    set_body(0, -move_length, 0)
    sleep(m_delay)
    set_body(-move_length, 0, move_up)
    sleep(m_delay)
    set_body(0, move_length, 0)
    sleep(m_delay)
    set_body(0, 0, 0)


'''
    Create body & legs
'''
body_frame = frame()
body = box(frame=body_frame, pos=(0,0,body_z/2), length=body_x, height=body_y, width=body_z, color=color.magenta)

for i in range(0,4):
    coxa[i],femur[i],tibia[i] = create_legs(i)


'''
    main loop
'''
while 1:
    rate(1)

    # init the legs position
    set_legs(0,100,80,42)
    set_legs(1,100,80,42)
    set_legs(2,100,80,42)
    set_legs(3,100,80,42)

    sleep(2)
    sit()
    sleep(3)
    stand()
    sleep(3)

    body_move_test(30,30, 1)
    body_move_test(40,40, 1)
    body_move_test(50,30, 1)
    body_move_test(50,40, 1)

    sleep(3)



    #set_legs(0, x_default - x_offset, y_start + y_step, z_boot)
	#set_legs(1, x_default - x_offset, y_start + y_step, z_boot)
	#set_legs(2, x_default + x_offset, y_start, z_boot)
	#set_legs(3, x_default + x_offset, y_start, z_boot)
    #sleep(2)








        
