from django import forms


class RatingForm(forms.Form):

    premium_name = forms.CharField(max_length=200)
    class_name = forms.MultipleChoiceField(choices=('A', 'B', 'C'))
    rate = forms.CharField() # will take input as string which will be a dictionary like:
    # {'rate1': value1, 'rate2': value2 ...}
    exposure_unit = forms.IntegerField()
    state = forms.CharField()
    user = forms.CharField(max_length=200)