from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

img = Image.open('graph-1.png')

# Convert the image to RGB colorspace
img.convert('L').point(lambda x : 255 if x > 50 else 0, mode="1").save("graph.png")

image_path = 'graph.png' 
image = Image.open(image_path)

image = image.convert('L')

width, height = image.size

binary_list = []

points = []

x_min = 0
x_max = 30
y_min = -40
y_max = 40


def findBinaryList(number):
    for y in range(height):
        pixel_color = image.getpixel((number, y))  
        if pixel_color < 128: 
            binary_list.append(1)  # Black pixel
            # height of the image is the y value
            # the width is the x value of the graph
            new_x = x_min + (number / width) * (x_max - x_min)
            new_y = y_min + ((height - y) / height) * (y_max - y_min)

            points.append((new_x, new_y))
        else:
            binary_list.append(0)  # White pixel

for x in range(width):
    findBinaryList(x)


df = pd.DataFrame(points)
# points -> tuples

x_values, y_values = zip(*points)

# combine x and y into one data frame
xy_pd_df = pd.DataFrame({'x': x_values, 'y': y_values})
xy_pd_df.head()

daily_data = {}  # dictionary to store daily data (sum, min, max, count)
                 # acts as input for output.txt/cpp code
interval = 1

for point in points:
    day = int(point[0] / interval)  # calculate the day using the interval
    value = point[1]  

    if day not in daily_data:
        daily_data[day] = {'sum': 0, 'min': float('inf'), 'max': float('-inf'), 'count': 0}  # Initialize sum, min, max, and count
    
    daily_data[day]['sum'] += value  # accumulate the sum of values
    daily_data[day]['count'] += 1  # increment the count of values
    daily_data[day]['min'] = min(daily_data[day]['min'], value)  # update the minimum value
    daily_data[day]['max'] = max(daily_data[day]['max'], value)  # update the maximum value

# Print the min, max, and average values for each day and write them to the "output.txt" file
with open('output.txt', 'w') as file:
    file.write(f'30 ')
    for day, data in sorted(daily_data.items()):
        avg = data['sum'] / data['count']
        min_val = data['min']
        max_val = data['max']
        file.write(f'{day} {min_val} {max_val} ')

print(len(points))