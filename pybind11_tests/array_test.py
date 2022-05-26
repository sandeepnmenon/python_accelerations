import random
import time
import sys

# Add parent directory path in import
sys.path.append('../')
from build.py_vector import get_array_sum

# Initialize an array with random numbers
list_len = 100000
array = [random.randint(0, 100) for i in range(list_len)]

# Calculate sum of all elements in the array using python for loop and time taken
start = time.time()
sum = 0
for i in range(list_len):
    sum += array[i]
end = time.time()
print("Sum of all elements in the array using python for loop:", sum)
print("Time taken:", end - start)

# Calculate sum of all elements in the array using C++ function using pybind11
start = time.time()
sum = get_array_sum(array)
end = time.time()
print("Sum of all elements in the array using C++ function:", sum)
print("Time taken:", end - start)
