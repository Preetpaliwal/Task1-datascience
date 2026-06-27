import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset correctly by skipping the metadata rows at the top.
data = pd.read_csv(
    'database.csv',
    encoding='utf-8-sig',
    skiprows=4,
    skip_blank_lines=True
)

# Remove the extra unnamed columns created by the file format.
data = data.loc[:, ~data.columns.str.startswith('Unnamed')]

# Keep only the population rows.
data = data[data['Indicator Name'] == 'Population, total'].copy()

# Find the latest year column that actually has data.
year_columns = [col for col in data.columns if col.isdigit() and data[col].notna().any()]
if not year_columns:
    raise ValueError('No year columns with data were found in the CSV.')
latest_year = max(year_columns, key=int)

# Prepare the data for plotting.
data = data[['Country Name', latest_year]].rename(
    columns={'Country Name': 'country', latest_year: 'population'}
)
data['population'] = pd.to_numeric(data['population'], errors='coerce')
data = data.dropna(subset=['population'])

print(data.head(5))

# Plot the top countries by population.
plot_data = data.sort_values('population', ascending=False).head(10)

# Bar chart
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.bar(plot_data['country'], plot_data['population'], color='skyblue')
plt.xlabel('Country')
plt.ylabel('Population')
plt.title(f'Top 10 Countries by Population ({latest_year})')
plt.xticks(rotation=45)

# Histogram
plt.subplot(1, 2, 2)
plt.hist(data['population'], bins=15, color='lightgreen', edgecolor='black')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.title(f'Population Distribution ({latest_year})')

plt.tight_layout()
plt.show()
