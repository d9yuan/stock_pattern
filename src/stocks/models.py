from django.db import models

# Create your models here.


class Stock(models.Model):
    stock = models.CharField(max_length=20, unique=True)
    # how many days of data to retrieve
    period = models.IntegerField()
    # returns the QuerySet of all historical data
    #  stored under this stock
    def get_prices(self):
        return self.price_set.all()

class DetailPage(models.Model):
    stk_name = models.CharField(max_length=20, null=True)
    def get_prices(self):
        return self.price_set.all()

class Price(models.Model):
    opts = {'default' : 0,
            'max_digits' : 1000,
            'decimal_places' : 2}
    open_price = models.DecimalField(**opts)
    close_price = models.DecimalField(**opts)
    high_price = models.DecimalField(**opts)
    low_price = models.DecimalField(**opts)
    date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    details = models.ForeignKey(DetailPage, on_delete=models.SET_NULL, null=True, default=None)

 

    
    

