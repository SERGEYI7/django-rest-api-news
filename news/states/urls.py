from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from states import views

urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='get_authors_with_params'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='get_authors_with_pk'),
    path('categories/', views.CategoryList.as_view(), name='get_categories_with_params'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='get_categories_with_pk'),
    path('tags/', views.TagList.as_view(), name='get_tags_with_params'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='get_tags_with_pk'),
    path('states/', views.StateList.as_view(), name='get_states_with_params'),
    path('states/<str:nm>=<str:pk>/', views.StateDetail.as_view(), name='get_states_with_pk')
]

urlpatterns = format_suffix_patterns(urlpatterns)