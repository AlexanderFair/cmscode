from display import Display
import random
from time import sleep
PLOTSIZE = 8000
# here are some functions to implement:
# down below is where you'll call them

# 2d cross product:
# returns 0 if there is a line passing through all of p1, p2, p3
# otherwise returns a value > 0 if the shortest angle from p2 to p3 about point p1 is counter clockwise
# and returns a value < 0 if the shortest angle is clockwise
def cross(p1, p2, p3):
    pass

# determine if the line segments defined by [p1, p2]
# and [q1, q2] intersect 
def intersect(p1, p2, q1, q2):
    pass

# check if any 3 points in points are collinear
# i.e. is there an infinite line passing through 
# at least three of the given points
def any_colinear(points):
    pass

# does the naive uncrossing algorithm.
# we will consider the i-th element of blue_pts
# to be paired with the i-th element of red_pts
def uncross(blue_pts, red_pts):
    pass

# generates n random points, and has them not be colinear
# ( you will want to use random.randint() )
def gen_rnd_points(n):
    pass

# heres where your main code should go:

# When you're ready to display the points, uncomment this line,
# display = Display()

# and then you can insert these lines where you want them (which
# will probably be after each time you uncross two lines):
# display.draw_points(points)  
# display.draw_points(blue_pts, red_pts)
# display.draw_pairing(blue_pts, red_pts)

# and you will want to add a sleep call ( sleep(num_seconds) )
# at the end of your program. this will pause execution of your program, 
# stopping it from closing the window as soon as you solve the problem.
# Note: you don't need to do a sleep call each time you draw points,
# that is already built in. Only need to do it at the very end. 