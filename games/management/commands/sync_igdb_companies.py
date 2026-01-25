from django.core.management import BaseCommand
from games.models import IGDBSyncStatus, Company
from games.services.igdb import get_igdb_data
from django.utils.timezone import make_aware, datetime

class Command(BaseCommand):
    help = "Sync IGDB companies incrementally"

    def handle(self, *args, **kwargs):
        sync, _ = IGDBSyncStatus.objects.get_or_create(id=3)
        last_ts = int(sync.last_updated_at.timestamp()) if sync.last_updated_at else 0
        self.stdout.write(f"Starting company sync from timestamp: {last_ts}")
        limit = 500
        offset = 0
        highest_ts = last_ts
        total_processed = 0
        while True:
            query = f"fields id, name, updated_at; limit {limit}; offset {offset};"
            if last_ts:
                query += f" where updated_at > {last_ts};"
                
            data = get_igdb_data("companies", query)
            if not data:
                if offset == 0:
                    self.stdout.write("No new companies found.")
                break

            for item in data:
                igdb_updated_at = item.get("updated_at", last_ts)
                updated_dt = make_aware(datetime.fromtimestamp(igdb_updated_at))
                company, created = Company.objects.update_or_create(
                    igdb_id=item["id"],
                    defaults={
                        "name": item.get("name", ""),
                        "igdb_updated_at": updated_dt
                    }
                )
                self.stdout.write(f"{'Added' if created else 'Updated'}: {company.name}")
                highest_ts = max(highest_ts, igdb_updated_at)
                total_processed += 1

            offset += limit
        sync.last_updated_at = make_aware(datetime.fromtimestamp(highest_ts))
        sync.save()

        self.stdout.write(self.style.SUCCESS(
            f"IGDB company sync complete! Total processed: {total_processed}"
        ))
