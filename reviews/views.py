from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from places.models import Attractions
from reviews.forms import ReviewForm, ReportReviewForm
from .models import ReviewRating


# Create your views here.
@login_required
def attraction_review(request, pk, slug):
    attraction = get_object_or_404(Attractions, id=pk, slug=slug, is_active=True)
    last_reviews = attraction.review_attraction.select_related('attraction', 'user').prefetch_related(
        'users_vote').filter(status="AP")[:3]
    user_number_reviews = attraction.review_attraction.filter(user=request.user).exists()
    if request.method == 'POST' and user_number_reviews is False:
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(commit=False)
            review.subject = form.cleaned_data['subject']
            review.review = form.cleaned_data['review']
            review.rating = form.cleaned_data['rating']
            review.ip = request.META.get('REMOTE_ADDR')
            review.attraction = attraction
            review.user = request.user
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Your review will be published in a few minutes.',
                                 extra_tags='success')
            return redirect('places:attraction_page', attraction.slug)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_page.html', {'attraction': attraction, 'last_reviews': last_reviews,
                                                        'form': form, 'user_number_reviews': user_number_reviews})


@login_required
def modify_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST or None, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.subject = form.cleaned_data['subject']
            review.review = form.cleaned_data['review']
            review.rating = form.cleaned_data['rating']
            review.ip = request.META.get('REMOTE_ADDR')
            review.user = request.user
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review update successufy.', extra_tags="success")
            return redirect('pages:reviews_dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ReviewForm(instance=review)
    return render(request, 'dashboard/reviews/update_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:reviews_dashboard')


@staff_member_required(login_url='/accounts/login/')
def staff_review_ap(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id)
    if request.method == "POST":
        review.status = "AP"
        review.save(update_fields=['status'])
        messages.add_message(request, messages.SUCCESS, 'Review updated successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:reviews_dashboard')


@staff_member_required(login_url='/accounts/login/')
def staff_review_re(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id)
    if request.method == "POST":
        review.status = "RE"
        review.save(update_fields=['status'])
        messages.add_message(request, messages.SUCCESS, 'Review updated successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:reviews_dashboard')


@staff_member_required(login_url='/accounts/login/')
def staff_review_wa(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id)
    if request.method == "POST":
        review.status = "WA"
        review.save(update_fields=['status'])
        messages.add_message(request, messages.SUCCESS, 'Review updated successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:reviews_dashboard')


@login_required
def report_this_review(request, pk):
    this_review = get_object_or_404(ReviewRating.user_reviews.reviews_approved(), id=pk, status="AP")
    if request.method == 'POST' and this_review.user != request.user:
        form = ReportReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(commit=False)
            review.subject = form.cleaned_data['subject']
            review.description = form.cleaned_data['description']
            review.ip = request.META.get('REMOTE_ADDR')
            review.review = this_review
            review.user = request.user
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Your report has been sent successfully.',
                                 extra_tags='success')
            return redirect('places:attraction_page', this_review.attraction.slug)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ReportReviewForm()
    return render(request, 'reviews/review_report.html', {'review': this_review, 'form': form, })


@login_required
def add_review_vote(request, pk):
    this_review = get_object_or_404(ReviewRating, id=pk, status="AP")
    if this_review.user != request.user:
        if this_review.users_vote.filter(id=request.user.id).exists():
            this_review.users_vote.remove(request.user)
            messages.add_message(request, messages.ERROR, f"You unvoted {this_review.subject}", extra_tags="danger")
        else:
            this_review.users_vote.add(request.user)
            messages.add_message(request, messages.SUCCESS, f"You voted {this_review.subject}")
    else:
        messages.add_message(request, messages.ERROR, "You can't vote your review.", extra_tags="danger")
    return redirect('places:attraction_page', this_review.attraction.slug)
