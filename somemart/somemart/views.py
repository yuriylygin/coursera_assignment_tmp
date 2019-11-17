import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Item, Review

from django.core.exceptions import ObjectDoesNotExist

from django.forms.models import model_to_dict

from marshmallow import Schema, fields
from marshmallow.validate import Range, Length
from marshmallow import ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from basicauth import encode, decode
from django.contrib.auth import authenticate

from base64 import b64decode

from pdb import set_trace


class IntFromStr(fields.Field):
    def _deserialize(self, value, attr, obj):
        try:
            return int(value)
        except ValueError:
            raise ValidationError('Value can not be transformed to int')


class ItemSchema(Schema):
    title = fields.Str(validate=Length(1, 64), required=True)
    description = fields.Str(validate=Length(1, 1024), required=True)
    price = IntFromStr(validate=Range(1, 1000000), required=True)


class ReviewSchema(Schema):
    text = fields.Str(validate=Length(1, 1024), required=True)
    grade = IntFromStr(validate=Range(1, 10), required=True)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        if auth is None:
            return HttpResponse(status=401)
        else:
            # user_encoded = auth.split(' ')[1]
            # login, password = b64decode(user_encoded).decode().split(':')
            login, password = decode(auth)
            user = authenticate(username=login, password=password)
            if user is None:
                return HttpResponse(status=401)
            elif not user.is_staff:
                return HttpResponse(status=403)
            else:
                try:
                    document = json.loads(request.body)
                    schema = ItemSchema(strict=True)
                    data = schema.load(document)
                    item = Item.objects.create(**data.data)
                    data.data['id'] = item.id
                    # data.data['login'] = login
                    return JsonResponse(data.data, status=201)

                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON'}, status=400)

                except ValidationError as exc:
                    return JsonResponse({'error': exc.normalized_messages()}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            data = schema.load(document)
            item = Item.objects.get(pk=item_id)
            data.data['item'] = item
            review = Review.objects.create(**data.data)
            response = {'id': review.id}
            return JsonResponse(response, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except ValidationError as exc:
            return JsonResponse({'error': exc.normalized_messages()}, status=400)

        except Item.DoesNotExist:
            # set_trace()
            return JsonResponse({'error': 'Item matching query does not exist.'}, status=404)

        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review matching query does not exist.'}, status=404)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            reviews = Review.objects.filter(item__id=item.id).order_by('-id')[:5]
            response = model_to_dict(item)
            response['reviews'] = [model_to_dict(review) for review in reviews]
            return JsonResponse(response, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Item.DoesNotExist:
            # set_trace()
            return JsonResponse({'error': 'Item matching query does not exist.'}, status=404)

        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review matching query does not exist.'}, status=404)
