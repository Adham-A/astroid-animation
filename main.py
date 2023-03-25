import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

RADIUS_INNER_CIRCLE = 1
RADIUS_BIG_CIRCLE = RADIUS_INNER_CIRCLE*4
RADIUS_SMALL_CIRCLE = RADIUS_BIG_CIRCLE-RADIUS_INNER_CIRCLE

# Red dot rotates 3pi/2 when circles rotates pi/2
FRAME_COUNT_GOAL = 1500
SPIN_FRAME_COUNT = FRAME_COUNT_GOAL//3


def main():
    """Generates the animation
    """

    fig = plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')

    values = np.linspace(0, np.pi*2, num=FRAME_COUNT_GOAL)
    values_length = len(values)

    circle_x = np.cos(values)
    circle_y = np.sin(values)

    small_circle = (circle_x * RADIUS_SMALL_CIRCLE,
                    circle_y * RADIUS_SMALL_CIRCLE)

    big_circle = (circle_x * RADIUS_BIG_CIRCLE,
                  circle_y * RADIUS_BIG_CIRCLE)

    # Plots big circle
    plt.plot(big_circle[0], big_circle[1], color="red")

    # Small circle
    line, = plt.plot(0, 0, scalex=1, scaley=1)

    red_dot, = plt.plot([], [], marker="o", markersize=10,
                        markeredgecolor="red", markerfacecolor="red")

    spin_values = np.linspace(0, np.pi*2, num=SPIN_FRAME_COUNT)
    spin_x = np.cos(spin_values)
    spin_y = -np.sin(spin_values)

    previous_red_dot_x = []
    previous_red_dot_y = []

    # Green line astroid
    line2, = plt.plot(0, 0, color="green")

    def update(frame):

        spin_index = int(np.mod(frame, SPIN_FRAME_COUNT))
        x_dot = spin_x[spin_index]
        y_dot = spin_y[spin_index]

        circle_rotate_index = int(np.mod(frame, values_length))

        cirlce_x_offset = small_circle[0][circle_rotate_index]

        cirlce_y_offset = small_circle[1][circle_rotate_index]

        red_dot_x = x_dot * RADIUS_INNER_CIRCLE + cirlce_x_offset
        red_dot_y = y_dot * RADIUS_INNER_CIRCLE + cirlce_y_offset

        # Set the data
        red_dot.set_xdata(red_dot_x)
        red_dot.set_ydata(red_dot_y)

        line.set_xdata(circle_x * RADIUS_INNER_CIRCLE + cirlce_x_offset)
        line.set_ydata(circle_y * RADIUS_INNER_CIRCLE + cirlce_y_offset)

        previous_red_dot_x.append(red_dot_x)
        previous_red_dot_y.append(red_dot_y)

        # Draw the astroid
        line2.set_xdata(previous_red_dot_x)
        line2.set_ydata(previous_red_dot_y)

    ani = animation.FuncAnimation(fig, update, frames=range(FRAME_COUNT_GOAL),
                                  interval=10, blit=False)

    writer = animation.FFMpegWriter(
        fps=60, metadata=dict(artist='Me'), bitrate=4000)
    ani.save(f"animation_sin_{time.time_ns()}.mp4", writer=writer)


main()
