from geopy.geocoders import Nominatim
import pandas as pd

def country_state_county_zip(lat, long):
    coord = str(lat) + ', ' + str(long)
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    county = address.get('county', '')
    state = address.get('state', '')
    country = address.get('country', '')
    ZIP = address.get('postcode', '')

    return country, state, county, ZIP

geolocator = Nominatim(user_agent="MyGeocoder")

df = pd.read_csv("demo-ghcnd-stations-lat-long.csv",)  #hi

#Create columns if they dont exist (ie: if the file has not been run before)
if 'Country' not in df:
    df["Country"] = ""
if 'State' not in df:
    df["State"] = ""
if 'County' not in df:
    df["County"] = ""
if 'ZIP' not in df:
    df["ZIP"] = ""

# Because on large files there will be timeout errors, run through the loop three times,
# This will make sure that rows had errors will have a 2nd and 3rd chance to be looked at.
for i in range(3):
    for index, row in df.iterrows():

        lat = float(row['Latitude'])
        long = float(row['Longitude'])

        #For checking just WA state
        #if 49.196064 > lat > 45.576501 and -125.375188 < long < -116.821468 \
        #         and pd.isnull(df.loc[df.index[index], 'Country']) == True:

        #For checking entire US
        #if 22.824922 < lat < 49.774613  and -126.196032 < long < -64.103819 \
        #         and pd.isnull(df.loc[df.index[index], 'Country']) == True:

        if len(df.loc[df.index[index], 'Country']) == 0:
            try:

                #Get data
                data = country_state_county_zip(lat,long)

                #Add data pieces to columns in the dataframe
                df.loc[df.index[index], 'Country'] = data[0]
                df.loc[df.index[index], 'State'] = data[1]
                df.loc[df.index[index], 'County'] = data[2]
                df.loc[df.index[index], 'ZIP'] = data[3]

                #Just for debugging/interest, print line found.
                print('Row: '+ str(index))

            except:
                print('Error on row: ' + str(index))
                df.to_csv("finalError.csv", index=False)

#Export to new CSV
df.to_csv("final.csv", index=False)
print('Completed')
