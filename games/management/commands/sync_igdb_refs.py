from django.core.management import BaseCommand
from games.models import Genre, IGDBSyncStatus, GameMode, Platform, PlayerPerspective, Franchise, Theme
from games.services.igdb import get_igdb_data
from django.utils.timezone import make_aware, datetime

REFERENCE_TABLES=[
    ("genres",Genre),
    ("game_modes", GameMode),
    ("platforms", Platform),
    ("player_perspectives", PlayerPerspective),
    ("franchises", Franchise),
    ("themes", Theme),
    #("keywords", Keyword),
    #("collections", Collection),
]
ENDPOINT_FIELDS={
    "genres":"id, name, slug",
    "game_modes":"id, name, slug",
    "platforms":"id, name, slug, abbreviation, alternative_name",
    "player_perspectives":"id, name, slug",
    "franchises":"id, name, slug",
    "themes":"id, name, slug",
    # "keywords":"id, name, slug",
    # "collections":"id, name, slug",
}

class Command(BaseCommand):
    help="Sync IGDB reference tables (Genres, platforms, GameModes, PlayerPerspective, Theme, Franchises)"
    def handle(self, *args, **kwargs):
        sync, _ = IGDBSyncStatus.objects.get_or_create(id=2)
        last = sync.last_updated_at
        self.stdout.write("Sync starting from {last}")
        for endpoint, model_class in REFERENCE_TABLES:
            self.stdout.write(f"sync for {endpoint}")
            fields= ENDPOINT_FIELDS[endpoint]
            query = f"fields {fields}; limit 500;"  
            data = get_igdb_data(endpoint, query)
            for item in data:
                defaults={
                    "name":item.get("name", ""),
                    "slug":item.get("slug", "")
                }
                if model_class is Platform:
                        defaults["abbreviation"]= item.get("abbreviation", "")  
                        defaults["alternative_name"]= item.get("alternative_name", "") 
                
                obj,created= model_class.objects.update_or_create(
                    igdb_id = item["id"],
                    defaults = defaults                   
                )  
            sync.last_updated_at = make_aware(datetime.now())
            sync.save()
            self.stdout.write(self.style.SUCCESS("IGDB reference table sync complete..."))
            
                     
                
                