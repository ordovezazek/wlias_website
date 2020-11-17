# wlias website

Follow these steps to setup:

1. install Python3, pip3, virtualenv, and git
2. open terminal/cmd and enter the following commands:

         git clone https://github.com/ordovezazek/wlias_website.git
         
3. cd into wlias_website folder and enter the following commands:

        git checkout -b [your name]
        git branch
        python3 -m venv wlias_env
        echo 'source wlias_env/bin/activate' > env.txt
        source env.txt
        
4. cd into wliasite folder
5. enter into terminal/cmd: pip install -r requirements.txt

Run website on localhost:

1. [terminal/cmd]: python manage.py makemigrations
2. [terminal/cmd]: python manage.py migrate
3.[terminal/cmd]: python manage.py createsuperuser
4.[terminal/cmd]: python manage.py runserver
5. Enter in browser address bar: localhost:8000/admin or localhost:8000
