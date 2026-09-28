# 👖🌱 Decode Backend (🥈 at SustainHacks 2022)
## Contributors: Jay Esquivel Jr, Shawn Esquivel
Welcome to the backend powering DECODE, the chrome extension that which helps you make greener decisions on apparel products.

More details: https://devpost.com/software/decode-z8ecsg

Front-end Code: https://github.com/shawnesquivel/decode

![Decode's Demo Gif](https://user-images.githubusercontent.com/94336773/205826346-1242214f-aa83-401a-a5c2-04465cb6499f.gif)

## How it works
    1. Signalled by opening the front-end (clicking on the extension)
    2. Processes an HTTP request of the webpage
    3. Web-scrapes the current product page's data
    4. Classifies and interprets the material data on the page
    5. Returns the applicable/identifiable material data in JSON-readable format for auto-fill
    6. Api request signalled by the extension submit button, 
    7. Form information is passed via the URL call using a specific format
    8. Back-end does the calculations and returns the calculations

## Challenges
While the planning and set-up portion of our project went smooth, coding for completion given the time alotted was the teams biggest challenge.
It wasn't until we had to figure out how to merge the front-end and back-end together that we ran into concerns over our extensions 
security and final functionality as the two pieces were working as intended separately.

## Accomplishments
This was both of our first times working on a hybrid website/chrome extension product and we were both able to have a taste of completely brand
new roles in our development journeys. Any opportunity I get to add a new tool to my toolkit is an exciting experience.

## Instructions
Use Python 3.10 or newer (CI verifies Python 3.10 and 3.12). Install the reviewed
dependency tree with `python -m pip install --require-hashes -r requirements.lock`.
Direct dependency pins remain in `requirements.txt`; regenerate the hashed lock
with `uv pip compile requirements.txt --python-version 3.10 --generate-hashes -o requirements.lock`.

1. Run `python -m unittest discover -s tests -v` to check local HTTP scraping and
   route contracts. The tests use synthetic data, not live retailers; the existing
   calculator placeholder is deliberately left unchanged.

2. Open a terminal in the root directory

3. Run the command 'python server.py'

4. Now, on a browser, we can test the following.

a)
To test product URL web-scraping, paste:
localhost/webscrape?url={insert url of below here}

Example Items:
- Shirt
https://www.urbanoutfitters.com/en-ca/shop/standard-cloth-angus-popover-polo-shirt?category=SEARCHRESULTS&color=011&searchparams=q%3Dshirt&type=REGULAR&quantity=1

- Jacket
https://www.adidas.ca/en/polar-fleece-nature-allover-print-1-4-zip-jacket/HK4575.html

- Jeans
https://ca.shein.com/High-Waist-Slant-Pocket-Straight-Leg-Jeans-p-2846834-cat-1934.html?src_identifier=st%3D2%60sc%3Djeans%60sr%3D0%60ps%3D1&src_module=search&src_tab_page_id=page_search1670150132131&mallCode=1&scici=Search~~EditSearch~~1~~jeans~~~~0

Example Jsonified Web-scraped Data:
{
    brand: "SHEIN"
    cloth_type: "pants"
    materials: [
        "Cotton: 62%",
        "Polyester: 37%",
        "Viscose 1%"
    ]
    num_washes: 200
    weight_grams: 890
}

To test the product sustainability calculator, paste:
http://localhost:80/submit?brand=$Nike&cloth_type=$Jacket&materialone=$Polyester&materialtwo=$Cotton&num_washes=$125&weight=$800

localhost/submit$brand=Nike&cloth_type=jacket&
Example Jsonified Calculations:
{
    sustainability_rating: 100
    fabric_quality: 67
    num_washes: 125
}
