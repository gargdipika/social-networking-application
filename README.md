Django Rest Framework application with UI

## Steps to setup and run application

1. Create a virtual enviornment run below command
    # python -m virtualenv ./venv (venv is name of vertual env.)
2. Activate virtual env
    # .\venv\Scripts\activate
3. Install dependencies run below command
    # pip install -r requirements.txt
4. Run below command to start the application
    # python manage.py runserver

## Steps to run application from browser

1. Open the browser and navigate to below url for home page
    # http://localhost:8000/
2. Access all the ui pages through above url by clicking on buttons or anchor elements
3. To login admin page first create superuser
    # python manage.py createsuperuser
4. For admin panel navigate to below url
    # http://localhost:8000/admin

## Steps to run postman collection

1. Import postman collection file from path - /postman-collection/social_network_app.postman_collection.json
2. Click on apis and send.