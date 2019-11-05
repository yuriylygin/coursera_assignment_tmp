from django.shortcuts import render
from django import views
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json

from marshmallow import ValidationError as MarshmallowError

from .schemas import REVIEW_SCHEMA
from .forms import DummyForm, ReviewSchema

from pdb import set_trace


class FormDummyView(views.View):

    def get(self, request):
        form = DummyForm()
        # print(form.__dict__)
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = DummyForm(request.POST, request.FILES)
        if form.is_valid():
            context = form.cleaned_data
            content = context.get('image').read()
            context['content'] = content
            return render(request, 'form.html', context=context)
        else:
            return render(request, 'error.html', context={'error': form.errors})


@method_decorator(csrf_exempt, name='dispatch')
class SchemaView(views.View):

    def post(self, request):
        try:
            # from pdb import set_trace; set_trace()
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA)
            return JsonResponse(document, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except ValidationError as exc:
            return JsonResponse({'error': exc.message}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MarshView(views.View):

    def post(self, request):
        try:
            # from pdb import set_trace; set_trace()
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            set_trace()
            data = schema.load(document)
            set_trace()
            return JsonResponse(data.data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except MarshmallowError as exc:
            return JsonResponse({'error': exc.normalized_messages()}, status=400)
