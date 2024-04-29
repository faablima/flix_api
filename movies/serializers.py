from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie

from genres.serializers import GenreSerializer
from actors.serializers import ActorSerializer

class MovieSerializer(serializers.ModelSerializer):
    
  class Meta:
    model = Movie
    fields = '__all__'  
    
  def validate_release_data(self, value):
    if value.year < 1800:
      raise serializers.ValidationError('A data de lançamento não pode ser anterior a 1990.')
    return value
  
  def validate_resume(self, value):
    if len(value) > 500:
      raise serializers.ValidationError('Resumo não deve ser maior do que 200 caracteres.')
    return value

class MovieListDetailSerializer(serializers.ModelSerializer):
  actors = ActorSerializer(many=True)
  genre = GenreSerializer()
  rate = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = Movie
    fields = ['id', 'title', 'genre', 'actors', 'release_data', 'rate', 'resume']
  
  def get_rate(self, obj):
    rating_result = obj.reviews.aggregate(average_rating=Avg('stars'))
    average_rating = rating_result.get('average_rating', None)
    
    if average_rating is not None:
      return round(average_rating, 2)
    return None