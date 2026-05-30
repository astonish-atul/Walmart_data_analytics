import pandas as pd 
import time 
import requests
from bs4 import BeautifulSoup
import json 
import random
import math
session = requests.Session()
# def product_sku(query,page_number):
#     user_agents = [

#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",

#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",

#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",

#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",

#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/137.0.0.0"
#     ]
#     url = f"https://www.walmart.com/search?q={query}&page={page_number}"

#     Headers = {
#         "User-Agent": random.choice(user_agents),
#         "Accept-Language": "en-US,en;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Referer": "https://www.google.com/",
#     }

    

#     response = session.get(url, headers=Headers , timeout=10)

#     print(response.url)

#     if response.status_code != 200:
#         print(response.status_code)
#         return "no signal"

#     soup = BeautifulSoup(response.text, 'html.parser')

#     sku=[]
    
#     tags=soup.find('script', {'id': '__NEXT_DATA__'})
   
#     data = json.loads(tags.string)

#     items = (
#         data.get('props', {})
#             .get('pageProps', {})
#             .get('initialData', {})
#             .get('searchResult', {})
#             .get('itemStacks', [])[0]
#             .get('items', [])
#     )

#     for item in items:

#         if item.get('usItemId'):
#             sku.append(item.get('usItemId'))

#     return sku


def product_info_extract(links,sku):
    user_agents = [

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",

        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/137.0.0.0"
        ]
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        }


    time.sleep(random.uniform(7, 10))  # Random delay between 5 to 10 seconds
    response = session.get(links, headers=Headers)

    print(f"SKU:{sku} , URL: {response.url}")

    
    soup = BeautifulSoup(response.text, 'html.parser')

    tag=soup.find('script', {'id': '__NEXT_DATA__'})

    data=json.loads(tag.string)

    product = data['props']['pageProps']['initialData']['data']['product']
    final_detail=[]
    reviews_data = data['props']['pageProps']['initialData']['data']['reviews']
    if  (len(reviews_data.get("customerReviews",[]))==0):

        return [{
            "SKU_id": sku,

            "item_name": product.get("name"),

            "review_rating": None,

            "review_title": None,

            "review_text": None,

            "review_date": None,

            "recommended": None,

            "positive_feedback": None,

            "negative_feedback": None,

            "reviewer_name": None,

            "review_language": None,

            "fulfilled_by": None,

            "review_source": None
        }]
    else:
        pages=min(math.ceil(reviews_data.get("totalReviewCount")/10),20)
    if pages > 1:
        a=2
    else:
        a=1
    for page in random.sample(range(1,pages+1), a):  # Randomly sample 2 pages of reviews
        review_link = f"https://www.walmart.com/reviews/product/{sku}?page={page}"
        time.sleep(random.uniform(6, 10))  # Random delay between 6 to 10 seconds
        review_response = session.get(review_link, headers=Headers)
        print(review_response.url)

        print(f"SKU:{sku} , Review Page: {page} , URL: {review_response.url}")


        review_soup = BeautifulSoup(review_response.text, 'html.parser')
        review_tag = review_soup.find('script', {'id': '__NEXT_DATA__'})
        review_data = json.loads(review_tag.string)
        reviews_data = review_data['props']['pageProps']['initialData']['data']['reviews']
        reviewa=reviews_data['customerReviews']
        for review in reviewa:
            info = {
                "SKU_id": sku,
                "item_name": review.get("itemName"),
                "product_category": product.get("category", {}).get("path", [{}])[-1].get("name"),
                "review_rating": review.get("rating"),
                "review_title": review.get("reviewTitle"),

                "review_text":
                    review.get("reviewText"),

                "review_date":
                    review.get("reviewSubmissionTime"),

                "recommended":
                    review.get("recommended"),

                "positive_feedback":
                    review.get("positiveFeedback"),

                "negative_feedback":
                    review.get("negativeFeedback"),

                "reviewer_name":
                    review.get("userNickname"),

                "review_language":
                    review.get("originalLanguage"),

                "fulfilled_by":
                    review.get("fulfilledBy"),

                "review_source":
                    review.get("externalSource")
                }
        
            final_detail.append(info)

    return final_detail


def main():

    all_product_details = []

    current_review_page=1

    product_number=1

    review_pages_to_scrape = 1  # Number of review pages to scrape per product

    # all_product_links = [f"https://www.walmart.com/reviews/product/{sku}?entryPoint=viewAllReviewsBottom&page={page}" for sku in product_sku_list for page in range(1, review_pages_to_scrape + 1)]
    missed_sku_list=[6515767297, 1646180610, 5289658885, 14975806858, 14522924811, 14538861837, 15443515279, 18324370193, 16899107729, 17607251346, 5306514453, 1656267286, 19915011478, 18030815517, 18648313811, 16385702047, 12835817248, 15178507679, 17874774562, 17429700518, 17902801448, 14822456361, 1724203176, 5321227054, 17637412271, 1847884976, 17591873202, 14541464758, 18263516985, 454408250, 15627174329, 19593853244, 16543872317, 19231566273, 20149518152, 986398921, 5243845836, 3341343950, 15689361616, 16347721681, 952665682, 14524651090, 16339673812, 16956323029, 17935752826, 14575306839, 19209163478, 12043760468, 5420668122, 14655311963, 5298865371, 5554158424, 14544200150, 15189959010, 19202402404, 11632865509, 16282016746, 18805066987, 17637113324, 2000499822, 397381999, 19340372593, 14672556913, 16624205172, 14351850484, 19312158201, 14506123386, 916649084, 17862610558]
    for sku in missed_sku_list: #Started from product index 1 i.e 2nd product

        link = f"https://www.walmart.com/reviews/product/{sku}?page=1"
        details = product_info_extract(link, sku)
        all_product_details.extend(details)

    df=pd.DataFrame(all_product_details)
    # df.to_csv("product_info_walmart.csv", index=False)
    #append to csv file
    df.to_csv("product_info_walmart.csv", mode='a', header=False, index=False)

if __name__ == "__main__":
    main()

