import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import ajax_login_required
from .forms import AttractionsForm, ImageForm
from .models import Attractions, ImageAttractions


# Create your views here.
def attraction_page(request, slug):
    attraction = get_object_or_404(Attractions.attraction.attractions_active(), slug=slug, is_active=True)
    reviews = attraction.review_attraction.filter(status="AP").select_related('attraction', 'user').prefetch_related(
        'users_vote',
    )
    images = attraction.attractions_images.filter(is_active=True)
    context = {
        'attraction': attraction,
        'reviews': reviews,
        'images': images,
    }
    return render(request, 'places/attraction_page.html', context)


def attraction_all(request):
    atractions_list = Attractions.attraction.attractions_active()
    paginator = Paginator(atractions_list, 4)  # Show 1 contacts per page.

    page_number = request.GET.get('page')
    atractions = paginator.get_page(page_number)
    context = {
        'atractions': atractions,
    }
    return render(request, 'places/attractions.html', context)


@ajax_login_required
def attraction_wishlist(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            att_id = data.get('attraction_id')
            attraction = get_object_or_404(Attractions, id=att_id)
            if attraction.users_wishlist.filter(id=request.user.id).exists():
                attraction.users_wishlist.remove(request.user)
                return JsonResponse({'status': False})
            else:
                attraction.users_wishlist.add(request.user)
                return JsonResponse({'status': True})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


@staff_member_required(login_url='/accounts/login/')
def add_attraction(request):
    if request.method == "POST":
        form = AttractionsForm(request.POST or None, request.FILES)
        if form.is_valid():
            attraction = form.save(commit=False)
            attraction.name = form.cleaned_data['name']
            attraction.title = form.cleaned_data['title']
            attraction.city = form.cleaned_data['city']
            attraction.adress = form.cleaned_data['adress']
            attraction.cap = form.cleaned_data['cap']
            attraction.description = form.cleaned_data['description']
            attraction.copertina = form.cleaned_data['copertina']
            attraction.is_active = form.cleaned_data['is_active']
            attraction.ip = request.META.get('REMOTE_ADDR')
            attraction.user = request.user
            attraction.save()
            messages.add_message(request, messages.SUCCESS, 'Attraction added successufy', extra_tags="success")
            return redirect('pages:attractions_dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")

    else:
        form = AttractionsForm()
    return render(request, 'dashboard/attractions/add_attractions.html', {'form': form})


@staff_member_required(login_url='/accounts/login/')
def modify_attraction(request, attraction_id):
    attraction = get_object_or_404(Attractions, id=attraction_id, user=request.user)
    if request.method == "POST":
        form = AttractionsForm(request.POST or None, request.FILES, instance=attraction)
        if form.is_valid():
            attraction = form.save(commit=False)
            attraction.name = form.cleaned_data['name']
            attraction.title = form.cleaned_data['title']
            attraction.city = form.cleaned_data['city']
            attraction.adress = form.cleaned_data['adress']
            attraction.cap = form.cleaned_data['cap']
            attraction.description = form.cleaned_data['description']
            attraction.copertina = form.cleaned_data['copertina']
            attraction.is_active = form.cleaned_data['is_active']
            attraction.ip = request.META.get('REMOTE_ADDR')
            attraction.user = request.user
            attraction.save()
            messages.add_message(request, messages.SUCCESS, 'Attraction added successufy', extra_tags="success")
            return redirect('pages:attractions_dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = AttractionsForm(instance=attraction)
    return render(request, 'dashboard/attractions/modify_attraction.html',
                  {'form': form, 'attraction': attraction})


@staff_member_required(login_url='/accounts/login/')
def delete_attraction(request, attraction_id):
    attraction = get_object_or_404(Attractions, id=attraction_id, user=request.user)
    if request.method == "POST":
        attraction.delete()
        messages.add_message(request, messages.SUCCESS, 'Attraction deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:attractions_dashboard')


@staff_member_required(login_url='/accounts/login/')
def add_image_attraction(request, attraction_id):
    attraction = get_object_or_404(Attractions, id=attraction_id, user=request.user)
    if request.method == "POST":
        form = ImageForm(request.POST or None, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.image = form.cleaned_data['image']
            image.alt_text = form.cleaned_data['alt_text']
            image.is_active = form.cleaned_data['is_active']
            image.ip = request.META.get('REMOTE_ADDR')
            image.attraction = attraction
            image.user = request.user
            image.save()
            messages.add_message(request, messages.SUCCESS, 'Image added successufy.', extra_tags="success")
            return redirect('places:add_image_attraction', attraction.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ImageForm()
    return render(request, 'dashboard/attractions/add_image_attraction.html',
                  {'attraction': attraction, 'form': form, })


@staff_member_required(login_url='/accounts/login/')
def delete_image_attraction(request, image_id):
    image = get_object_or_404(ImageAttractions, id=image_id, user=request.user)
    if request.method == "POST":
        image.delete()
        messages.add_message(request, messages.SUCCESS, 'Image deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('places:add_image_attraction', image.attraction.id)


@staff_member_required(login_url='/accounts/login/')
def modify_image_attraction(request, image_id):
    image = get_object_or_404(ImageAttractions, id=image_id, user=request.user)
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
            return redirect('places:add_image_attraction', image.attraction.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ImageForm(instance=image)
    return render(request, 'dashboard/attractions/modify_image_attraction.html', {'image': image, 'form': form})


@staff_member_required(login_url='/accounts/login/')
def staff_attraction_status(request, attraction_id):
    attraction = get_object_or_404(Attractions, id=attraction_id, user=request.user)
    if request.method == "POST":
        if attraction.is_active is False:
            attraction.is_active = True
        else:
            attraction.is_active = False
        attraction.save(update_fields=['is_active'])
        return redirect('pages:attractions_dashboard')
