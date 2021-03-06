from visual import *
from visual.graph import *
from sys import argv

# try:
script, filename = argv

target = open(filename, 'w')
target.truncate()
# except:
#     pass


def swing(angle1, angle2):
    g = 9.8 # N kg-1

    fixed_tip = box(pos = (0, 0, 0), length = 2, width = 2, height = .5, color = color.red)
    top_mass = sphere(mass = 1, radius = 1, color = color.green)
    bot_mass = sphere(mass = 1, radius = 1, color = color.blue)

    top_mass.pos = vector(10, 0, 0).rotate(angle = angle1, axis = (0, 0, 1))
    bot_mass.pos = top_mass.pos + vector(10, 0, 0).rotate(angle = angle2, axis = (0, 0, 1))

    tip_top = helix(const = 9999, len = 10, pos = fixed_tip.pos, radius = .5, thickness = .1, coils = 10, color = color.yellow)
    top_bot = helix(const = 9999, len = 10, radius = .5, thickness = .1, coils = 10, color = color.cyan)

    tip_top.axis = top_mass.pos - fixed_tip.pos

    top_bot.pos = top_mass.pos
    top_bot.axis = bot_mass.pos - top_mass.pos

    # top_mass.trail = curve(color = top_mass.color)
    # bot_mass.trail = curve(color = bot_mass.color)

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
    was_right = False
    now_left = False
    now_right = False
    above = False
    flipped = False

    timer = 0
    dt = .01

    if tip_top.axis.y < 0:
             angle_top = atan(-tip_top.axis.x / tip_top.axis.y)
    else:
        if tip_top.axis.x >= 0:
            angle_top = pi / 2 + atan(tip_top.axis.y / tip_top.axis.x)
        else:
            tip_top.axis.x < 0

    if top_bot.axis.y < 0:
        angle_bot = atan(-top_bot.axis.x / top_bot.axis.y)
    else:
        if top_bot.axis.x >= 0:
            angle_bot = pi / 2 + atan(top_bot.axis.y / top_bot.axis.x)
        else:
            top_bot.axis.x < 0

    angle_top_old = angle_top
    angle_bot_old = angle_bot

    dangle_top = angle_top - angle_top_old
    dangle_bot = angle_bot - angle_bot_old

    # while not flipped and timer < 500:
    while timer < 10000:
        # rate(200)
        # top_mass.trail.append(pos = top_mass.pos)
        # bot_mass.trail.append(pos = bot_mass.pos)

        top_mass.momentum += top_mass.Ftot * dt
        top_mass.velocity = top_mass.momentum / top_mass.mass
        top_mass.pos += top_mass.velocity * dt

        bot_mass.momentum += bot_mass.Ftot * dt
        bot_mass.velocity = bot_mass.momentum / bot_mass.mass
        bot_mass.pos += bot_mass.velocity * dt

        tip_top.axis = top_mass.pos - fixed_tip.pos

        # angle_top_old = angle_top
        #
        # if tip_top.axis.y < 0:
        #          angle_top = atan(-tip_top.axis.x / tip_top.axis.y)
        # else:
        #     if tip_top.axis.x >= 0:
        #         angle_top = pi / 2 + atan(tip_top.axis.y / tip_top.axis.x)
        #     else:
        #         tip_top.axis.x < 0
        #
        # dangle_top = angle_top - angle_top_old

        was_left = False
        was_right = False
        now_left = False
        now_right = False
        above = False
        flipped = False

        if top_bot.axis.x < 0:
            was_left = True
            was_right = False
        else:
            was_left = False
            was_right = True

        top_bot.pos = top_mass.pos
        top_bot.axis = bot_mass.pos - top_mass.pos

        if top_bot.axis.y > 0:
            above = True
            if top_bot.axis.x < 0:
                now_left = True
                now_right = False
            else:
                now_left = False
                now_right = True
        else:
            above = False

        if above and ((was_left and now_right) or (was_right and now_left)):
            flipped = True
        else:
            flipped = False

        # angle_bot_old = angle_bot
        #
        # if top_bot.axis.y < 0:
        #     angle_bot = atan(-top_bot.axis.x / top_bot.axis.y)
        # else:
        #     if top_bot.axis.x >= 0:
        #         angle_bot = pi / 2 + atan(top_bot.axis.y / top_bot.axis.x)
        #     else:
        #         top_bot.axis.x < 0
        #
        # dangle_bot = angle_bot - angle_bot_old

        top_mass.Fs_up = -tip_top.const * (mag(tip_top.axis) - tip_top.len) * norm(tip_top.axis)

        bot_mass.Fs = -top_bot.const * (mag(top_bot.axis) - top_bot.len) * norm(top_bot.axis)
        top_mass.Fs_down = top_bot.const * (mag(top_bot.axis) - top_bot.len) * norm(top_bot.axis)

        top_mass.Ftot = top_mass.Fg + top_mass.Fs_up + top_mass.Fs_down
        bot_mass.Ftot = bot_mass.Fg + bot_mass.Fs

        # print dangle_top * 180 / pi, dangle_bot * 180 / pi

        timer += dt

    target.write(str(timer))

    # try:
    #     target.write(str(timer))
    # except:
    #     pass

theta1_first = 120
theta1_last = 125

theta2_first = 90
theta2_last = 95

theta1_range = range(theta1_first, theta1_last, 5)
theta2_range = range(theta2_first, theta2_last, 5)

for theta1 in theta1_range:
    for theta2 in theta2_range:
        print "%r, %r" % (theta1, theta2)
        swing(-radians(90 - theta1), -radians(90 - theta2))
        if theta2 != theta2_range[-1]:
            # try:
            target.write(", ")
            # except:
            #     pass
    # try:
    target.write("\n")
    # except:
    #     pass

# try:
target.close()
#     print "closed."
# except:
#     pass

print "done."
