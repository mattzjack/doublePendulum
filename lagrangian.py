from visual import *
from visual.graph import *
import math
import csv
################################################


def polar_to_cart_vector3(r, theta):
    #given polar coordinates (local to some origin), this function returns local cartesian coordinates in the form of a vector with 3 elements
    x = r * math.sin(theta)
    y = -1 * r * math.cos(theta)
    return vector(x, y, 0)

def update_masses(top_mass, bot_mass, fixed_tip, g, dt, l_top, l_bot): 
    theta_1 = top_mass.theta        #shorthand
    theta_2 = bot_mass.theta        #shorthand
    d_theta_1 = top_mass.d_theta    #shorthand
    d_theta_2 = bot_mass.d_theta    #shorthand
    mu = 1 + (1.0 * top_mass.mass) / bot_mass.mass #shorthand. Multiplying numerator by 1.0 so that python evaluates the expression as float, not integer, division
    theta_1 = top_mass.theta        #shorthand
    theta_2 = bot_mass.theta        #shorthand
    #the next two lines are a rat's nest
    d2_theta_1 = (g*(math.sin(theta_2)*math.cos(theta_1-theta_2)-mu*math.sin(theta_1))-(l_bot*d_theta_2*d_theta_2+l_top*d_theta_1*d_theta_1*math.cos(theta_1-theta_2))*math.sin(theta_1-theta_2))/(1.0*l_top*(mu-math.cos(theta_1-theta_2)*math.cos(theta_1-theta_2)));
    d2_theta_2 = (mu*g*(math.sin(theta_1)*math.cos(theta_1-theta_2)-math.sin(theta_2))+(mu*l_top*d_theta_1*d_theta_1+l_bot*d_theta_2*d_theta_2*math.cos(theta_1-theta_2))*math.sin(theta_1-theta_2))/(1.0*l_bot*(mu-math.cos(theta_1-theta_2)*math.cos(theta_1-theta_2)));

    top_mass.d_theta += d2_theta_1*dt;
    bot_mass.d_theta += d2_theta_2*dt;
    
    top_mass.theta = top_mass.theta + top_mass.d_theta*dt
    bot_mass.theta = bot_mass.theta + bot_mass.d_theta*dt

    top_mass.pos = (fixed_tip.pos + polar_to_cart_vector3(l_top, top_mass.theta))
    bot_mass.pos = (top_mass.pos + polar_to_cart_vector3(l_bot, bot_mass.theta))



#Python Lesson: This run() function can be called using keyword arguments.
#To call run(), you have the option of specifying certain arguments like this: run(arg_name=arg_value).
#If you don't specify any arguments to the function, it'll just assume some default arguments and happily run.
#It's the exact same syntax you would use to initialize a Vpython object - can initialize a sphere with sphere(), sphere(radius=1, mass=1), sphere(mass=1, pos=(0,0,0), radius=1), etc.
def run(dt = 0.01, max_time=10000, top_mass_theta_arg=math.pi/2, bot_mass_theta_arg=0, l_top=10, l_bot=10, top_mass_d_theta_arg=0, bot_mass_d_theta_arg=0):
    #"top_mass_theta_arg" and "top_mass_d_theta_arg" are TERRIBLE variable names, but at least they're consistent.
    g = 9.8
    timer = 0
    #initialize the fixed pivot of the pendulum
    fixed_tip = box(pos = (0, 0, 0), length = 2, width = 2, height = .5, color = color.red)    
    #initialize the top mass
    top_mass = sphere(mass = 1, radius = 1, color = color.green)    #(note that we haven't declared the position yet)
    top_mass.trail = curve(color = top_mass.color)
    #initialize the bottom mass
    bot_mass = sphere(mass = 1, radius = 1, color = color.blue)     #(note that we haven't declared the position yet)
    bot_mass.trail = curve(color = bot_mass.color)
    #initialize angles
    top_mass.theta = top_mass_theta_arg     #angle swept out by upper rod against vertical line
    bot_mass.theta = bot_mass_theta_arg  #angle swept out by lower rod against vertical line
    #here, we finally get the positions of bot_mass and top_mass in cartesian coordinates
    top_mass.pos = fixed_tip.pos + polar_to_cart_vector3(l_top, top_mass.theta)
    bot_mass.pos = top_mass.pos + polar_to_cart_vector3(l_bot, bot_mass.theta)
    top_mass.d_theta = top_mass_d_theta_arg     #time derivative of theta_1
    bot_mass.d_theta = bot_mass_d_theta_arg     #time derivative of theta_2
    
    prev_bot_theta = bot_mass.theta
    
    while (timer < max_time and not flipped(prev_bot_theta, bot_mass.theta)): #if we're measuring the time for something else to happen, simply replace the call to flipped() with some other check.
        #rate(100) #comment out this line if you dgaf about the animation - it'll run much faster.
        timer += dt

        #update bot_mass and top_mass
        prev_bot_theta = bot_mass.theta
        update_masses(top_mass, bot_mass, fixed_tip, g, dt, l_top, l_bot)
        #draw - might waste memory when running tons of sims
        #top_mass.trail.append(pos = top_mass.pos)
        #bot_mass.trail.append(pos = bot_mass.pos)
    print "completed one simulation"
    #return some results of the simulation that we're interested in.
    return timer

def flipped(prev_theta, curr_theta):
    prev_theta = prev_theta % (2 * math.pi)
    curr_theta = curr_theta % (2*math.pi)
    if 3*math.pi/2 > prev_theta > math.pi/2 and 3*math.pi/2 > curr_theta > math.pi/2: #this is a liiiiittle hack-y, but boy is it less hacky than what we used to have!
        if ((prev_theta < math.pi and curr_theta > math.pi) or (prev_theta > math.pi and curr_theta < math.pi)):
            print prev_theta, curr_theta
            return true
    return false


def repeat():
    #use this function if you want to iterate over initial conditions
    degree_increment = 1   #Decreasing this increment value means we have to really sit around for a while in order to get the data.

    with open('lagrangian_data.csv', 'wb') as f:
        writer = csv.writer(f)
        for top_angle_degrees in xrange(0,180,degree_increment):    #Python Lesson: Syntax for xrange() is xrange(begin, end, step). It returns a list that you can iterate over in a for loop.
            row_results = []
            for bot_angle_degrees in xrange(0,180, degree_increment):
                top_angle_rad = top_angle_degrees * math.pi / 180
                bot_angle_rad = bot_angle_degrees * math.pi / 180
                row_results.append(run( top_mass_theta_arg=top_angle_rad, bot_mass_theta_arg=bot_angle_rad))
            writer.writerow(row_results)
    print "all done FOR REAL"

repeat()
#run(dt=0.05, max_time=10)
#run(dt=0.05, max_time=100, top_mass_theta_arg=math.pi/2+0.5, bot_mass_theta_arg=math.pi-0.5)
