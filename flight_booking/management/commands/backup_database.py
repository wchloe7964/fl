import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup SQLite database'
    
    def handle(self, *args, **options):
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        db_path = settings.DATABASES['default']['NAME']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
        
        try:
            # Copy database file
            shutil.copy2(db_path, backup_file)
            
            # Keep only last 7 backups
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('db_backup_')])
            for old_backup in backups[:-7]:
                os.remove(os.path.join(backup_dir, old_backup))
            
            self.stdout.write(self.style.SUCCESS(f'Database backed up to {backup_file}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Backup failed: {str(e)}'))