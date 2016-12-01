from visual import *
from visual.graph import *
import math

################################################


def polar_to_cart_vector3(r, theta):
    #given polar coordinates (local to some origin), this function returns local cartesian coordinates in the form of a vector with 3 elements
    x = r * math.sin(theta)
    y = -1 * r * math.cos(theta)
    return vector(y, x, 0) #or should it be some other ordering of x, y, and 0

def update_masses(top_mass, bot_mass, fixed_tip, g, dt, l_top, l_bot, d_theta_1, d_theta_2):
    theta_1 = top_mass.theta
    theta_2 = bot_mass.theta
    mu = 1 + top_mass.mass / bot_mass.mass #shorthand
    #this thing is quite the rat's nest. God I hope it works.
##    d2_theta_1 = (g*(math.sin(theta_2)*math.cos(theta_1-theta_2)-mu*math.sin(theta_1))-(l_bot*d_theta_2*d_theta_2+l_top*d_theta_1*d_theta_1*math.cos(theta_1-theta_2))*math.sin(theta_1-theta_2))/(l_top*(mu-math.cos(theta_1-theta_2)*math.cos(theta_1-theta_2)));
##    d2_theta_2 = (mu*g*(math.sin(theta_1)*math.cos(theta_1-theta_2)-math.sin(theta_2))+(mu*l_top*d_theta_1*d_theta_1+l_bot*d_theta_2*d_theta_2*math.cos(theta_1-theta_2))*math.sin(theta_1-theta_2))/(l_bot*(mu-math.cos(theta_1-theta_2)*math.cos(theta_1-theta_2)));

    Theta1 = top_mass.theta
    Theta2 = bot_mass.theta
    dTheta1 = d_theta_1
    dTheta2 = d_theta_2
    l1 = l_top
    l2 = l_bot
    d2Theta1  =  (g*(math.sin(Theta2)*math.cos(Theta1-Theta2)-mu*math.sin(Theta1))-(l2*dTheta2*dTheta2+l1*dTheta1*dTheta1*math.cos(Theta1-Theta2))*math.sin(Theta1-Theta2))/(l1*(mu-math.cos(Theta1-Theta2)*math.cos(Theta1-Theta2)));
    d2_theta_1 = d2Theta1
    d2Theta2  =  (mu*g*(math.sin(Theta1)*math.cos(Theta1-Theta2)-math.sin(Theta2))+(mu*l1*dTheta1*dTheta1+l2*dTheta2*dTheta2*math.cos(Theta1-Theta2))*math.sin(Theta1-Theta2))/(l2*(mu-math.cos(Theta1-Theta2)*math.cos(Theta1-Theta2)));
    d2_theta_2 = d2Theta2

##    numer = g * (math.sin(theta_2) * math.sin(theta_1 - theta_2) - mu * math.sin(theta_1)
##    numer -= math.sin(theta_1 - theta_2) * (l_bot * d_theta_2**2 + l_top * d_theta_1**2

    d_theta_1 += d2_theta_1*dt;
    d_theta_2 += d2_theta_2*dt;
    
    #print ["theta_1", top_mass.theta]
    #print fixed_tip.pos + polar_to_cart_vector3(l_top, theta_1)
    top_mass.theta += d_theta_1*dt;
    bot_mass.theta += d_theta_2*dt;

    #print ["theta_1", top_mass.theta]
    #print fixed_tip.pos + polar_to_cart_vector3(l_top, theta_1)
    top_mass.pos = (fixed_tip.pos + polar_to_cart_vector3(l_top, top_mass.theta))
    bot_mass.pos = (top_mass.pos + polar_to_cart_vector3(l_bot, bot_mass.theta))


def run(iteration):
    g = 9.8
    timer = 0
    dt = 0.01
    timer = 0
    max_time = 20
    #initialize the fixed pivot of the pendulum
    fixed_tip = box(pos = (0, 0, 0), length = 2, width = 2, height = .5, color = color.red)    
    #initialize the top mass
    top_mass = sphere(mass = 1, radius = 1, color = color.green)    #(note that we haven't declared the position yet)
    top_mass.trail = curve(color = top_mass.color)
    #initialize the bottom mass
    bot_mass = sphere(mass = 1, radius = 1, color = color.blue)     #(note that we haven't declared the position yet)
    bot_mass.trail = curve(color = bot_mass.color)
    #initialize the massless rods, upper_rod and lower_rod
    l_top = 10
    l_bot = 10
    #initialize angles
    top_mass.theta = math.pi/4     #angle swept out by upper rod against vertical line
    bot_mass.theta = -1*math.pi/4  #angle swept out by lower rod against vertical line
    #here, we finally get the positions of bot_mass and top_mass in cartesian coordinates
    top_mass.pos = fixed_tip.pos + polar_to_cart_vector3(l_top, top_mass.theta)
    bot_mass.pos = top_mass.pos + polar_to_cart_vector3(l_bot, bot_mass.theta)
    d_theta_1 = -1   #time derivative of theta_1
    d_theta_2 = 0   #time derivative of theta_2
    
    #################
    #if you want to update the initial conditions over multiple iterations,
    #that would best be done right here.
    #simply update the initial conditions as a function of the iteration.
    #################

    while (timer < max_time):
        rate(100) #remove this line if you dgaf about the animation 
        timer += dt

        #update bot_mass and top_mass
        #print ["top_mass.pos before call", top_mass.pos]
        update_masses(top_mass, bot_mass, fixed_tip, g, dt, l_top, l_bot, d_theta_1, d_theta_2)
        #print ["top_mass.pos after call ", top_mass.pos]
        #draw
        top_mass.trail.append(pos = top_mass.pos)
        bot_mass.trail.append(pos = bot_mass.pos)
        #print "\n"
    print "all done"
    print "started from the bottom now we here"


def repeat():
    #use this function if you want to iterate over initial conditions
    iteration = 0
    max_iters = 0
    while iteration < max_iters:
        #do your fiddling with initial conditions here
        run(iteration)
    print "all done FOR REAL"

##def reset():
##    #Should only call this function when everything's ALREADY been declared.
##    g = 9.8
##    timer = 0
##    dt = 0.01
##    timer = max_time
##
##    #initialize the fixed pivot of the pendulum
##    fixed_tip = box(pos = (0, 0, 0), length = 2, width = 2, height = .5, color = color.red)    
##
##    #initialize the top mass
##    top_mass = sphere(mass = 1, radius = 1, color = color.green)
##    top_mass.pos = vector(0, -10, 0)
##    top_mass.trail = curve(color = top_mass.color)
##
##    #initialize the bottom mass
##    bot_mass = sphere(mass = 1, radius = 1, color = color.blue)
##    bot_mass.pos = top_mass.pos + vector(0, -10, 0)
##    bot_mass.trail = curve(color = bot_mass.color)
##
##    #initialize the massless rods, upper_rod and lower_rod
##    #upper_rod =
##    #lower_rod =
##    l_top = mag(top_mass.pos - fixed_tip.pos)
##    l_bot = mag(bot_mass.pos - top_mass.pos)
##
##    #CALCULATE IT FROM THE POS'S OF BOT_MASS AND TOP_MASS YA DUM DUM
##    #theta_1 = math.pi/4     #angle swept out by upper rod against vertical line
##    #theta_2 = -1*math.pi/4  #angle swept out by lower rod against vertical line
##
##    d_theta_1 = 0   #time derivative of theta_1
##    d_theta_2 = 0   #time derivative of theta_2
##    

run(0)
