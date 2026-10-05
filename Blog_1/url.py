from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # Primeira página: lista todos os posts (ex: ://meusite.com)
    path('', views.post_list, name='post_list'),
    
    # Segunda página: detalhe de um post específico (ex: ://meusite.com1/ ou /slug-do-post/)
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'), 
    path(
        'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
