from django.core.management.base import BaseCommand
from games.services.igdb import get_igdb_data
from games.models import Game, IGDBSyncStatus
from django.utils.timezone import make_aware, datetime


class Command(BaseCommand):
    help = "Sync games data from IGDB incrementally using updated_at field"

    def handle(self, *args, **kwargs):
        sync, _= IGDBSyncStatus.objects.get_or_create(id=1)
        
        last= sync.last_updated_at #datetime obj(2023-06-06 05:52:51.000000)
        last_ts= int(last.timestamp()) if last else 0 #convert datetime->unix timestamp
        self.stdout.write(f"Starting IGDB sync (last_ts={last_ts})...")

        query = f"""
        fields name, summary, first_release_date, updated_at, cover.image_id,
        involved_companies.company.name, involved_companies.publisher, involved_companies.developer;
        where updated_at > {last_ts};
        sort updated_at asc;
        limit 500;
        """
        data = get_igdb_data("games", query)
        if not data:
            self.stdout.write("No new updates")
            return
        highest_ts= last_ts
        for item in data:
            igdb_id = item["id"]
            name = item.get("name", "")
            developer = ""
            publisher = ""
            for c in item.get("involved_companies", []):
                comp = c.get("company", {}).get("name", "")
                if c.get("developer") and comp:
                    developer = comp
                if c.get("publisher") and comp:
                    publisher = comp

            cover_id= item.get("cover", {}).get("image_id")
            cover_url= f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover_id}.jpg" if cover_id else None
            released_dt= make_aware(datetime.fromtimestamp(item["first_release_date"])) if item.get("first_release_date") else None
            updated_dt = make_aware(datetime.fromtimestamp(item["updated_at"]))
            game, created = Game.objects.update_or_create(
                igdb_id=igdb_id,
                defaults={
                    "name": name,
                    "developer": developer,
                    "publisher": publisher,
                    "description": item.get("summary", ""),
                    "released": released_dt,
                    "igdb_updated_at": updated_dt,
                    "cover_url":cover_url
                }
            )
            highest= max(highest_ts, item.get("updated_at",0))
            self.stdout.write(f"{'added' if created else 'updated'}: {game.name}")
            print("Created:" if created else "Updated:", name)
        sync.last_updated_at=make_aware(datetime.fromtimestamp(highest))
        sync.save()
        self.stdout.write(self.style.SUCCESS("IGDB Sync Complete!"))
