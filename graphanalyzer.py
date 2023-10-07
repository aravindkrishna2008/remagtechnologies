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

def findBinaryList(number):
    for y in range(height):
        pixel_color = image.getpixel((number, y))  
        if pixel_color < 128: 
            binary_list.append(1)  # Black pixel
            print(y)
            # if (len(points) > 0 and points[-1][1] != (30*(number/width))):
            points.append((31*(number/width), 160*(-y/height)+160))
        else:
            binary_list.append(0)  # White pixel

    # print(binary_list)

for x in range(width):
    findBinaryList(x)

print(points)
# convert points to pandas dataframe
df = pd.DataFrame(points)
# points -> tuples


x_values, y_values = zip(*points)
# combine x and y into one data frame
xy_pd_df = pd.DataFrame({'x': x_values, 'y': y_values})
xy_pd_df.head()

def outlier_treatment(datacolumn):
 sorted(datacolumn)
 Q1,Q3 = np.percentile(datacolumn , [25,75])
 IQR = Q3 - Q1
 lower_range = Q1 - (1.5 * IQR)
 upper_range = Q3 + (1.5 * IQR)
 return lower_range,upper_range


print(xy_pd_df)
lowerbound,upperbound = outlier_treatment(xy_pd_df.y)
xy_pd_df[(xy_pd_df.y < lowerbound) | (xy_pd_df.y > upperbound)]
xy_pd_df.drop(xy_pd_df[ (xy_pd_df.y > upperbound) | (xy_pd_df.y < lowerbound) ].index , inplace=True)

# Create a scatter plot

# plt.scatter(xy_pd_df["x"], xy_pd_df["y"], marker='o', color='b', label='Coordinates',s=2)

# plt.plot(xy_pd_df["x"], xy_pd_df["y"])

# Add labels and a legend


# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.xticks(np.arange(0, 31, 1)) 
# plt.yticks(np.arange(0, 80, 5))
# plt.title('Scatter Plot of (X, Y) Coordinates')
# plt.legend()

# # Display the plot
# plt.grid(True)
# plt.show()

daily_averages = {}
print("running file")

for point in points:
    day = int(point[0])  # Extract the day from the first element of each tuple
    value = point[1]     # Extract the value from the second element of each tuple

    if day not in daily_averages:
        daily_averages[day] = []  # Initialize an empty list for each new day
    
    daily_averages[day].append(value)  # Append the value to the corresponding day

# Calculate the average for each day and store it in a new dictionary
daily_averages_result = {}
for day, values in daily_averages.items():
    avg = sum(values) / len(values)  # Calculate the average for the day
    daily_averages_result[day] = avg

# Print the daily averages
for day, avg in sorted(daily_averages_result.items()):
    print(f"Day {day}: {avg}")



daily_averages = {}
for point in points:
    day = int(point[0])
    value = point[1]

    if day not in daily_averages:
        daily_averages[day] = []

    daily_averages[day].append(value)

daily_averages_result = {}
for day, values in daily_averages.items():
    avg = sum(values) / len(values)
    daily_averages_result[day] = avg

# Write the daily averages to the "output.txt" file
with open('output.txt', 'w') as file:
    for day, avg in sorted(daily_averages_result.items()):
        file.write(f'{day} {avg} ')

# Print the length of the points list
print(len(points))

exit()




