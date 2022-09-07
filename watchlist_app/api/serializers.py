from rest_framework import serializers
from watchlist_app.models import Review, WatchList,StreamPlatform




class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')
    # reviews= ReviewSerializer(many=True, read_only=True)
    # len_name = serializers.SerializerMethodField() #Custom attribte to count length

    class Meta:
        model = WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True) #when u add Fk in models this is to be modified
    # watchlist = serializers.StringRelatedField(many=True) 
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='movie-details') 

    class Meta:
        model = StreamPlatform
        fields = "__all__"


# -----------------Commenting validation cause dont need them currently
    # def get_len_name(self, object):
    #     return len(object.name)    

    # def validate(self,data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("Title and description should be different")
    #     else:
    #         return data    

    # def validate_name(self, value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is short.")
    #     return value      

# --------------------------------serializers.Serializer-------------------------------------
# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is short.")
#     return value            

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)    
#         instance.description = validated_data.get('description', instance.description)    
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self,data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Title and description should be different")
#         else:
#             return data    

#     def validate_name(self, value):
#         if len(value)<2:
#             raise serializers.ValidationError("Name is short.")
#         return value            