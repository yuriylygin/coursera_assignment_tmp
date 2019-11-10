import json
from itertools import product

from django.db.models import Count, Max, Min
from somemart.models import Item, Review
from pdb import set_trace


class TestViews(object):

    correct = dict(title=['x', 'x'*64],
                   description=['x', 'x'*1024],
                   price=[1, 1000000, '1', '1000000'])

    fail = dict(title=['', 'x'*65],
                description=['', 'x' * 1025],
                price=[0, 1000001, '', '0', '1000001'])

    def test_post_item(self, client, db):
        """/api/v1/goods/ (POST) сохраняет товар в базе."""
        url = '/api/v1/goods/'

        for title, description, price in product(self.correct['title'], self.correct['description'], self.correct['price']):
            data = json.dumps({
                'title': title,
                'description': description,
                'price': price
            })
            response = client.post(url, data=data, content_type='application/json')
            assert response.status_code == 201
            document = response.json()
            # Объект был сохранен в базу
            item = Item.objects.get(pk=document['id'])
            assert item.title == title
            assert item.description == description
            assert item.price == int(price)

        for title, description, price in product(self.fail['title'], self.correct['description'], self.correct['price']):
            data = json.dumps({
                'title': title,
                'description': description,
                'price': price
            })
            response = client.post(url, data=data, content_type='application/json')
            assert response.status_code == 400

        print(Item.objects.aggregate(Count('id')))
        print(Item.objects.aggregate(Max('id')))
        print(Item.objects.aggregate(Min('id')))

    def test_post_review(self, client, db):
        d = Item.objects.aggregate(Count('id'))
        print(d)
        pass

