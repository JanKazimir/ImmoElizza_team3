# Jan Brainstorm

## Architecture of the program:

function get_pages_to_be_scraped():
    >> returns a list: pages_to_scrape = []
    ?? How do we do this?

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



## Questions:
How do we get the list of properties to scrape?
> Jan will look into this question



### Data we gather:

property_data = {
    "locality": str,                    # e.g. "Gent", "Ukkel", "Knokke-Heist"
    "property_type": str,               # "House" / "Apartment" / "Villa" / "Studio" / ...
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

