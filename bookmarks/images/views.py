import redis
from actions.utils import create_action
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image

# connect to Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


# defines views for the images app
@login_required
def image_create(request):
    """image_create creates a view for authenticated users to store images on the site.

    Args:
        request (GET): gets the http response to create an instance of the form
        request (POST): validates the form

    Returns:
        object: Image object is saved to the database
    """
    if request.method == "POST":
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "bookmarked image", new_image)
            messages.success(request, "Image added successfully!")
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(
        request, "images/image/create.html", {"section": "images", "form": form}
    )


def image_detail(request, id, slug):
    """image_detail simple view that displays an image

    Args:
        request (Image): :model:`Images.image`
        id (Integer): id of image
        slug (String): url

    Returns:
        string: url images/image/detail.html
        dict: section, images, image
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr(f"image:{image.id}:views")
    # increment image ranking by 1
    r.zincrby("image_ranking", 1, image.id)
    return render(
        request,
        "images/image/detail.html",
        {
            "section": "images",
            "image": image,
            "total_views": total_views,
        },
    )


@login_required
@require_POST
def image_like(request):
    """image_like function-based view performs the 'like' and 'unlike' actions on images
    for logged in users.

    Args:
        request (POST): only accepts POST http requests, and it expects the image_id and
        action parameters.

    Returns:
        HttpResponseNotAllowed object (status code 405): if http request is not done via
        POST
        Http response : converts given object into JSON
    """
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request):
    """image_list is a view listing all the bookmarked images on the site. It uses
    JavaScript requests for infinite scroll functionality. This view handles both
    standard and AJAX infinite scroll pagination. A QuerySet is created to retrieve all
    images in the database, and then the paginator gets 8 images per page.

    Args:
        request (AJAX, GET): requests more images when scrolling to the bottom

    Returns:
        HttpResponse: if there are more images to load, the next page appears below
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # if this is an AJAX request and the page is out of range
            # return an empty page
            return HttpResponse("")
        # if the page is out of range, return last page of results
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            "images/image/list_images.html",
            {"section": "images", "images": images},
        )
    return render(
        request,
        "images/image/list.html",
        {"section": "images", "images": images},
    )


@login_required
def image_ranking(request):
    """image_ranking displays the ranking of the most viewed images. Redis returns all
    elements in the sorted set, retrieves elements ordered by descending score, and
    slices the results to get the 10 top ranking elements. image_ranking_ids is a list
    of returned image IDs, list() forces the QuerySet execution to retrieve the image
    objects connected to the IDs. The top 10 Image objects are sorted by their ranking.

    Args:
        request (set): Redis works with all the images as a sorted set

    Returns:
        HttpResponse: shows the top 10 ranked image objects
    """
    # get image ranking dictionary
    image_ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get the most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        "images/image/ranking.html",
        {"section": "images", "most_viewed": most_viewed},
    )
