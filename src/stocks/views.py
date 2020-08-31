from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse

import yfinance as yf
from datetime import date, time, datetime

from .forms import StockForm, FindForm, DetailForm
from .models import Stock, DetailPage, Price
from .utils import stock_find_single, create_stock_bar_chart
# Create your views here.

def stock_create_view(request):
    form = StockForm(request.POST or None)
    stk_name = ""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            stk_name = form.cleaned_data.get('stock')
            period = form.cleaned_data.get('period')
            period = '{}d'.format(period)
            stk = yf.Ticker(stk_name)
            historical_data = stk.history(period=period)
            for index, row in historical_data.iterrows():
                dt = datetime.combine(row.name.date(), time())
                p_args = {
                    'stock' : form.instance,
                    'open_price': row['Open'],
                    'close_price': row['Close'],
                    'high_price': row['High'],
                    'low_price': row['Low'],
                    'date' : dt
                }
                p = Price(**p_args)
                p.save()
            return redirect('../')
        else:
            stk_name = request.POST['stock']
    context = {
        'form': form,
        'stk_name': stk_name,
    }
    return render(request, "stocks/stocks_create.html", context)

def stock_find_view(request):
    stock_find_args = {
        'lower_day' : 2,
        'lowest_day' : 2,
        'lower_control' : False,
        'lowest_control' : False,
        'allow_duplicates' : False
    }
    form = FindForm(request.POST or None)
    pattern_found = []
    exist_error = []
    if request.method == "POST":
        if (form.is_valid()):
            stk_name = form.cleaned_data['stock']
            stock_find_args = {
                'lower_day': form.cleaned_data['lower_day'],
                'lowest_day': form.cleaned_data['lowest_day'],
                'lower_control': form.cleaned_data['lower_control'],
                'lowest_control': form.cleaned_data['lowest_control'],
                'allow_duplicates': form.cleaned_data['allow_duplicates']
            }
            try:
                pattern_found = stock_find_single(stk_name, **stock_find_args)
                DetailPage.objects.all().delete()
                for row in pattern_found:
                    id_list = row[3]
                    detail = DetailPage(stk_name=stk_name)
                    detail.save()
                    for id_ in id_list:
                        price_obj = Price.objects.get(id=id_)
                        price_obj.details = detail
                        price_obj.save()
                    row.append(detail.id)
            except:
                DetailPage.objects.all().delete()
                form = FindForm()
                exist_error = [ "DNE" ]
    else:
        DetailPage.objects.all().delete()
        form = FindForm()
    context = {
        'form' : form,
        'found' : pattern_found,
        'exist_error' : exist_error
    }
    return render(request, 'stocks/stocks_find.html', context)

def stock_detail_view(request, id):
    detail_obj = get_object_or_404(DetailPage, id=id)
    detail_prices = detail_obj.get_prices()
    form = DetailForm(request.POST or None)
    days = 8
    if (request.method == 'POST'):
        if (form.is_valid()):
            days = form.cleaned_data['days']
    dates = list(detail_prices.values_list('date', flat=True))
    y_close = list(detail_prices.values_list('close_price', flat=True))
    y_open = list(detail_prices.values_list('open_price', flat=True))
    # for i in range(0, days):
    #     dates.append(dates[:-1] + timedelta(days=1))
    #     y_close.append()
    bar_plot = create_stock_bar_chart(dates=dates, y_open=y_open, y_close=y_close, days=days)

    context = {
        'form' : form,
        'data' : bar_plot
    }
    return render(request, 'stocks/stocks_detail.html', context)
