from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Laptop
from .forms import LaptopForm


def home(request):
    laptops = Laptop.objects.all().order_by('-id')
    paginator = Paginator(laptops, 5)

    page_number = request.GET.get('page')
    laptops_page = paginator.get_page(page_number)

    return render(request, 'home.html', {'laptops': laptops_page})


def get_laptop(request, pk):
    laptop = get_object_or_404(Laptop, id=pk)
    return render(request, 'laptop_info.html', {'object': laptop})


def add_laptop(request):
    form = LaptopForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Laptop Added Successfully!")
            return redirect('/laptops')
    return render(request, 'laptop_form.html', {'form': form})


def update_laptop(request, pk):
    laptop = get_object_or_404(Laptop, id=pk)
    form = LaptopForm(request.POST or None, instance=laptop)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Laptop Updated Successfully!")
            return redirect('/laptops')
    return render(request, 'laptop_form.html', {'form': form})


def delete_laptop(request, pk):
    laptop = get_object_or_404(Laptop, id=pk)
    laptop.delete()
    messages.success(request, "Laptop Deleted Successfully!")
    return redirect('/laptops')
