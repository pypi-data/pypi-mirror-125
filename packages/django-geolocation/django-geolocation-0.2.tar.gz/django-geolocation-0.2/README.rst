=====
geolocation
=====

geolocation is a Django app which takes the IP address of the client and,
exploiting an external API (via get requests), gives information about 
the client's location based on the IP address. After this, the address 
is stored in a postgre database which is used to count how many times 
the client has connected to the web app. The index page shows the 
geolocation data of the client.

Quick start
-----------

1. Add "geolocation" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'geolocation',
    ]

2. Include the geolocation URLconf in your project urls.py like this::

    path('geolocation/', include('geolocation.urls')),

3. Run ``python manage.py migrate`` to create the geolocation models.

4. Start the development server and visit http://127.0.0.1:8000/
