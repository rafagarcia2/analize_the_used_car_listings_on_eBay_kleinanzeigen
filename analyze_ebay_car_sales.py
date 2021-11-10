"""analyze_ebay_car_sales.py

Author: Rafael Garcia
Solution to: https://app.dataquest.io/c/54/m/294/guided-project%3A-exploring-ebay-car-sales-data/
"""


import pandas as pd

autos = pd.read_csv("autos.csv", encoding="Latin-1")

new_columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
       'last_seen']

# rename columns
autos = autos.rename(columns=new_columns)

# remove unnecessary columns
columns_to_drop = ['seller', 'offer_type', 'abtest']
autos.drop(columns=columns_to_drop, inplace=True)

# convert columns to number
autos['price'] = autos['price'].apply(lambda x: float(x.replace('$','').replace(',','')))
autos['odometer'] = autos['odometer'].apply(lambda x: float(x[:-2].replace(',', '')))

autos.rename(columns={"odometer": "odometer_km"}, inplace=True)

# remove outliers
autos = autos[autos.price.between(1, 351000)]
autos = autos[autos.registration_year.between(1900, 2016)]

# taking the top 20 tags that appear the most in the dataset
first_20_brands = autos.brand.value_counts().head(20).index

# calculate the mean price
dict_agg_brand = {}
dict_agg_km = {}
for brand in first_20_brands:
    mean_price_brand = autos[autos['brand'] == brand]['price'].mean()
    mean_km_brand = autos[autos['brand'] == brand]['odometer_km'].mean()
    dict_agg_brand[brand] = mean_price_brand
    dict_agg_km[brand] = mean_km_brand

brand_mean_series = pd.Series(dict_agg_brand)
km_mean_series = pd.Series(dict_agg_km)

# create dataframe with values
df_brand_mean = pd.DataFrame(brand_mean_series, columns=['mean_price'])
df_brand_mean['mean_km'] = km_mean_series
