call pip install virtualenv
call virtualenv venv
call venv/scripts/activate
call pip install --upgrade pip
call pip install -r requirements.txt
call python manage.py makemigrations
call python manage.py migrate
echo "close this. Then, click run.bat"
pause