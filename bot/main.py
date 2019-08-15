import math
import threading

from movement import motor_controls as mc
from usdar.usdar import detection as dt
from usdar.usdar import ultrasonic as us
from usdar.usdar import stepper as st


def get_angle_to_turn():
    env_map = dt.scan_360()
    distances = [(x, y, math.sqrt(x*x+y*y)) for x, y in env_map]
    max_dist = distances[[i[2]
                          for i in distances].index(
        max([i[2] for i in distances]))]
    return math.degrees(math.atan2(max_dist[0], max_dist[1]))


def reset_us_stepper(ticks_to_reset):
    st.run_stepper(ticks_to_reset, False)


if __name__ == "__main__":
    while True:
        angle_to_turn = get_angle_to_turn()
        t = threading.Thread(target=reset_us_stepper)
        t.start()
        if angle_to_turn < 0:
            angle_to_turn = 360 + angle_to_turn
        print('The most space seems to be at:', angle_to_turn, '°.')
        mc.turn_degree(angle_to_turn)
        front_dist = us.get_distance()
        print('In front of me there is', front_dist, 'cm space.')
        if front_dist > 20:
            mc.move_front()
            while front_dist > 20:
                front_dist = us.get_distance()
        mc.stop_motors()
