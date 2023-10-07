points = [(0.1, 2), (0.2, 30), (0.5, 40), (0.9, 1), (1.1, 2), (1.2, 30), (1.5, 40), (1.9, 1)]

# Initialize a dictionary to store daily averages
daily_averages = {}

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
