from django import forms

from .models import Stock


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            'stock',
            'period'
        ]

    def clean_stock(self, *args, **kwargs):
        stock= self.cleaned_data['stock']
        if stock.isupper():
            return stock
        else:
            raise forms.ValidationError("Use Caps as stock names.")
    
    def clean_period(self, *args, **kwargs):
        period = self.cleaned_data['period']
        if period < 366:
            return period
        else:
            raise forms.ValidationError("Period cannot exceed 365.")

class FindForm(forms.Form):
    stock = forms.CharField(max_length=20,
    widget=forms.TextInput(attrs={'style': 'width: 100px', 
                            'placeholder': 'eg: AAPL'}))
    lower_day = forms.IntegerField(initial=2,
     widget=forms.TextInput(attrs={'style': 'width: 40px'}))
    lowest_day = forms.IntegerField(initial=2,
     widget=forms.TextInput(attrs={'style': 'width: 40px'}))
    lower_control = forms.BooleanField(required=False)
    lowest_control = forms.BooleanField(required=False)
    allow_duplicates = forms.BooleanField(required=False)

    def clean_lower_day(self, *args, **kwargs):
        lower_day = self.cleaned_data['lower_day']
        if lower_day  > 0:
            return lower_day
        else:
            raise forms.ValidationError("Lower_day needs to be positive.")
    
    def clean_lowest_day(self, *args, **kwargs):
        lowest_day = self.cleaned_data['lowest_day']
        if lowest_day > 0:
            return lowest_day
        else:
            raise forms.ValidationError("Lowest_day needs to be positive.")

class DetailForm(forms.Form):
    days = forms.IntegerField(initial=8, widget=forms.TextInput(attrs={'style': 'width: 50px'}))

    def clean_days(self, *args, **kwargs):
        days = self.cleaned_data['days']
        if days > 0:
            return days
        else:
            raise forms.ValidationError("Days needs to be positive.")

