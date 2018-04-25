import numpy as np

# Part 1
# background (non-associated) mortality rate
a = -np.log(1 - (((18*100) - 36.2) / 100000))
# stroke-associated mortality rate
b = -np.log(1-(36.2 / 100000))

# Part 2
# rate of first-ever stroke event
c = -np.log(1-(15/1000))

# Part 3
# rate transition from stroke to post-stroke
d = 0.9 * c
# rate transition from stroke to death
e = 0.1 * c

# Part 4
# annual rate of recurrent stroke
f = (-np.log(0.83)) * 0.17 / ((1 - 0.83) * 5)

# Part 5
# rate transition from post-stroke to stroke
g = 0.8 * f
# rate transition from post-stroke to death
h = 0.2 * f

# Part 6
# rate transition from stroke to post-stroke
i = 1 / (1/52)

print(a, b, c, d, e, f, g, h, i)
