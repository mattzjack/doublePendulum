from visual import *
from visual.graph import *
from sys import argv

script, filename = argv

target = open(filename, 'w')
target.truncate()
# target.write("impulse data\n")


def swing(angle1, angle2):
    g = 9.8 # N kg-1

    fixed_tip = box(pos = (0, 0, 0), length = 2, width = 2, height = .5, color = color.red)
    top_mass = sphere(mass = 1, radius = 1, color = color.green)
    bot_mass = sphere(mass = 1, radius = 1, color = color.blue)

    top_mass.pos = vector(10, 0, 0).rotate(angle = angle1, axis = (0, 0, 1))
    # top_mass.pos = vector(0, 1, 0) * 10
    bot_mass.pos = top_mass.pos + vector(10, 0, 0).rotate(angle = angle2, axis = (0, 0, 1))
    # bot_mass.pos = top_mass.pos + vector(1, 0, 0) * 10

    tip_top = helix(const = 9999, len = 10, pos = fixed_tip.pos, radius = .5, thickness = .1, coils = 10, color = color.yellow)
    top_bot = helix(const = 9999, len = 10, radius = .5, thickness = .1, coils = 10, color = color.cyan)

    tip_top.axis = top_mass.pos - fixed_tip.pos

    if tip_top.axis.y < 0:
        angle_top = atan(-tip_top.axis.x / tip_top.axis.y)
    elif tip_top.axis.y >= 0:
        if tip_top.axis.x >= 0:
            angle_top = pi / 2 + atan(tip_top.axis.y / tip_top.axis.x)
        elif tip_top.axis.x < 0:
            tip_top.axis.x < 0
        else:
            print "error: tip_top.axis.x"
    else:
        print "error: tip_top.axis.y"

    top_bot.pos = top_mass.pos
    top_bot.axis = bot_mass.pos - top_mass.pos

    if top_bot.axis.y < 0:
        angle_bot = atan(-top_bot.axis.x / top_bot.axis.y)
    elif top_bot.axis.y >= 0:
        if top_bot.axis.x >= 0:
            angle_bot = pi / 2 + atan(top_bot.axis.y / top_bot.axis.x)
        elif top_bot.axis.x < 0:
            top_bot.axis.x < 0
        else:
            print "error: top_bot.axis.x"
    else:
        print "error: top_bot.axis.y"

    top_mass.trail = curve(color = top_mass.color)
    bot_mass.trail = curve(color = bot_mass.color)

    top_mass.Fg = vector(0, -top_mass.mass * g, 0)
    bot_mass.Fg = vector(0, -bot_mass.mass * g, 0)

    top_mass.Fs_up = -tip_top.const * (mag(tip_top.axis) - tip_top.len) * norm(tip_top.axis)

    bot_mass.Fs = -top_bot.const * (mag(top_bot.axis) - top_bot.len) * norm(top_bot.axis)
    top_mass.Fs_down = top_bot.const * (mag(top_bot.axis) - top_bot.len) * norm(top_bot.axis)

    top_mass.Ftot = top_mass.Fg + top_mass.Fs_up + top_mass.Fs_down
    bot_mass.Ftot = bot_mass.Fg + bot_mass.Fs

    top_mass.velocity = vector(0, 0, 0)
    bot_mass.velocity = vector(0, 0, 0)

    top_mass.momentum = top_mass.mass * top_mass.velocity
    bot_mass.momentum = bot_mass.mass * bot_mass.velocity

    was_left = False
    now_right = False
    above = False
    flipped = False

    timer = 0
    dt = .01

    # target.write("top angle: " + str(angle1) + "; bot angle: " + str(angle2) + "\n")

    while not flipped and timer < 100:
        timer += dt

        top_mass.trail.append(pos = top_mass.pos)
        bot_mass.trail.append(pos = bot_mass.pos)

        top_mass.momentum += top_mass.Ftot * dt
        top_mass.velocity = top_mass.momentum / top_mass.mass
        top_mass.pos += top_mass.velocity * dt

        bot_mass.momentum += bot_mass.Ftot * dt
        bot_mass.velocity = bot_mass.momentum / bot_mass.mass
        bot_mass.pos += bot_mass.velocity * dt

        tip_top.axis = top_mass.pos - fixed_tip.pos

        if tip_top.axis.y < 0:
            angle_top = atan(-tip_top.axis.x / tip_top.axis.y)
        elif tip_top.axis.y >= 0:
            if tip_top.axis.x >= 0:
                angle_top = pi / 2 + atan(tip_top.axis.y / tip_top.axis.x)
            elif tip_top.axis.x < 0:
                tip_top.axis.x < 0
            else:
                print "error: tip_top.axis.x"
        else:
            print "error: tip_top.axis.y"

        # if top_bot.axis.y >= 0:
        #     if top_bot.axis.x < 0:
        #         was_left = True
        #     else:
        #         was_left = False
        # else:
        #     was_left = False

        top_bot.pos = top_mass.pos
        top_bot.axis = bot_mass.pos - top_mass.pos

        # if top_bot.axis.y >= 0:
        #     if top_bot.axis.x >= 0:
        #         now_right = True
        #     else:
        #         now_right = False
        # else:
        #     now_right = False
        #
        # if (was_left and now_right) or (not was_left and not now_right):
        #     flipped = True
        # else:
        #     flipped = False

        if top_bot.axis.y >= 0:
            # above = True
            if angle_bot < 0:
                was_left = True
            else:
                was_left = False
        # else:
        #     above = False

        if top_bot.axis.y < 0:
            angle_bot = atan(-top_bot.axis.x / top_bot.axis.y)
        elif top_bot.axis.y >= 0:
            if top_bot.axis.x >= 0:
                angle_bot = pi / 2 + atan(top_bot.axis.y / top_bot.axis.x)
            elif top_bot.axis.x < 0:
                top_bot.axis.x < 0
            else:
                print "error: top_bot.axis.x"
        else:
            print "error: top_bot.axis.y"

        if top_bot.axis.y >= 0:
            above = True
            if angle_bot < 0:
                now_right = False
            else:
                now_right = True
        else:
            above = False

        if above and ((was_left and now_right) or (not was_left and not now_right)):
            flipped = True
        else:
            flipped = False

        top_mass.Fs_up = -tip_top.const * (mag(tip_top.axis) - tip_top.len) * norm(tip_top.axis)

        bot_mass.Fs = -top_bot.const * (mag(top_bot.axis) - top_bot.len) * norm(top_bot.axis)
        top_mass.Fs_down = top_bot.const * (mag(top_bot.axis) - top_bot.len) * norm(top_bot.axis)

        top_mass.Ftot = top_mass.Fg + top_mass.Fs_up + top_mass.Fs_down
        bot_mass.Ftot = bot_mass.Fg + bot_mass.Fs

        # target.write("top angle: " + str(angle_top) + "; bot angle: " + str(angle_bot) + "\n")

    target.write(str(timer))

theta1_range = 9
theta2_range = 10

for theta1 in range(theta1_range):
    for theta2 in range(theta2_range):
        swing(-radians(theta1), -radians(theta2))
        if theta2 != theta2_range - 1:
            target.write(", ")
        print str(theta1) + ",", theta2
    target.write("\n")

target.close
