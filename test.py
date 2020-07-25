import selenium
from selenium import webdriver as wb
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas

option = wb.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs

chrome_prefs["profile.default_content_settings"] = { "popups": 1 }
def scrape(link_list):
    webD = wb.Chrome(r"C:\Users\Shubham\.wdm\drivers\chromedriver\win32\83.0.4103.39\chromedriver.exe",chrome_options = option)
    link = link_list
    webD.get(link)
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'Dq9MAugU'))
        WebDriverWait(webD,100).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        try:
            name = webD.find_element_by_class_name('_3ggwzaPV').text
            reviewPanel = webD.find_element_by_class_name('_3VED7yyh')
            no_of_reviews = reviewPanel.find_element_by_class_name('reviewCount').text
            el = reviewPanel.find_element_by_class_name('ui_bubble_rating')
            flight_rating = float(el.get_attribute('class').split()[1][-2:])/10
        except:
            return
        reviews=[]
        flag=True
        f=True
        while flag:
            try:
                time.sleep(5)
            except TimeoutException:
                print("Timed out waiting for page to load")
            finally:
                try:
                    review_divs = webD.find_elements_by_class_name('Dq9MAugU')
                    clickObj = webD.find_elements_by_class_name('XUVJZtom')
                except:
                    f = False
                for obj in clickObj:
                    try:
                        obj.click()
                    except:
                        f = False
                for review_div in review_divs:
                    try:
                        customer = review_div.find_element_by_class_name('_2fxQ4TOx').text.split()
                        if(len(customer)):
                            customer_name = customer[0]
                            date = customer[-2] + customer[-1]
                        else:
                            break
                    except:
                        break
                    try:
                        flight_description = review_div.find_elements_by_class_name('_3tp-5a1G')
                        if len(flight_description):
                            travel_route = flight_description[0].text
                        else:
                            travel_route = "NA"
                        #suspected heading
                        if len(flight_description)>1:
                            type_of_flight = flight_description[1].text
                        else:
                            type_of_flight = "NA"
                        if len(flight_description)>2:
                            class_of_flight = flight_description[2].text
                        else:
                            class_of_flight = "NA"
                    except:
                        travel_route = "NA"
                        type_of_flight = "NA"
                        class_of_flight = "NA"

                    try:
                        el = review_div.find_element_by_class_name('ui_bubble_rating')
                        overall_rating = float(el.get_attribute('class').split()[1][-2:])/10
                    except:
                        overall_rating = -1
                    try:
                        review_heading = review_div.find_element_by_class_name('glasR4aX').text
                        text_review = review_div.find_element_by_class_name('cPQsENeY').text
                    except:
                        review_heading = "NA"
                        text_review = "NA"
                    try:
                        ratingPanel = review_div.find_elements_by_class_name('_3ErKuh24')
                        if len(ratingPanel):
                            legroom_rating = float(ratingPanel[0].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            legroom_rating = -1
                        if len(ratingPanel)>1:
                            seat_comfort_rating = float(ratingPanel[1].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            seat_comfort_rating = -1
                        if len(ratingPanel)>2:
                            in_flight_entertainment_rating = float(ratingPanel[2].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            in_flight_entertainment_rating = -1
                        if len(ratingPanel)>3:
                            customer_service_rating = float(ratingPanel[3].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            customer_service_rating = -1
                        if len(ratingPanel)>4:
                            value_for_money_rating = float(ratingPanel[4].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            value_for_money_rating = -1
                        if len(ratingPanel)>5:
                            cleanliness_rating = float(ratingPanel[5].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            cleanliness_rating = -1
                        if len(ratingPanel)>6:
                            check_in_rating = float(ratingPanel[6].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            check_in_rating = -1
                        if len(ratingPanel)>7:
                            food_rating = float(ratingPanel[7].find_element_by_class_name('ui_bubble_rating').get_attribute('class').split()[1][-2:])/10
                        else:
                            food_rating = -1
                    except:
                        food_rating = -1
                        check_in_rating = -1
                        cleanliness_rating = -1
                        value_for_money_rating = -1
                        customer_service_rating = -1
                        in_flight_entertainment_rating = -1
                        seat_comfort_rating = -1
                        legroom_rating = -1
                    tmp = {
                        'customer_name':customer_name,
                        'date':date,
                        'travel_route':travel_route,
                        'type_of_flight':type_of_flight,
                        'class_of_flight':class_of_flight,
                        'overall_rating':overall_rating,
                        'review_heading': review_heading,
                        'text_review':text_review,
                        'legroom_rating':legroom_rating,
                        'seat_comfort_rating':seat_comfort_rating,
                        'in_flight_entertainment_rating':in_flight_entertainment_rating,
                        'customer_service_rating':customer_service_rating,
                        'value_for_money_rating':value_for_money_rating,
                        'cleanliness_rating':cleanliness_rating,
                        'check_in_rating':check_in_rating,
                        'food_rating':food_rating
                    }
                    reviews.append(tmp)
            if len(reviews)>=300:
                break
            try:
                next_button = webD.find_element_by_class_name("next")
            except:
                break
            if next_button.get_attribute('class').split()[-1] == "disabled":
                break
            else:
                try:
                    next_button.click()
                except:
                    break
        tmpObj = {
            'flight_name' : name,
            'no_of_reviews':no_of_reviews,
            'flight_overall_rating': flight_rating,
            'reviews': reviews
        }
        arr = [tmpObj]
        df=pandas.DataFrame(arr)
        df.to_csv('dataset.csv',mode='a',header=False)
        webD.close()
        return 1