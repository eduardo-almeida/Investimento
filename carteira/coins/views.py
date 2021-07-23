from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CoinForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from coins.models import Coin


@login_required
def coinList(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')

    fixa = Coin.objects.filter(modalidade='fixa').count()
    variavel = Coin.objects.filter(modalidade='variavel').count()
    cripto = Coin.objects.filter(modalidade='cripto').count()

    if search:
        coins = Coin.objects.filter(nome__icontains=search)
    elif filter:
        coins = Coin.objects.filter(modalidade=filter)
    else:
        coins_list = Coin.objects.all().order_by('-created_at')
        paginator = Paginator(coins_list, 3)
        page = request.GET.get('page')
        coins = paginator.get_page(page)
    return render(request, 'coins/listcoin.html', {'coins': coins, 'fixa': fixa, 'variavel': variavel, 'cripto': cripto})


@login_required
def coinView(request, id):
    coin = get_object_or_404(Coin, pk=id)
    return render(request, 'coins/coin.html', {'coin': coin})


@login_required
def newCoin(request):
    if request.method == 'POST':
        form = CoinForm(request.POST)
        if (form.is_valid()):
            coin = form.save(commit=False)
            coin.user = request.user
            coin.save()
            return redirect('/coinList/')
    else:
        form = CoinForm()
        return render(request, 'coins/addcoin.html', {'form': form})


@login_required
def editCoin(request, id):
    coin = get_object_or_404(Coin, pk=id)
    form = CoinForm(instance=coin)

    if (request.method == 'POST'):
        form = CoinForm(request.POST, instance=coin)
        if (form.is_valid()):
            coin = form.save(commit=False)

            coin.save()
            return redirect('/coinList/')
        else:
            return render(request, 'coins/editcoin.html', {'form': form, 'coin': coin})

    else:
        return render(request, 'coins/editcoin.html', {'form': form, 'coin': coin})


@login_required
def deleteCoin(request, id):
    coin = get_object_or_404(Coin, pk=id)
    coin.delete()
    messages.info(request, "Moeda deletada com sucesso!")
    return redirect('/coinList/')
