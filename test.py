import time

from Clogic.Clogic import normal_distribution, calculate


start = time.time()

for i in range(1000):
    calculate(0.006, 0.055, 0.026, 0.012)

print(f"Time: {time.time() - start}")