# Model Building


### from the readme:
- You have to handle NANs.
- You have to handle categorical data.
- You have to select features.
- You have to remove features that have too strong correlation.

But first, we have to prepare the data for machine learning.

- No duplicates.
- No NANs.
- No text data.
- No features that have too strong correlation between them.

split, select model, model evaluation, write readme

#### style:
typed funciton and classes, docstring, comments, code formatted with black, removed usused comments and code


## My notes
I'll keep the dropped columns dropped for now, that way I acn move ahead. 

### Data cleaning:

Index('locality', 'zip_code', 'property_type', 'property_subtype', 'price',
       'number_of_bedrooms', 'livable_surface_m2', 'furnished', 'has_terrace',
       'has_garden', 'land_area_m2', 'number_of_facades', 'has_swimming_pool',
       'build_year', 'has_garage', 'number_of_garages', 'type_of_heating',
       'has_elevator', 'type_of_glazing', 'energy_KWh_m2_year', 'region',
       'price_by_m2', 'building_state'],
 
bools are: furnished, has_terrace, has_garden, etc...
**Drop**:
locality - redundant with zipcode
region - redundant with zip code
price by m2 -> redundant, derived from price and living area
BUT: in order to make sense of the zip code, i'm thinking of using it.


**Decide:**
zip code: the big one.
property type
property subtype
build year categorical -> bins?
type of glazing -> categorical needs a number, might be redundant with energy
building state : from 1(to demolish) -> 7 (new)



### The plan:

**Data Cleaning**
DROP cols:  
- locality and region -> redundant with zip code
- type of glazing (3 possibilities, annoying, captured by energy)
- type of heating (8 possibilities, annoying to do, somewhat captured by energy, 8k+ nulls + 1700 not specified. almost half empty...) 
  ❓Might want to come back to this


Categoricals
- correlated trio (build_year, building_state, energy): keep all of them, let lasso pick the winner. 
- Building state : keep it as one column. lasso will figure it out. One hot encode possible, but the weight should take care of it, and it's simpler with one column


- Property type / property subtype : We group then one hot encode towards this:
prop_type_num = 
flat + studentFlat + loft + flatStudio
house + masterHouse + mansion
villa
mixedBuilding
duple + triplex
penthouse
others = chalet, bungalow, cottage, groundFloor



Fill in nulls:
has_terrace : if null -> false
Before or after the split makes no difference, it's a hard choice.

**SPLIT**
split into X_train, X_test
> don't forget to drop price here

**Target Encoding for the zipcode**
My idea for now is to do this:
df.groupby(zipcode) get the median price per m2 for that zipcode and write that to a new column for each row. Basically, instead of a zip code i use the median price per m2 for that zipcode.
Reasonable?
> DROP zipcode after this
❗Carefull here and below. When doing this, only calculate values for the train set, and map them to the test set. Don't recalculate a new value for the test set, otherwise, i'm leaking info from the test set, into itself. instead, transform the test set with the values from the train set


**Filling Nulls**
building state (mode)

number of bedrooms (mode)
furnished (mode)
number of facade (mode)

build year, (median)
energy (median)
land area (median)

❗Carefull When doing this, only calculate values for the train set, and map them to the test set. Don't recalculate a new value for the test set, otherwise, i'm leaking info from the test set, into itself. instead, transform the test set with the values from the train set


**Polynomial Expansion**
Before standardisation because everything used needs to be normalised.


**Standardise**

**Model build**

Idea : loop through possible polynomial degrees. hyperparameter search
**Test and score the model**