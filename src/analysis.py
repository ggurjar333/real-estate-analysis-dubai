# Feature engineering
import pandas as pd

# Load the data
data = pd.read_csv('2023-11-20_14-00-08_extracted_data.csv')

# Feature engineering
data['price_range'] = pd.cut(data['price'], bins=[0, 100000, 200000, 300000, float('inf')], labels=['0-100k', '100k-200k', '200k-300k', '300k+'])
data['price_per_sqft'] = data['price'] / data['area_square_feet']
data['bed_bath_ratio'] = data['bedrooms'] / data['bathrooms']
data['total_rooms'] = data['bedrooms'] + data['bathrooms']

# Save the DataFrame to JSON
featured_data = data.to_json('featured_data.json', orient='records')
