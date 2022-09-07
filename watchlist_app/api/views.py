from rest_framework.response import Response
# from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from watchlist_app.api.pagination import WatchListCPagination, WatchListLOPagination, WatchListPagination
from watchlist_app.api.serializers import ReviewSerializer, WatchListSerializer,StreamPlatformSerializer
from watchlist_app.models import WatchList,StreamPlatform,Review
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from watchlist_app.api.permissions import  IsAdminOrReadOnly,IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)   #only happens with foreign key and if we are trying to use it as something  
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)   


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk') #jis movie ka review dena he uska pk lenge and add karenge use net step me watchlist me
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if review_queryset.exists():                                          # condition so that same user doesnt review one movie twice
            raise ValidationError("You have already reviewed this movie!")
        print(serializer.validated_data)
        if watchlist.number_rating == 0:
            watchlist.avg_rating  = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']  ) / 2
        print(serializer.validated_data)
        watchlist.number_rating =  watchlist.number_rating + 1
        watchlist.save()        

        serializer.save(watchlist=watchlist,review_user=review_user)     # watchlist is basically that particular movie on that particlar pk

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']    

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer  
    permission_classes = [IsReviewUserOrReadOnly]  
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'





# -------------------------------------Mixins-------------------------------------
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# -----------------------------Model Viewset---------------------------------
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]



# -----------------------------Viewset---------------------------------

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self,request) :
#         serializer = StreamPlatformSerializer(data=request.data)  
#         if serializer.is_valid(): 
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)       

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
        return Response(serializer.data)

    def post(self,request) :
        serializer = StreamPlatformSerializer(data=request.data)  
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)  

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating'] 


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]   #admin can edit rest every1 can read only

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self,request) :
        serializer = WatchListSerializer(data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
           return Response(serializer.errors)            

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]  #is view me kitno ko apply hota he ye permission_classes

    def get(self, request,pk):
        try:
            movie  = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)    
        serializer = WatchListSerializer(movie)
        return Response(serializer.data) 

    def put(self,request,pk):
        movie  = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       

    def delete(self,request,pk):
        movie  = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)                   
            
















# ------------------------------FBV--------------------------------

# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':  
#         serializer = MovieSerializer(data=request.data)  
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#            return Response(serializer.errors)    

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request,pk):

#     if request.method == 'GET':
#         try:
#             movie  = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)    
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data) 

#     if request.method == 'PUT':
#         movie  = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


#     if request.method == 'DELETE':
#         movie  = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

