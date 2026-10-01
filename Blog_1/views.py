from django.shortcuts import get_object_or_404, render
from django.http import  Http404
from django.core.paginator import EmptyPage, Paginator,PageNotAnInteger 
from  django.contrib import messages 
from .models import Post

def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts= paginator.page(page_number)
    except PageNotAnInteger:
       
        posts = paginator.page(1)
    except EmptyPage:
        
        posts = paginator.page(paginator.num_pages)
    """if len(posts) <= 1:
        
        messages.warning(request,'Ocorreu um erro para carregar todas as publicações de forma convercional(seguindo o livro.), então, foi usado -objects- no lugar de -published-')
        posts = Post.objects.all()"""
    


    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    try:
        post = get_object_or_404(Post, status= Post.Status.PUBLISHED, 
                        slug=post, publish__year = year,publish__month = month,publish__day = day)
    except Http404:
        post =  get_object_or_404(Post, slug=post)

    return render(request, 'blog/post/detail.html', {'post': post})