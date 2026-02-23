# Jan Brainstorm

## Architecture of the program

function get_pages_to_be_scraped():
    >> returns a list: pages_to_scrape = []
    ?? How do we do this?
    !! We need to check for duplicates
    !! filter out project?

function scrape_all_pages(pages_to_scrape):
    && takes pages_to_scrape list
    + uses scrape_a_page function.
    >> returns all_properties variable (dict?)

function scrape_a_page():
    >> return a variable "property_data" that contains the useful data of a page. property = {  }
    ?? Dictionary? what variables?

function write_to_file():
    << takes the all_properties
    >> returns data.csv


### Options

in get_pages_to_be_scraped(): we do one pass for houses, one pass for appartements?
Do we get some of the projects?

#### For get_pages_to_be_scraped(): 
1/ make a list all the postal codes, make a search for each postal code, dump all the links in a file, clean the duplicates
we have to be careful about the projects page here



## Questions

How do we get the list of properties to scrape?
> Jan will look into this question

### Data we gather

property_data = {
    "page_url": str,                    # so we can filter out duplicates
    "locality": str,                    # e.g. "Gent", "Ukkel", "Knokke-Heist"
    "property_type": str,               # "House" OR "Apartment"
    "property_subtype": str,            # "Bungalow", "Chalet", "Mansion", "Townhouse", "Penthouse", ...
    "price": float | int | None,        # sale price in €
    "sale_type": str,                   # especially note if "exclusion of life sales" / viager / ...
    "number_of_rooms": int | None,
    "living_area_m2": float | int | None,
    "kitchen_fully_equipped": bool | None,
    "furnished": bool | None,
    "open_fire": bool | None,
    "has_terrace": bool | None,
    "terrace_area_m2": float | int | None,   # meaningful only if has_terrace = True
    "has_garden": bool | None,
    "garden_area_m2": float | int | None,    # meaningful only if has_garden = True
    "land_area_m2": float | int | None,      # surface of the plot of land
    "number_of_facades": int | None,
    "has_swimming_pool": bool | None,
    "building_condition": str           # "New", "Just renovated", "Good", "To refresh", "To be renovated", ...
}

From the instructions, we need:
    - Locality :
    - Type of property (House/apartment)
    - Subtype of property (Bungalow, Chalet, Mansion, ...)
    - Price
    - Type of sale (Exclusion of life sales)
    - Number of rooms
    - Living Area
    - Fully equipped kitchen (Yes/No)
    - Furnished (Yes/No)
    - Open fire (Yes/No)
    - Terrace (Yes/No)
        - If yes: Area
    - Garden (Yes/No)
        - If yes: Area
    - Surface of the land
?        - Surface area of the plot of land
    - Number of facades
    - Swimming pool (Yes/No)
    - State of the building (New, to be renovated, ...)

?? let's check these are actually present in the data.
> Jan

?? Post code? do we
> Jan

### Reference of classes and tags and such for the data we need to gather
  
page_url : we should have a page url field, so we can check for duplicates.
  
locality : xpath : //*[@id="main_content"]/div[1]/div[1]/div/div[2]/div/span[2] , <span class="city-line">6940 Durbuy</span>
> !! it also includes the postal code, we need to move that somewhere else.
> !! The same postal code can represent different towns, the same town can have different postal codes
> ?? How do we search
  
property_type:
    **Houses** can be : Residence, Chalet, Bungalow, Villa.
    **Appartments** can be: Appartment, Duplex, Loft, Penthouse
    **Projects**: new constructions, there is more than one property. It's a bit more complicated, there is more that one page, the price changes... Ignore?

property subtype: what actually appears in the page: that means the property type is derived from this. 

price: it appears in two places, we'll have to regex it because it's ugly

type of sale : exclusion of life sales. When doing a search, there is a filter for that, so we can make a list of them, and exclude them from the list of urls to scrape.


Data fields:
number of bedrooms: it's in the data fields, all of them seem annoying to retrieve.