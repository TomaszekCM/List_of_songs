import os


def periodic_backup():
    os.system("python3 manage.py dumpdata --format json -e contenttypes -e auth.permission > backups/czystedanezbazy3.json")
    return True