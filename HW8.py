# Your name: Sam Gibson
# Your student id: 42836823
# Your email: samcg@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import numpy as np

def load_rest_data(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute("SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants "
                "JOIN categories ON restaurants.category_id = categories.id "
                "JOIN buildings ON restaurants.building_id = buildings.id")
    
    ndict = {}

    for row in cur:
        name = row[0]
        category = row[1]
        building = row[2]
        rating = row[3]
        inner_dict = {'category': category, 'building': building, 'rating': rating}
        ndict[name] = inner_dict

    return ndict

def plot_rest_categories(db):

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute("SELECT category, COUNT(*) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category")

    cdict = {}
    for row in cur:
        cdict[row[0]] = row[1]

    sdict = dict(sorted(cdict.items(), key=lambda x: x[1], reverse=False))

    keys = list(sdict.keys())
    vals = list(sdict.values())

    fig, ax = plt.subplots(figsize=(7,5))
    
    ax.barh(keys, vals, color='darkturquoise')
    ax.set_xlabel('# of Restaurants')
    ax.set_ylabel('Restaurant Category')
    ax.set_title('Types of Restaurants on South U')
    plt.xticks([0, 1, 2, 3, 4])
    plt.tight_layout()
    plt.show()
    return sdict

def find_rest_in_building(building_num, db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute(f"SELECT restaurants.name, buildings.id, restaurants.rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = {building_num} ORDER by restaurants.rating DESC")

    rlist = []
    for row in cur:
        rlist.append(row[0])

    return rlist

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    # def test_get_highest_rating(self):
    #     highest_rating = get_highest_rating('South_U_Restaurants.db')
    #     self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
