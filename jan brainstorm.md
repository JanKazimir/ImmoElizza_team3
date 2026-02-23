# Jan Brainstorm

## Architecture of the program

function get_pages_to_be_scraped():
    >> returns a list: pages_to_scrape = []
    ?? How do we do this?

function scrape_all_pages(pages_to_scrape):
    && takes pages_to_scrape list
    + uses scrape_a_page function.
    >> returns all_properties variable

function scrape_a_page():
    >> return a variable "property" that contains the useful data of a page. property = {  }
    ?? Dictionary? what variables?

function write_to_file():
    << takes
    >> returns data.csv

## Questions:

### Data we gather:


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
?? Post code? do we


