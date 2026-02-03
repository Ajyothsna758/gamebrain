from games.models import Game
from rest_framework import serializers

class GameRecommendationSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    platforms = serializers.StringRelatedField(many=True)
    player_perspectives = serializers.StringRelatedField(many=True)
    themes = serializers.StringRelatedField(many=True)
    class Meta:
        model = Game
        fields = ["id", "name", "total_rating", "released", "genres", "platforms", "player_perspectives", "themes", "cover_url"]
        
