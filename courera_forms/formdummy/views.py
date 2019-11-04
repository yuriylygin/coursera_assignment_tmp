from django.shortcuts import render
from django.views import View


class FormDummyView(View):

    def get(self, request):
        return render(request, 'form.html', {})

    def post(self, request):
        text = request.POST.get('text')
        grade = request.POST.get('grade')
        content = request.FILES.get('image').read()

        return render(request, 'form.html', context=dict(
            text=text,
            grade=grade,
            content=content,
        ))

