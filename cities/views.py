from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, FloatField
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CityForm, ImageForm
from .models import City, ImageCity


# Create your views here.
@staff_member_required(login_url='/accounts/login/')
def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST or None, request.FILES)
        if form.is_valid():
            city = form.save(commit=False)
            city.name = form.cleaned_data['name']
            city.title = form.cleaned_data['title']
            city.description = form.cleaned_data['description']
            city.copertina = form.cleaned_data['copertina']
            city.is_active = form.cleaned_data['is_active']
            city.ip = request.META.get('REMOTE_ADDR')
            city.user = request.user
            city.save()
            messages.add_message(request, messages.SUCCESS, 'City added successufy.', extra_tags="success")
            return redirect('pages:cities_dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = CityForm()
    return render(request, 'dashboard/city/add_city.html', {'form': form})


@staff_member_required(login_url='/accounts/login/')
def modify_city(request, city_id):
    city = get_object_or_404(City, id=city_id, user=request.user)
    if request.method == "POST":
        form = CityForm(request.POST or None, request.FILES, instance=city)
        if form.is_valid():
            city = form.save(commit=False)
            city.name = form.cleaned_data['name']
            city.title = form.cleaned_data['title']
            city.description = form.cleaned_data['description']
            city.copertina = form.cleaned_data['copertina']
            city.is_active = form.cleaned_data['is_active']
            city.ip = request.META.get('REMOTE_ADDR')
            city.user = request.user
            city.save()
            messages.add_message(request, messages.SUCCESS, 'City update successufy.', extra_tags="success")
            return redirect('pages:cities_dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = CityForm(instance=city)
    return render(request, 'dashboard/city/update_city.html', {'form': form, 'city': city})


@staff_member_required(login_url='/accounts/login/')
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id, user=request.user)
    if request.method == "POST":
        city.delete()
        messages.add_message(request, messages.SUCCESS, 'City deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:cities_dashboard')


@staff_member_required(login_url='/accounts/login/')
def add_image_city(request, city_id):
    city = get_object_or_404(City, id=city_id, user=request.user)
    if request.method == "POST":
        form = ImageForm(request.POST or None, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.image = form.cleaned_data['image']
            image.alt_text = form.cleaned_data['alt_text']
            image.is_active = form.cleaned_data['is_active']
            image.ip = request.META.get('REMOTE_ADDR')
            image.city = city
            image.user = request.user
            image.save()
            messages.add_message(request, messages.SUCCESS, 'Image added successufy.', extra_tags="success")
            return redirect('cities:add_image_city', city.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ImageForm()
    return render(request, 'dashboard/city/add_image_city.html', {'city': city, 'form': form, })


@staff_member_required(login_url='/accounts/login/')
def delete_image_city(request, image_id):
    image = get_object_or_404(ImageCity, id=image_id, user=request.user)
    if request.method == "POST":
        image.delete()
        messages.add_message(request, messages.SUCCESS, 'Image deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('cities:add_image_city', image.city.id)


@staff_member_required(login_url='/accounts/login/')
def modify_image_city(request, image_id):
    image = get_object_or_404(ImageCity, id=image_id, user=request.user)
    if request.method == "POST":
        form = ImageForm(request.POST or None, request.FILES, instance=image)
        if form.is_valid():
            image = form.save(commit=False)
            image.image = form.cleaned_data['image']
            image.alt_text = form.cleaned_data['alt_text']
            image.is_active = form.cleaned_data['is_active']
            image.ip = request.META.get('REMOTE_ADDR')
            image.user = request.user
            image.save()
            messages.add_message(request, messages.SUCCESS, 'Image modifidy successufy.', extra_tags="success")
            return redirect('cities:add_image_city', image.city.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ImageForm(instance=image)
    return render(request, 'dashboard/city/update_image_city.html', {'image': image, 'form': form})


@staff_member_required(login_url='/accounts/login/')
def staff_city_status(request, city_id):
    city = get_object_or_404(City, id=city_id, user=request.user)
    if request.method == "POST":
        if city.is_active is False:
            city.is_active = True
        else:
            city.is_active = False
        city.save(update_fields=['is_active'])
        return redirect('pages:cities_dashboard')


def city_page(request, slug):
    city = get_object_or_404(City.cities.select_related('user').prefetch_related('city_images', 'city_attractions'),
                             slug=slug, is_active=True)
    images = city.city_images.filter(is_active=True)
    attractions = city.city_attractions.filter(is_active=True).annotate(
            review_number=Count('review_attraction', filter=Q(is_active=True)),
            review_avg=Avg('review_attraction__rating', filter=Q(is_active=True), output_field=FloatField())
        )
    context = {
        'city': city,
        'images': images,
        'attractions': attractions,
    }
    return render(request, 'city/city_page.html', context)


def city_all(request):
    city_list = City.cities.cities_active()
    paginator = Paginator(city_list, 6)  # Show 1 contacts per page.

    page_number = request.GET.get('page')
    cities = paginator.get_page(page_number)

    context = {
        'section': 'list_of_cities',
        'cities': cities,
    }
    return render(request, 'city/cities.html', context)
