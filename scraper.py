# import libraries

from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv



def scrape():

    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        items = []
        for i in range (3):
            # specify the url
            meal_page = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal='+str(i)


            # query the website and return the html to the variable ‘page’
            page = urlopen(meal_page)

            # parse the html using beautiful soup and store in variable `soup`
            soup = BeautifulSoup(page, 'html.parser')

            # Take out the <div> of name and get its value


            items.append([])
            for wrapper in soup.find_all('div', attrs={'class': 'item_wrap'}):
                # gets link as a string
                link = wrapper.span.a.get('href')
                food_page = urlopen(link)
                # turn into beautiful soup object

                nutrition_data = BeautifulSoup(food_page, 'html.parser')
                item_name = nutrition_data.find('span', attrs={'class': 'sub_title'}).text.strip()

                try:
                    nutrition_table = nutrition_data.find('tr', attrs={'class': 'three_column'}).find_all('td')
                    # .contents gets children or .texts
                    # texts (not still has b and br tags)
                    # this returns a list with separated where the br's occur
                    # nutriton_facts [0] is left of <br>
                    # gets the first td

                    nutrition_facts = nutrition_table[0].p.text.split('\n')
                    # gets to the right of </b> and left of &nbsp

                    serving_size = int (nutrition_facts [1].split(': ')[1].split('\xa0')[0])
                    calories = int (nutrition_facts [2].split(': ')[1])
                    calories_from_fat = int(nutrition_facts [3].split(': ')[1])

                    amount_serving = nutrition_table[1].p.text.split('\n')

                    total_fat = float (amount_serving[1].split(': ')[1].split(' ')[0])
                    saturated_fat = float (amount_serving[2].split(': ')[1].split(' ')[0])

                    # open a csv file with append, so old data will not be erased


                    writer.writerow([item_name, i, serving_size, calories, calories_from_fat, total_fat, saturated_fat])
                except:
                    print ("invalid data")

        print (items)

if __name__ == "__main__":
    scrape()