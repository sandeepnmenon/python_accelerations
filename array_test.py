import random
import time

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

