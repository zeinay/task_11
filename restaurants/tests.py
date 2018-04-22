from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from restaurants.models import Restaurant, Item
from restaurants.forms import RestaurantForm, ItemForm, SignupForm, SigninForm
from restaurants.views import restaurant_create, restaurant_delete, restaurant_update, item_create
from django.http import response

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
            )
        self.user.set_password(self.user.password)
        self.user.save()

    def test_create(self):
        restaurant = Restaurant.objects.create(
            owner= self.user,
            name="Hamza's Pizza",
            description="Pizza that tastes really good.",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png",
            )
        item = Item.objects.create(
            name="Hamza's Special Pizza",
            description="The restaurant's special.",
            price=1.750,
            restaurant=restaurant,
            )
    

class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
            is_staff=True,
            )
        self.user.set_password(self.user.password)
        self.user.save()
        self.user2 = User.objects.create(
            username="bob2",
            password='adminadmin',
            )
        self.user2.set_password(self.user2.password)
        self.user2.save()
        self.user3 = User.objects.create(
            username="bob3",
            password='adminadmin',
            )
        self.user3.set_password(self.user3.password)
        self.user3.save()

        self.restaurant_data = {
            "name": "Hamza's Pizza",
            "description": "Pizza that tastes really good.",
            "opening_time": "00:01:00",
            "closing_time":"23:59:00",
            "logo":"http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            }
        self.item_data = {
            "name": "Original Pizza",
            "description": "Best original pizza ever.",
            "price": 1.750,
        }

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            name="Restaurant 1",
            description="This is Restaurant 1",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.item_1_1 = Item.objects.create(
            name="Pizza 1",
            description="This is Pizza 1",
            price=1.750,
            restaurant=self.restaurant_1,
            )
        self.item_1_2 = Item.objects.create(
            name="Pizza 2",
            description="This is Pizza 2",
            price=1.750,
            restaurant=self.restaurant_1,
            )

        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user2,
            name="Restaurant 2", 
            description="This is Restaurant 2",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.item_2_1 = Item.objects.create(
            name="Pizza 1",
            description="This is Pizza 1",
            price=1.750,
            restaurant=self.restaurant_2,
            )
        self.item_2_2 = Item.objects.create(
            name="Pizza 2",
            description="This is Pizza 2",
            price=1.750,
            restaurant=self.restaurant_2,
            )

        self.restaurant_3 = Restaurant.objects.create(
            owner=self.user,
            name="Restaurant 3",
            description="This is Restaurant 3",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.item_3_1 = Item.objects.create(
            name="Pizza 1",
            description="This is Pizza 1",
            price=1.750,
            restaurant=self.restaurant_3,
            )
        self.item_3_2 = Item.objects.create(
            name="Pizza 2",
            description="This is Pizza 2",
            price=1.750,
            restaurant=self.restaurant_3,
            )
        
        self.user_data_1 = {
            "username": "bob",
            "password": "adminadmin"
            }
        self.user_data_2 = {
            "username": "billy",
            "password": "adminadmin",
            }
        self.user_data_3 = {
            "username": "bob",
            "password": "",
            }
        self.user_data_4 = {
            "username": "",
            "password": "somepassword",
            }

    def test_restaurant_list_view(self):
        list_url = reverse("restaurant-list")
        response = self.client.get(list_url)
        for restaurant in Restaurant.objects.all():
            self.assertIn(restaurant, response.context['restaurants'])
            self.assertContains(response, restaurant.name)
            self.assertContains(response, restaurant.description)
            self.assertContains(response, restaurant.logo.url)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.status_code, 200)

    def test_restaurant_detail_view(self):
        detail_url = reverse("restaurant-detail", kwargs={"restaurant_id":self.restaurant_1.id})
        response = self.client.get(detail_url)
        self.assertContains(response, self.restaurant_1.name)
        self.assertContains(response, self.restaurant_1.description)
        self.assertContains(response, self.restaurant_1.logo.url)
        for item in Item.objects.filter(restaurant=self.restaurant_1):
            self.assertContains(response, item.name)
            self.assertContains(response, item.description)
            self.assertContains(response, item.price)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.status_code, 200)

    def test_restaurant_create_view(self):
        create_url = reverse("restaurant-create")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(create_url)
        request.user = self.user
        response1 = restaurant_create(request)
        self.assertEqual(response1.status_code, 200)

        request2 = self.factory.post(create_url, self.restaurant_data)
        request2.user = self.user
        response2 = restaurant_create(request2)
        self.assertEqual(response2.status_code, 302)

    def test_item_create_view(self):
        create_url = reverse("item-create", kwargs={"restaurant_id":self.restaurant_2.id})
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(create_url)
        request.user = self.user
        response1 = item_create(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(create_url)
        request.user = self.user2
        response1 = item_create(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(create_url)
        request.user = self.user3
        response1 = item_create(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 302)

        request = self.factory.post(create_url, self.item_data)
        request.user = self.user2
        response2 = item_create(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response2.status_code, 302)

        detail_url = reverse("restaurant-detail", kwargs={"restaurant_id":self.restaurant_2.id})
        response = self.client.get(detail_url)
        self.assertTrue(Item.objects.filter(restaurant=self.restaurant_2, name="Original Pizza").exists())

    def test_restaurant_update_view(self):
        update_url = reverse("restaurant-update", kwargs={"restaurant_id":self.restaurant_2.id})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(update_url)
        request.user = self.user
        response1 = restaurant_update(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(update_url)
        request.user = self.user2
        response1 = restaurant_update(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 200)

        request = self.factory.get(update_url)
        request.user = self.user3
        response1 = restaurant_update(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 302)

        request2 = self.factory.post(update_url, self.restaurant_data)
        request2.user = self.user
        response2 = restaurant_update(request2, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response2.status_code, 302)

    def test_restaurant_delete_view(self):
        delete_url = reverse("restaurant-delete", kwargs={"restaurant_id":self.restaurant_1.id})
        request = self.factory.get(delete_url)
        request.user = self.user
        response = restaurant_delete(request, restaurant_id=self.restaurant_1.id)
        self.assertEqual(response.status_code, 302)

        delete_url = reverse("restaurant-delete", kwargs={"restaurant_id":self.restaurant_2.id})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)

    def test_signup_view(self):
        signup_url = reverse("signup")

        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(signup_url, self.user_data_1)
        self.assertEqual(response2.status_code, 200)

        response3 = self.client.post(signup_url, self.user_data_2)
        self.assertEqual(response3.status_code, 302)

        response4 = self.client.post(signup_url, self.user_data_3)
        self.assertEqual(response4.status_code, 200)

        response5 = self.client.post(signup_url, self.user_data_4)
        self.assertEqual(response5.status_code, 200)

    def test_signin_view(self):
        signin_url = reverse("signin")
        
        response = self.client.get(signin_url)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(signin_url, self.user_data_1)
        self.assertEqual(response2.status_code, 302)

        response2 = self.client.post(signin_url, self.user_data_2)
        self.assertEqual(response2.status_code, 200)

        response2 = self.client.post(signin_url, self.user_data_3)
        self.assertEqual(response2.status_code, 200)

        response2 = self.client.post(signin_url, self.user_data_4)
        self.assertEqual(response2.status_code, 200)

    def test_signout_view(self):
        signout_url = reverse("signout")
        response = self.client.get(signout_url)
        self.assertEqual(response.status_code, 302)


class RestaurantFormTestCase(TestCase):
    def test_valid_form(self):
        name = "Some random restaurant"
        description = "Some random description"
        opening_time = "12:15"
        closing_time = "10:15"
        logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
        data = {
            'name':name,
            'description': description,
            'opening_time': opening_time,
            'closing_time': closing_time,
            'logo': logo,
        }
        form = RestaurantForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('name'), name)
        self.assertEqual(form.cleaned_data.get('description'), description)

    def test_invalid_form(self):
        name = "Some restaurant"
        description = "Some random description"
        data = {
            'name':name,
            'description': description,
        }
        form = RestaurantForm(data=data)
        self.assertFalse(form.is_valid())

class ItemFormTestCase(TestCase):
    def test_valid_form(self):
        name = "A Pizza Shop"
        description = "Best pizza shop in the neighbourhood."
        price = 1.750
        data = {
            'name':name,
            'description': description,
            'price': price,
        }
        form = ItemForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('name'), name)
        self.assertEqual(form.cleaned_data.get('description'), description)
        self.assertEqual(form.cleaned_data.get('price'), price)

    def test_invalid_form(self):
        name = "A Pizza Shop"
        description = "Best pizza shop in the neighbourhood."
        price = 1.750
        data = {
            'name':name,
            'description': description,
        }
        data2 = {
            'name':name,
            'price': price,
        }
        data3 = {
            'price':price,
            'description': description,
        }
        form = ItemForm(data=data)
        form2 = ItemForm(data=data2)
        form3 = ItemForm(data=data3)
        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())

class AuthFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
        )
        self.user_data_1 = {
            "username": "bob",
            "password": "adminadmin",
        }
        self.user_data_2 = {
            "username": "billy",
            "password": "adminadmin",
        }
        self.user_data_3 = {
            "username": "bob",
            "password": "",
        }
        self.user_data_4 = {
            "username": "",
            "password": "somepassword",
        }

    def test_valid_signin_form(self):
        form = SigninForm(data=self.user_data_1)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('username'), self.user_data_1['username'])
        self.assertEqual(form.cleaned_data.get('password'), self.user_data_1['password'])

    def test_invalid_signin_form(self):
        form = SigninForm(data=self.user_data_3)
        self.assertFalse(form.is_valid())
        form = SigninForm(data=self.user_data_4)
        self.assertFalse(form.is_valid())

    def test_valid_signup_form(self):
        form = SignupForm(data=self.user_data_2)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], self.user_data_2['username'])
        self.assertEqual(form.cleaned_data.get('password'), self.user_data_2['password'])

    def test_invalid_signup_form(self):
        form = SignupForm(data=self.user_data_1)
        self.assertFalse(form.is_valid())
        form = SignupForm(data=self.user_data_3)
        self.assertFalse(form.is_valid())
        form = SignupForm(data=self.user_data_4)
        self.assertFalse(form.is_valid())