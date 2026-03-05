## Questions i'm curious about

Price is the most relevant factor. 
correlations to price are obvious.


- The obvious stuff : 
  - what are the strongest correlations to price.
  - what are the weakest?
  - any surprises?
  

- Can we group or bundle variables into one? : eco friendlyness score = solar panels, heat pump, energy efficiency, a few more? maybe smallness

Does having something rare in an area push prices up?
Zipcode, compute the average of each bool.
    - for those "rare" bools (less than 20% yes) : does being yes increase price?


- What is the correlation of price by liveable area, per zipcode? that's the basic version. 
    > the complex version is to take into account the median liveable area of the area. say does the 75% percentile of appartments in ixe
    > actually, what is the distribution here: linear or exponential?

Thinking in terms of distribution is useful.


- average size per zipcode? 
    > to a map?



## Data cleaning for the machine learing part:
It's more complicated. 
We can't have nulls, so we need to fill in or drop, but that means more fine control, more subjective analysis.
Second, when we fill in the nulls, there are some do and don't : don't fill in the data using median from the whole data set, otherwise you have data leakage. 

so it's more ccomplicated.








For cleaning
lots of missing values on :

kitchen equipment
garden area : check how many garden area are missing in garden area is true.
has swimming pool
has cellar
number of garages presumably, if has garage is true and num of garage is none, num of garage is 1
is low energy
has solar panel
has floor heating
has heat pump
has fireplace
has balcony
has attic
yearly_total_primary_energy_consumption_in_kWh_by_year



## Todo:
a function to get the column health : percentage of missing, anything above fifty is sketchy.



## Cheat sheet:
Inspect: df.info(), df.describe(), df.shape, df.dtypes, df.head()
Missing values:  df.isnull().sum(), df.dropna(), df.fillna(value)
Duplicates: df.duplicated(), df.drop_duplicates()
Rename / Drop: df.rename(columns={...}), df.drop(columns=[...]), df.drop(index=[...])
Type conversion: df.astype(), pd.to_numeric(), pd.to_datetime()
String cleaning: df['col'].str.strip(), .str.lower(), .str.replace()
Filtering / Replacing: df[df['col'] > x], df.replace(), df.where(), df.mask()
Apply custom logic: df.apply(fn), df.map(fn)


## Some observatiosn as I go through:
