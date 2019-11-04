from django.shortcuts import render
from django import views
from .forms import DummyForm


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
