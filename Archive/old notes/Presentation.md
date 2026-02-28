# Presentation: ImmoEliza Team 3


## What to say:
- Main blocks of the projects are:
  
  - Get the data
    - scrape data from a property page >> write to file
    - scrape all property pages by calling (scrape data) >>
  
  - Knowing what data to get:
    - get the property links from **one** search page
    - get **all** the search pages
  
  
## Challenges:
1 Get past the 50 pages of search results:

  - Filter by property type until you have less that 2000 results.
    - 2000 because forward and backwards 
    - >>> not a good idea in the end, difficult to automate, not elegant.
  -   Filter by price: Annoying to check if each range is less than 200
  -   Filter by post code
- Make it fast



Do a presentation on the following slides, as marked
Keep the text as it is. 
MAKE THE TEXT READABLE FROM FAR AWAY!
Keep it simple.
Make it look nice. Design should feel elegant, simple, dark mode, with a max of three accent colors. Reuse the same colors for the whole thing. 
You can have images to illustrate, but don't overdo it.



---

# 🏠 ImmoEliza — Team 3

---

## The Pipeline

> **1 — Get the Data**
> - `4` Scrape data from a property page → write to file
> - `5` Scrape all property pages by calling `scrape_data()`
>   - `6` ⚠️ This needs all the property links!

> **2 — Knowing What Data to Get**
> - `7` Get the property links from a search page → write to file
> - `8` Get all the search pages

> **3 — Data Manipulation**
> - `9` Clean the data (remove duplicates)
> - `10` Expect crashes → Write data to file

---

## First Challenge

### **Getting past 50 pages of results**

Build a new URL by changing the page number

---

## First Idea: Filter by Province

> ❗ More than 1000 results for most provinces
>
> → Forward and reverse trick

- Still 4 provinces with more than 2000 results
  - Slice the data further? (subtypes, prices…)
    - → **Inelegant, messy, hard to automate…**

---

## Better Idea: Filter by Zip Code

- Trick the site's API to give out all `{"zip_code": "city"}`
- Build a function to generate search page URLs
- Test it works
- → `All_Search_Pages.json`
- → `get_property_links_from_a_search_page()`
- → **ALL property links collected** ✅

---

## Second Challenge: Cleaning Data

**JSON with duplicates → New JSON without duplicates**

---

## Avoiding Crashes & Data Manipulation

- **Challenge:** Avoid data crashes
  - → Write each scraped line to a JSON

- **Manipulate data:**
  - → JSON to CSV converter

---

## Ultimate Challenge

### …solving the GitHub mess…

---

## Solution

- Ask colleagues 🤝

---

## Q&A

**How do you organise your Repo?**