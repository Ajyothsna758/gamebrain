from rest_framework.throttling import UserRateThrottle
class RecommendationThrottle(UserRateThrottle):
    rate= "30/min"