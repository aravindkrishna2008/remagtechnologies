from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the image
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
x_max = 31
y_min = -40
y_max = 40


def findBinaryList(number):
    for y in range(height):
        pixel_color = image.getpixel((number, y))  
        if pixel_color < 128: 
            binary_list.append(1)  # Black pixel
            # print(y)
            print(y, height)
            # height of the image is the y value
            # the width is the x value of the graph
            new_x = x_min + (number / width) * (x_max - x_min)
            new_y = y_min + ((height - y) / height) * (y_max - y_min)

            # if (len(points) > 0 and points[-1][1] != (30*(number/width))):
            points.append((new_x, new_y))
        else:
            binary_list.append(0)  # White pixel

    # print(binary_list)

for x in range(width):
    findBinaryList(x)




# print(points)
# convert points to pandas dataframe
df = pd.DataFrame(points)
# points -> tuples


x_values, y_values = zip(*points)
# combine x and y into one data frame
xy_pd_df = pd.DataFrame({'x': x_values, 'y': y_values})
xy_pd_df.head()

# def outlier_treatment(datacolumn):
#  sorted(datacolumn)
#  Q1,Q3 = np.percentile(datacolumn , [25,75])
#  IQR = Q3 - Q1
#  lower_range = Q1 - (1.5 * IQR)
#  upper_range = Q3 + (1.5 * IQR)
#  return lower_range,upper_range


# print(xy_pd_df)
# lowerbound,upperbound = outlier_treatment(xy_pd_df.y)
# xy_pd_df[(xy_pd_df.y < lowerbound) | (xy_pd_df.y > upperbound)]
# xy_pd_df.drop(xy_pd_df[ (xy_pd_df.y > upperbound) | (xy_pd_df.y < lowerbound) ].index , inplace=True)

# Create a scatter plot

plt.scatter(xy_pd_df["x"], xy_pd_df["y"], marker='o', color='b', label='Coordinates',s=2)

# plt.plot(xy_pd_df["x"], xy_pd_df["y"])

# Add labels and a legend


plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.xticks(np.arange(0, 30, 1)) 
plt.yticks(np.arange(-40, 45, 5))
plt.title('Scatter Plot of (X, Y) Coordinates')
plt.legend()

# Display the plot
plt.grid(True)
plt.show()

daily_min_max = {}
interval = 1  # Define the time interval in days
print("running file")

for point in points:
    day = int(point[0] / interval)  # Calculate the day using the interval
    value = point[1]  # Extract the value from the second element of each tuple

    if day not in daily_min_max:
        daily_min_max[day] = {'min': float('inf'), 'max': float('-inf')}  # Initialize min and max values
    
    if value < daily_min_max[day]['min']:
        daily_min_max[day]['min'] = value
    
    if value > daily_min_max[day]['max']:
        daily_min_max[day]['max'] = value

# Print the minimum and maximum values for each day
for day, min_max in sorted(daily_min_max.items()):
    print(f"Interval {day}-{day + 1}: Min = {min_max['min']}, Max = {min_max['max']}")

# Write the minimum and maximum values to the "output.txt" file
with open('output.txt', 'w') as file:
    for day, min_max in sorted(daily_min_max.items()):
        file.write(f'{day} {min_max["min"]} ')

# Print the length of the points list
print(len(points))
print(height, width)


exit()
