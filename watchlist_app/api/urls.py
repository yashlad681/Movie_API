from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views  import ( movie_details, movie_list)
from watchlist_app.api.views  import (  UserReview, WatchListAV,WatchDetailAV, WatchListGV,
StreamPlatformAV,StreamPlatformVS,
StreamPlatformDetailAV,ReviewList,ReviewDetail,ReviewCreate )


router = DefaultRouter()
streamplatform_list = StreamPlatformVS.as_view({'get': 'list'})
streamplatform_detail = StreamPlatformVS.as_view({'get': 'retrieve'})
router.register('stream',StreamPlatformVS,basename='streamplatform')

urlpatterns = [

    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view() , name='movie-details'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),

    path('',include(router.urls)),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    
    path('<int:pk>/review_create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),  
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    
    path('reviews/', UserReview.as_view(), name='user-review-detail'),
    
    
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
  
]
