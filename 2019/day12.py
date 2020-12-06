import copy
from math import gcd

from utils.Int3Point import Int3Point


def calculate_velocity(moons: [Int3Point], velocities: [Int3Point]):
    for i, moon_1 in enumerate(moons):
        for j, moon_2 in enumerate(moons):
            if moon_1.x > moon_2.x:
                velocities[i].x -= 1
                velocities[j].x += 1
            if moon_1.y > moon_2.y:
                velocities[i].y -= 1
                velocities[j].y += 1
            if moon_1.z > moon_2.z:
                velocities[i].z -= 1
                velocities[j].z += 1
    return velocities


def calculate_energy(moons: [Int3Point], velocities: [Int3Point]):
    total_energy = 0
    for i, moon in enumerate(moons):
        moons[i] = moon + velocities[i]
        pot = abs(moons[i].x) + abs(moons[i].y) + abs(moons[i].z)
        kin = abs(velocities[i].x) + abs(velocities[i].y) + abs(velocities[i].z)
        total_energy += (pot * kin)
    return moons, total_energy


def calculate_energy_after_x_steps(moons: [Int3Point], steps):
    velocities = [Int3Point(0, 0, 0) for i in range(4)]
    for i in range(0, steps + 1):
        moon_with_energy = calculate_energy(moons, velocities)
        moons = moon_with_energy[0]
        velocities = calculate_velocity(moons, velocities)
        total_energy = moon_with_energy[1]
    return total_energy


def steps_to_initial_state(moons: [Int3Point]):
    steps = 1
    velocities = [Int3Point(0, 0, 0) for i in range(4)]
    initial_state = copy.deepcopy(moons)
    moon_with_energy = calculate_energy(moons, velocities)
    moons = moon_with_energy[0]
    velocities = calculate_velocity(moons, velocities)
    x = 0
    y = 0
    z = 0
    while x == 0 or y == 0 or z == 0:
        moon_with_energy = calculate_energy(moons, velocities)
        moons = moon_with_energy[0]
        if check_x(initial_state, moons) and x == 0:
            x = steps + 1
        if check_y(initial_state, moons) and y == 0:
            y = steps + 1
        if check_z(initial_state, moons) and z == 0:
            z = steps + 1

        velocities = calculate_velocity(moons, velocities)
        steps += 1

    return nww([x, y, z])


def nww(numbers):
    lcm = numbers[0]
    for i in numbers[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def check_x(init_state: [Int3Point], moons: [Int3Point]):
    return init_state[0].x == moons[0].x and init_state[1].x == moons[1].x and init_state[2].x == moons[2].x and \
           init_state[3].x == moons[3].x


def check_y(init_state: [Int3Point], moons: [Int3Point]):
    return init_state[0].y == moons[0].y and init_state[1].y == moons[1].y and init_state[2].y == moons[2].y and \
           init_state[3].y == moons[3].y


def check_z(init_state: [Int3Point], moons: [Int3Point]):
    return init_state[0].z == moons[0].z and init_state[1].z == moons[1].z and init_state[2].z == moons[2].z and \
           init_state[3].z == moons[3].z


# part 1
assert 179 == calculate_energy_after_x_steps(
    [Int3Point(-1, 0, 2), Int3Point(2, -10, -7), Int3Point(4, -8, 8), Int3Point(3, 5, -1)], 10)
assert 1940 == calculate_energy_after_x_steps(
    [Int3Point(-8, -10, 0), Int3Point(5, 5, 10), Int3Point(2, -7, 3), Int3Point(9, -8, -3)], 100)
# solution
# <x=1, y=3, z=-11>
# <x=17, y=-10, z=-8>
# <x=-1, y=-15, z=2>
# <x=12, y=-4, z=-4>
assert 8310 == calculate_energy_after_x_steps(
    [Int3Point(1, 3, -11), Int3Point(17, -10, -8), Int3Point(-1, -15, 2), Int3Point(12, -4, -4)], 1000)

# part 2
assert 2772 == nww([18, 28, 44])
assert 2772 == steps_to_initial_state(
    [Int3Point(-1, 0, 2), Int3Point(2, -10, -7), Int3Point(4, -8, 8), Int3Point(3, 5, -1)])
assert 4686774924 == steps_to_initial_state(
    [Int3Point(-8, -10, 0), Int3Point(5, 5, 10), Int3Point(2, -7, 3), Int3Point(9, -8, -3)])
assert 319290382980408 == steps_to_initial_state(
    [Int3Point(1, 3, -11), Int3Point(17, -10, -8), Int3Point(-1, -15, 2), Int3Point(12, -4, -4)])
