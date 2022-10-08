from types import NoneType
from django.test import TestCase, Client
from . import views
from . import models

# Create your tests here.


class TestUtilityFunctions(TestCase):
    # def setUp(self):

    #     # Create suburbs.
    #     models.Suburb.objects.create()
    #     # a1 = Airport.objects.create(code="AAA", city="City A")
    #     # a2 = Airport.objects.create(code="BBB", city="City B")

    #     # # Create flights.
    #     # Flight.objects.create(origin=a1, destination=a2, duration=100)
    #     # Flight.objects.create(origin=a1, destination=a1, duration=200)
    #     # Flight.objects.create(origin=a1, destination=a2, duration=-100)



    def test_filter(self):
        """ Test if the filter function works correctly. """

        # Create lists
        lst_1 = [20, 15, 12, 5, 17, 10]
        lst_2 = ['a', 'c', 'b', 'd', 'g', 'f']
        lst_3 = []
        lst_4 = ['a']

        self.assertEqual(views.filter(
            lst_1, lambda e: e > 10), [20, 15, 12, 17])
        self.assertEqual(views.filter(lst_2, lambda e: e != 'c'), [
                         'a', 'b', 'd', 'g', 'f'])
        self.assertEqual(views.filter(lst_3, lambda e: e > 0), [])
        self.assertEqual(views.filter(lst_4, lambda e: e != 'c'), ['a'])
        self.assertEqual(views.filter(lst_4, lambda e: e != 'a'), [])

    def test_map(self):
        """ Test if the map function works correctly. """

        # Create lists
        lst_1 = [20, 15, 12, 5, 17, 10]
        lst_2 = ['a', 'c', 'b', 'd', 'g', 'f']
        lst_3 = []
        lst_4 = ['a']

        self.assertEqual(views.map(lst_1, lambda e: 5 * e),
                         [100, 75, 60, 25, 85, 50])
        self.assertEqual(views.map(lst_2, lambda e: 2*e),
                         ['aa', 'cc', 'bb', 'dd', 'gg', 'ff'])
        self.assertEqual(views.map(lst_3, lambda e: 10*e), [])
        self.assertEqual(views.map(lst_4, lambda e: 'c'), ['c'])
        self.assertEqual(views.map(lst_4, lambda e: e), ['a'])

    def test_location(self):
        """ Test if the Location class behaves correctly. """

        # Create locations
        l1 = views.Location(-18.375, 167.89)
        l2 = views.Location(37.625, 155.75)

        self.assertEqual(l1.get_latitiude(), -18.375)
        self.assertEqual(l1.get_longitude(), 167.89)
        self.assertEqual(l2.get_latitiude(), 37.625)
        self.assertEqual(l2.get_longitude(), 155.75)


    def test_haversine_distance(self):
        """ Test if the haversine_distance function works correctly. """

        # Create locations
        melbourne = views.Location(-37.840935,144.946457)
        sydney = views.Location(-33.865143,151.209900)
        brisbane = views.Location(-27.470125, 153.021072)
        perth = views.Location(-31.953512, 115.857048)


        self.assertLess(abs(views.haversine_distance(melbourne,sydney) - 714.23), 5)
        self.assertLess(abs(views.haversine_distance(brisbane,sydney) - 733.15), 5)
        self.assertLess(abs(views.haversine_distance(perth,sydney) - 3294.14), 5)

    def test_add_photo(self):
        """ Test if the add_photo function works correctly. """

        # Create suburbs
        clayton = {"latitude": -37.915047, "longitude":145.129272,"name":"Clayton"}
        caufield = {"latitude": -37.876823, "longitude":145.045837,"name":"Caufield"}
        oakleigh = {"latitude": -37.883, "longitude":145.117,"name":"Oakleigh"}
        chadstone = {"latitude": -37.8876600, "longitude":145.0951900,"name":"Chadstone"}

        # Add photo and place id to suburbs
        clayton_with_photo_and_place_id = views.add_photo(clayton)
        caufield_with_photo_and_place_id = views.add_photo(caufield)
        oakleigh_with_photo_and_place_id = views.add_photo(oakleigh)
        chadstone_with_photo_and_place_id = views.add_photo(chadstone)

        # Check if photo has been added
        self.assertTrue("photo" in clayton_with_photo_and_place_id)
        self.assertNotEqual(clayton_with_photo_and_place_id["photo"], "")

        self.assertTrue("photo" in caufield_with_photo_and_place_id)
        self.assertNotEqual(caufield_with_photo_and_place_id["photo"], "")

        self.assertTrue("photo" in oakleigh_with_photo_and_place_id)
        self.assertNotEqual(oakleigh_with_photo_and_place_id["photo"], "")

        self.assertTrue("photo" in chadstone_with_photo_and_place_id)
        self.assertNotEqual(chadstone_with_photo_and_place_id["photo"], "")

        # Check if place_id has been added
        self.assertTrue("place_id" in clayton_with_photo_and_place_id)
        self.assertTrue("place_id" in caufield_with_photo_and_place_id)
        self.assertTrue("place_id" in oakleigh_with_photo_and_place_id)
        self.assertTrue("place_id" in chadstone_with_photo_and_place_id)


