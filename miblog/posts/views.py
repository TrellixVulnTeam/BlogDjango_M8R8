from django.utils.http import urlquote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# Create your views here.
from .models import Post
from .forms import PostForm

#paginaciones
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_create(request):

    #permisos de usuario
    if not request.user.is_authenticated:
        raise Http404


    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Tu post ha sdo creado correctamente", extra_tags="primary")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    share_string = urlquote_plus(instance.titulo)
    context = {
        "titulo": instance.titulo,
        "instance": instance,
        "share_string": share_string
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all()#.order_by("-timestamp")
    paginator = Paginator(queryset_list, 6)  # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "titulo": "List",
        "object_list": queryset
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    #permisos de usuario
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Tu post ha sdo modificado correctamente")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "titulo": instance.titulo,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    #permisos de usuario
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Tu post ha sdo eliminado correctamente", extra_tags="primary")
    return redirect("posts:list")

# configuramos las urls paara cada funcion en urls.py de post
