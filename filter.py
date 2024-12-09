import pandas as pd

data = pd.read_csv('sample.csv')

# Define the list of categories to retain
desired_categories = [
    'Food', 'Nightlife', 'Bars', 'American (Traditional)', 'American (New)',
    'Breakfast & Brunch', 'Sandwiches', 'Seafood', 'Restaurants'
]

# Convert the list of categories into a regex string
pattern = '|'.join(desired_categories)  # Create a regex pattern like 'Food|Nightlife|Bars|...'

# Filter the DataFrame to only include rows matching the categories
filtered_data = data[data['categories'].str.contains(pattern, case=False, na=False)]

# Display the filtered DataFrame
print(filtered_data)

# Optionally save the filtered data to a new CSV
filtered_data.to_csv('restaurants.csv', index=False)
