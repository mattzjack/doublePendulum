from visual import *
from visual.graph import *

def swing():
    g = 9.8 # N kg-1

    fixed_tip = box(pos = (0, 0, 0), length = 2, width = 2, height = .5, color = color.red)
    top_mass = sphere(mass = 1, radius = 1, color = color.green)
    bot_mass = sphere(mass = 1, radius = 1, color = color.blue)

    top_mass.pos = vector(0, -10, 0)
    bot_mass.pos = vector(0, -20, 0)

    tip_top = helix(const = 10, len = 10, pos = fixed_tip.pos, radius = .5, thickness = .1, coils = 10, color = color.yellow)
    top_bot = helix(const = 10, len = 10, radius = .5, thickness = .1, coils = 10, color = color.cyan)

    tip_top.axis = top_mass.pos - fixed_tip.pos

    top_bot.pos = top_mass.pos
    top_bot.axis = bot_mass.pos - top_mass.pos

    top_mass.trail = curve(color = top_mass.color)
    bot_mass.trail = curve(color = bot_mass.color)

    top_mass.Fg = vector(0, -top_mass.mass * g, 0)
    bot_mass.Fg = vector(0, -bot_mass.mass * g, 0)

    top_mass.displacement = fixed_tip.pos - top_mass.pos
    top_mass.Fs_up = tip_top.const * (mag(top_mass.displacement) - tip_top.len) * norm(top_mass.displacement)

    bot_mass.displacement = top_mass.pos - bot_mass.pos
    bot_mass.Fs = top_bot.const * (mag(bot_mass.displacement) - top_bot.len) * norm(top_mass.displacement)
    top_mass.Fs_down = -top_bot.const * (mag(bot_mass.displacement) - top_bot.len) * norm(top_mass.displacement)

    top_mass.Ftot = top_mass.Fg + top_mass.Fs_up + top_mass.Fs_down
    bot_mass.Ftot = bot_mass.Fg + bot_mass.Fs

    top_mass.velocity = vector(0, 0, 0)
    bot_mass.velocity = vector(0, 0, 0)

    top_mass.momentum = top_mass.mass * top_mass.velocity
    bot_mass.momentum = bot_mass.mass * bot_mass.velocity

    timer = 0
    dt = .01

    while timer < 60:
        rate(100)
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

        top_bot.pos = top_mass.pos
        top_bot.axis = bot_mass.pos - top_mass.pos

        top_mass.displacement = fixed_tip.pos - top_mass.pos
        top_mass.Fs_up = tip_top.const * (mag(top_mass.displacement) - tip_top.len) * norm(top_mass.displacement)

        bot_mass.displacement = top_mass.pos - bot_mass.pos
        bot_mass.Fs = top_bot.const * (mag(bot_mass.displacement) - top_bot.len) * norm(top_mass.displacement)
        top_mass.Fs_down = -top_bot.const * (mag(bot_mass.displacement) - top_bot.len) * norm(top_mass.displacement)

        top_mass.Ftot = top_mass.Fg + top_mass.Fs_up + top_mass.Fs_down
        bot_mass.Ftot = bot_mass.Fg + bot_mass.Fs
swing()
