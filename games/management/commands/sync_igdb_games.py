from django.core.management.base import BaseCommand
from games.services.igdb import get_igdb_data
from games.models import Game, IGDBSyncStatus, Genre, Collection, Company, Platform, Franchise, Theme, GameMode, GameTimeToBeat, Keyword, PlayerPerspective
from django.utils.timezone import make_aware, datetime
from decimal import Decimal

def set_many2many(game, model, igdb_ids, field_name):
    if not igdb_ids:
        return
    objs= model.objects.filter(igdb_id__in=igdb_ids)
    getattr(game, field_name).set(objs)
    
def sec_to_hr(sec):
    return round(Decimal(sec)/Decimal(3600), 2) if sec else None
    
class Command(BaseCommand):
    help = "Sync games data from IGDB incrementally using updated_at field"

    def handle(self, *args, **kwargs):
        sync, _= IGDBSyncStatus.objects.get_or_create(id=1)      
        last= sync.last_updated_at #datetime obj(2023-06-06 05:52:51.000000)
        last_ts= int(last.timestamp()) if last else 0 #convert datetime->unix timestamp
        self.stdout.write(f"IGDB sync starting from (last_ts={last_ts})...")

        query = f"""
        fields 
        name, 
        summary, 
        first_release_date, 
        cover.image_id,
        storyline,
        hypes,
        rating,
        rating_count,
        total_rating,
        total_rating_count,
        url,
        genres,
        game_modes,
        platforms,
        franchises,
        player_perspectives,
        themes,
        keywords,
        collections,
        similar_games,
        involved_companies.company, 
        involved_companies.publisher, 
        involved_companies.developer,
        updated_at;
        where updated_at > {last_ts};
        sort updated_at asc;
        limit 500;
        """
        data = get_igdb_data("games", query)
        if not data:
            self.stdout.write("No new updates")
            return
        highest_ts= last_ts
        game_ids = []
        self.stdout.write("after query")
        for item in data:
            igdb_id = item["id"]
            name = item.get("name", "")
            description= item.get("summary", "")
            released= item.get("first_release_date")
            igdb_updated_at = item.get("updated_at")
            cover_id = item.get("cover", {}).get("image_id")
            cover_url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover_id}.jpg" if cover_id else None
            story_line = item.get("story_line", "")
            hypes = item.get("hypes", 0)
            igdb_rating = item.get("rating")
            igdb_rating_count = item.get("rating_count")
            total_rating = item.get("total_rating")
            total_rating_count = item.get("total_rating_count")
            igdb_url = item.get("url", "")            
            released_dt= make_aware(datetime.fromtimestamp(released)) if released else None
            updated_dt = make_aware(datetime.fromtimestamp(igdb_updated_at))
            
            game, created = Game.objects.update_or_create(
                igdb_id=igdb_id,
                defaults={
                    "name": name,
                    "description": description,
                    "released": released_dt,
                    "cover_url":cover_url,
                    "story_line":story_line,
                    "hypes":hypes,
                    "igdb_rating":igdb_rating,
                    "igdb_rating_count":igdb_rating_count,
                    "total_rating":total_rating,
                    "total_rating_count":total_rating_count,
                    "igdb_url":igdb_url,
                    "igdb_updated_at": updated_dt,
                    
                }
            )
            set_many2many(game, Genre, item.get("genres"), "genres")
            set_many2many(game, GameMode, item.get("game_modes"), "game_modes")
            set_many2many(game, Platform, item.get("platforms"), "platforms")
            set_many2many(game, Franchise, item.get("franchises"), "franchises")
            set_many2many(game, PlayerPerspective, item.get("player_perspectives"), "player_perspectives")
            set_many2many(game, Theme, item.get("themes"), "themes")
            set_many2many(game, Keyword, item.get("keywords"), "keywords")
            set_many2many(game, Collection, item.get("collections"), "collections")
            set_many2many(game, Game, item.get("similar_games"), "similar_games")
            developer_ids=[]
            publisher_ids=[]
            for c in item.get("involved_companies", []):
                company_id= c.get("company")
                if not company_id:
                    continue
                if c.get("developer"):
                    developer_ids.append(company_id)
                if c.get("publisher"):
                    publisher_ids.append(company_id)    
            game.developer.set(Company.objects.filter(igdb_id__in=developer_ids))
            game.publisher.set(Company.objects.filter(igdb_id__in=publisher_ids)) 
             
            highest= max(highest_ts, item.get("updated_at",0))
            self.stdout.write(f"{'added' if created else 'updated'}: {game.name}")
        if game_ids:
            ttb_query = f"""
            fields game_id, hastily, normally, completely;
            where game_id = ({', '.join(map(str, game_ids))})
            """    
            ttb_data = get_igdb_data("game_time_to_beats", ttb_query)
            for ttb in ttb_data:
                try:
                    game = Game.objects.get(igdb_id=ttb["game_id"])
                except Game.DoesNotExist:
                    continue
                GameTimeToBeat.objects.update_or_create(
                    game = game,
                    defaults = {
                        "main_story":sec_to_hr(ttb.get("hastily")),
                        "main_sides":sec_to_hr(ttb.get("normally")),
                        "completion":sec_to_hr(ttb.get("completely")),
                    }
                ) 
                
                        
        sync.last_updated_at=make_aware(datetime.fromtimestamp(highest))
        sync.save()
        self.stdout.write(self.style.SUCCESS("IGDB Sync Complete!"))
