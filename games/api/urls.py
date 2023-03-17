from django.urls import path
from games.api import views as api_views

urlpatterns = [

    # generic view urlleri
    path('developer/', api_views.DeveloperListCreateAPIView.as_view(), name='developer-list'),
    path('developer/<int:pk>', api_views.DeveloperRetrieveUpdateDestroyAPIView.as_view(), name='developer-detail'),
    path('game/', api_views.GameListCreateAPIView.as_view(), name='game-list'),
    path('game/<int:pk>', api_views.GameRetrieveUpdateDestroyAPIView.as_view(), name='game-detail'),

    path('search/developer/<str:query>', api_views.SearchDevelopers.as_view(), name='search-developer'),
    path('search/game/<str:query>', api_views.SearchGames.as_view(), name='search-games')

]
