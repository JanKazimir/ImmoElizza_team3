 So i found this in the html
 
 
 $(document).ready(() => {
        localStore.setItem(
            STORAGE_KEY_PROPERTY_DETAILS,
            JSON.stringify({
                reference: 'RWC41877',
                transactionTypeId: 74,
                transactionType: 'Sale',
                propertyTypeId: 2,
                propertyType: 'Appartment',
                propertySubTypeId: 26,
                propertySubType: 'Duplex',
                id: '10512664',
                price: '235000.00',
                vlanCode: 'rwc41877',
                sellerType: 'private',
                sellerTypes: 'private',
                sellerId: '3556709',
                priceRangeId: '23',
                zipCode: '3630',
                city: 'Meeswijk',
                country: 'Belgium',
                countryId: '1'
            }));
    });


      dataLayer.push({
  "property_type": "appartment",
  "property_sub_type": "duplex",
  "transaction_type": "sale",
  "zip_code": "3630",
  "vlan_code": "rwc41877",
  "livable_surface": "128.00",
  "price": "235000.00",
  "seller_type": "private",
  "seller_id": "3556709",
  "is_new_construction_project": false,
  "country_id": 318,
  "software": null,
  "page_language": "en",
  "page_type": "propertyDetailResult"



              for magicbox in soup.find_all("script", type="text/javascript"):
                magic_text = magicbox.get_text()
                m = re.search(r'\"property_type\": \"(\w+)\"', magic_text)
                if m:
                    print("Found property_type:", m.group(1))
                    property_data["property_type"] = m.group(1)
                    break
                


All fields we need:

property_data = {
    "page_id": int,   ✅                  # index, set as default for now
    "page_url": str,   ✅                 # done
    "locality": str, ❗
    "zip_code":        ✅                 
    "property_type": str,   ✅            # houses, appartment, investment property
    "property_subtype": str,  ✅        
    "price": float | int | None,  ✅      #
    "number_of_rooms": int | None, ✅
    "living_area_m2": float | int | None, ✅
    "kitchen_fully_equipped": bool | None, ❗
    "furnished": bool | None, ✅
    "open_fire": bool | None,
    "has_terrace": bool | None, ✅
    "terrace_area_m2": float | int | None,   ✅
    "has_garden": bool | None, ✅
    "garden_area_m2": float | int | None,   ✅
    "land_area_m2": float | int | None,    ✅  
    "number_of_facades": int | None, ✅
    "has_swimming_pool": bool | None,
    "building_condition": str , ✅
    "build_year": int ✅
}
More fields to get: let's prioritize:

Cellar
Yes

Garage
Yes

Balcony
Yes

Elevator
Yes

Access for disabled
No


Fireplace
No

Specific primary energy consumption
45 kWh/m²/year

EPC/PEB reference
A


Type of glazing
Double glass

Low-energy house
Yes

Solar panels
Yes

Floor heating
Yes

Heat pump
Yes


Number of garages
1


Surface of living-room
32 m²

Surface bedroom 1
15 m²

Surface bedroom 2
14 m²


Surface kitchen
9 m²

Number of bathrooms
1

Number of showers
1

Surface of the bathroom(s)
5 m²




Fireplace
No

Access for disabled
Yes

Balcony
Yes

Specific primary energy consumption
45 kWh/m²/year

EPC/PEB reference
A








## problems:
can't use xpaths, they'll change between pages. I need to regex this shit

            
            # Number of Bedrooms:
            property_data["number_of_rooms"] = tree.xpath("//*[@id='main_content']/div[8]/div/div[2]/div/div[1]/p")[0].text_content()
            property_data["building_condition"] = tree.xpath("//*[@id='main_content']/div[8]/div/div[1]/div/div[1]/p")[0].text_content()

            