from playwright.sync_api import sync_playwright
import pandas as pd
import numpy as np


def main():
    
    with sync_playwright() as p:
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        i = 0
        for page_number in np.arange(0, 500, 25):
            page_url = f"https://www.booking.com/searchresults.en-us.html?label=gen173nr-1FCAEoggI46AdIM1gEaLICiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuALloKujBsACAdICJDRmMjM3ZTVjLTc4MTctNDliZi1hNmY1LTVhMDU3ZWFiZjc1ZNgCBeACAQ&aid=304142&ss=Dominican+Republic&ssne=Dominican+Republic&ssne_untouched=Dominican+Republic&lang=en-us&sb=1&src_elem=sb&dest_id=60&dest_type=country&checkin=2023-09-01&checkout=2023-09-10&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=class&offset={page_number}"
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(page_url, timeout=60000)
                        
            hotels = page.locator('//div[@data-testid="property-card"]').all()
            print(f'There are: {len(hotels)} hotels.')

            hotels_list = []
            
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                # hotel_dict['address'] = hotel.locator('//div[@data-testid="address"]').inner_text()
                hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                #hotel_dict['Total'] = hotel.locator('//div[@data-testid="review-score"]').inner_text()
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
                hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

                hotels_list.append(hotel_dict)

            if i == 0:
                df = pd.DataFrame(hotels_list)
                df.to_csv('hotels_list_1.csv', mode='w', index=False) 

            elif i >= 0:
                df = pd.DataFrame(hotels_list)
                df.to_csv('hotels_list_1.csv', mode='a', header=False, index=False)
            
            i += 1        
        browser.close()

            
if __name__ == '__main__':
    main()