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
            points.append((30*(number/width), 160*(-y/height)+160))
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

# # plt.plot(xy_pd_df["x"], xy_pd_df["y"])

# # Add labels and a legend


# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.xticks(np.arange(0, 31, 1)) 
# plt.yticks(np.arange(0, 80, 5))
# plt.title('Scatter Plot of (X, Y) Coordinates')
# plt.legend()

# # Display the plot
# plt.grid(True)
# plt.show()


with open('output.txt', 'w') as file:
    # Write the length of the points list as the first number
    file.write(f'{len(points)} ')
    
    # Iterate through the list of tuples
    for point in points:
        # Write the tuple values separated by a space
        file.write(f'{point[0]} {point[1]} ')

# Close the file
file.close()

print(len(points))




