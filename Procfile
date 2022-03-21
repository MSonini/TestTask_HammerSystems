release: sh -c 'cd hammersystems && python manage.py migrate'
web: sh -c 'cd hammersystems && gunicorn hammersystems.wsgi --log-file=-'
