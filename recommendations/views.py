from django.shortcuts import render
import time
# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from recommendations.serializers import GameRecommendationSerializer
from .services.new_user_rec import new_user_recommendations
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.paginator import Paginator
from rest_framework.response import Response
from games.models import WishList, GameStatus, UserLibrary, RatingCategory, RatingType, GameOverallRating, GameCategoryRating

from .serializers import RecommendationSerializer
from .services.existing_user_rec import existing_user_recommendations
from .services.game_recommendation import get_recommendations
class RecommendationPagination(PageNumberPagination):
    page_size= 10

# class NewUserGameRecommendationAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     pagination_class = RecommendationPagination
#     renderer_classes = [HTMLFormRenderer]
#     serializer_class = GameRecommendationSerializer
#     def get_queryset(self):
#         return new_user_recommendations(self.request.user)

# class NewUserGameRecommendationAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [TemplateHTMLRenderer]
#     serializer_class = GameRecommendationSerializer
#     template_name = "recommendations/new_user_rec.html"
#     def get(self, request):
#         games = new_user_recommendations(request.user)
#         paginator = Paginator(games, 20)
#         page_number = request.GET.get("page")
#         games_page = paginator.get_page(page_number)
#         wishlist_games=WishList.objects.filter(user=request.user).values_list("game_id", flat=True)
#         # library
#         statuses= GameStatus.objects.all()
#         library_games= {
#             lg.game_id: lg for lg in UserLibrary.objects.filter(user=request.user) 
#         }
#         # rating
#         rating_types= RatingType.objects.all()
#         overall_rating = {
#             r.game_id: r.rating_type_id for r in GameOverallRating.objects.filter(user=request.user)
#         }
#         categories= RatingCategory.objects.all()
#         # category_rating= {
#         #     (r.game_id, r.category_id): r.rating_type_id for r in GameCategoryRating.objects.filter(user=request.user)
#         # }
#         category_rating = {}
#         for r in GameCategoryRating.objects.filter(user=request.user):
#             category_rating.setdefault(r.game_id, {})[r.category_id] = r.rating_type_id
#         return Response(
#                   {"games":games_page,
#                    "wishlist_games": wishlist_games,
#                    "statuses":statuses,
#                    "library_games":library_games,
#                    "rating_types":rating_types,
#                    "overall_rating":overall_rating,
#                    "category_rating":category_rating,
#                    "categories":categories,
#                    })

# View for both new and existing user:
class GameRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = RecommendationSerializer
    template_name = "recommendations/game_recommendation.html"
    def get(self, request):
        recs = get_recommendations(request.user, limit=100)
        # Normalize structure
        if isinstance(recs, list):
            # existing user case
            games = [item["game"] for item in recs]
        else:
            # new user case (QuerySet)
            games = recs
        paginator = Paginator(games, 20)
        page_number = request.GET.get("page")
        games_page = paginator.get_page(page_number)
        #wishlist
        wishlist_games=WishList.objects.filter(user=request.user).values_list("game_id", flat=True)
        # # library
        # statuses= GameStatus.objects.all()
        # library_games= {
        #     lg.game_id: lg for lg in UserLibrary.objects.filter(user=request.user) 
        # }
        # # rating
        # rating_types= RatingType.objects.all()
        # overall_rating = {
        #     r.game_id: r.rating_type_id for r in GameOverallRating.objects.filter(user=request.user)
        # }
        # categories= RatingCategory.objects.all()
        # # category_rating= {
        # #     (r.game_id, r.category_id): r.rating_type_id for r in GameCategoryRating.objects.filter(user=request.user)
        # # }
        # category_rating = {}
        # for r in GameCategoryRating.objects.filter(user=request.user):
        #     category_rating.setdefault(r.game_id, {})[r.category_id] = r.rating_type_id
        return Response(
                  {"games":games_page,
                   "wishlist_games": wishlist_games,
                #    "statuses":statuses,
                #    "library_games":library_games,
                #    "rating_types":rating_types,
                #    "overall_rating":overall_rating,
                #    "category_rating":category_rating,
                #    "categories":categories,
                   })

# #### existing users API view:
class ExistingUserRecommendationsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RecommendationPagination

    def get(self, request):
        start= time.time()
        recs = existing_user_recommendations(request.user, limit=100)

        rec_objs = []
        for r in recs:
            game = r["game"]
            game.score = r["score"]
            game.explanations = r["explanations"]
            rec_objs.append(game)

        serializer = RecommendationSerializer(rec_objs, many=True)
        end=time.time()
        print("time", end - start)
       
        return Response(serializer.data)
    
    

