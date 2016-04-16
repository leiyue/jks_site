import mimetypes
import os
import shutil
import zipfile

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils import timezone

try:
    BACKUP_DIR = '%s/%s' % (settings.PROJECT_ROOT, settings.ADMIN_BACKUP_DIR)
except AttributeError:
    BACKUP_DIR = '%s/backup' % settings.PROJECT_ROOT

SQL_BACKUP_DIR = '%s/sql' % BACKUP_DIR


def zip_dir(path, zip):
    for root, dirs, files in os.walk(path):
        relative_path = os.path.relpath(root, path)
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename):
                arcname = os.path.join(relative_path, file)
                zip.write(filename, arcname)


def send_file(path, filename=None, content_type=None):
    if filename is None:
        filename = os.path.basename(path)
    if content_type is None:
        content_type, encoding = mimetypes.guess_type(filename)

    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write(open(path, 'rb').read())
    return response


@staff_member_required
def admin_backup(request):
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)
    os.mkdir(BACKUP_DIR)
    os.mkdir(SQL_BACKUP_DIR)

    zip_path = '%s/backup-%s.zip' % (BACKUP_DIR, str(timezone.now()).replace(' ', '_'))
    zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    for db in settings.DATABASES:
        db = settings.DATABASES[db]
        if db['ENGINE'] == 'django.db.backends.sqlite3':
            if os.path.isabs(db['NAME']):
                db_file = db['NAME']
            else:
                db_file = '%s/%s' % (settings.PROJECT_ROOT, db['NAME'])

            shutil.copy(db_file, SQL_BACKUP_DIR)

        elif db['ENGINE'] == 'django.db.backends.mysql':
            os.system(
                'mysqldump -u %s %s -p%s > %s/%s.sql' % (
                    db['USER'],
                    db['NAME'],
                    db['PASSWORD'],
                    SQL_BACKUP_DIR,
                    db['NAME'],
                )
            )

        elif db['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            os.system(
                'pg_dump -Fc -w -U %s -f %s/%s.sql %s' % (
                    db['USER'],
                    SQL_BACKUP_DIR,
                    db['NAME'],
                    db['NAME'],
                )
            )

    zip_dir(SQL_BACKUP_DIR, zip_file)
    zip_dir(settings.MEDIA_ROOT, zip_file)
    zip_file.close()

    return send_file(zip_path)
