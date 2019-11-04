from django import forms


class DummyForm(forms.Form):
    text = forms.CharField(label='Отзыв', min_length=3, max_length=10)
    grade = forms.IntegerField(label='Оценка', min_value=1, max_value=10)
    image = forms.FileField(label='Фото', required=True)

    def clean_text(self):
        text = self.cleaned_data['text']
        if 'abc' not in text:
            raise forms.ValidationError('Вы не о том пишите')

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return text
