# Capstone project - Luxury Car Rental

## Distinctiveness & complexity

The main difference between my Captsone project "Rental-50" & project 2 "commerce" relies on the renting function, as many users can rent a single car as long as their dates are not the same (if user1 rents car1 for 1-1-2025, then user2 cannot rent car1 for that same day, but can rent car2 for 1-1-2025).

While thinking of this project, I always kept in mind all the previous projects and what I learned from them, so that I could combine all of that on a project that motivates me to complete it and makes me ambitious about it, so I came with this project idea of a car rental page. After reviewing all of the previous projects to see if they where completed, while taking inspiration for these capstone, I was always asking myself these question "if the capstone has to be more complex than this, what can I create that satisfies the requirements & myself as a web programmer?".

## What does this project have?

This project wants to create a web page where any person can look for a vehicle to rent on a specific place. These are some of the technical things that it has:

- A place to log-in, register & log-out with your user. :white_check_mark:
- As a user, you can search for a specific geographic place to see all available options on your city, with many other parametres to customize the results as much as you want. :white_check_mark:
- Using an internal API, staff members can fetch for all of the users & cars that are on the database. :white_check_mark:
- If user is logged-in, he can make a reserve for a specific vehicle for certain amount of time, as long as no user has previously bookmarked that same day. :white_check_mark:
- Using the search bar, a user can filter vehicles according to certain days, models, manufacturers or place where the vehicle is located. :white_check_mark:

## Admin-related functions

On the Django-admin interface, if the user is allowed in he can have access to the following tables:

- All the cars that are available, that can be toggled as not available if the company no longer rents them or own them. :white_check_mark:
- Users that are registered, as well as some personal information that te page requires for any user. :white_check_mark:
- Rentals that happened in the past for any vehicle or user. :white_check_mark:
- Create new cars that will be available for the users to rent. :white_check_mark:

## How does this app work?

To start, you must **cd** into the **capstone** app (path must look similar to this: C:\Users\PC\Documents\GitHub\CS50-Web-Programming-Course\capstone\capstone). Once you are here you must run these 2 migrations commands on your terminal (**python manage.py makemigrations car_rental** && **python manage.py migrate**). Now, you can start the server by running **python manage.py runserver**. First thing you will see is a small landing page I made, where there is not much to be seen apart from some front-end customization. Next thing you will likely want to do is click on **search** on the navbar or on the button located on the last section of the landing. Now, you can see a search form which it's use is pretty intuitive, by just looking for vehicles according to your inputs, which will show on a new page & you can open them to see more images or book the car. Also, there is a log-in system inspired by the ones on the other projects, but a bit more complex, by asking for some more information.

## More technical information on how these works

Getting into the more technical information & usage, let's start with the databases. On the models.py you can see how I created them, & this is how they work & their expected usage & functions:

**Models:**

- **User**: this class is pretty simple, only thing it does is store every user's data so that whenever they book a car the page knows something more about them.
- **Make**: the Make table is thought to just store the name of all of the car manufactures to use as a foreign key when choosing the models that are available.
- **Model**: following the Make table, Model is just a table that has 2 columns: a foreign key related to the make table & a name one for the car model.
- **City**: City table is only used to create the cities in which the page has cars to rent, so it is used as a foreign key on the upcoming Car table.
- **Chasis**: same track as with the Make, Model & City tables, this is just to classify the cars by their chasis type, so that it gives the database a more complex look & information storage.
- **Car**: one of the most important tables we have, this is thought to keep the vehicles the company has to rent (as well as the ones that are no longer available), with a primary key being the licence plate (expected to be unique no matter the country or city the car is in). As I previously mentioned, this table has 4 foreign keys: Make, Model, City & Chasis. Finally, when the car is created, you can **optionally** include up to 5 images of the car, which will be shown on a carousel when any user access the cars.html (URL: [http://localhost:8000/car/${licence_plate}/]).
- **Booking**: finally our last table, Booking is meant to store all past, present & future books for vehicles, storing the car, user, date, if the car has to be delivered to the user's house or not (a simple boolean) & total price (same price as the base one the car has per day, as the page only allows users to rent the cars for a single day).

**More files & paths in the app:**

- **templates\car_rental**: in this path you can find the main HTML files that the page renders according to their path. Here is what each file contains:
  - **book.html**: this is the file that shows the form so that a user can book a car.
  - **cars.html**: in here the cars information is rendered so that any user can see it.
  - **edit_profile.html**: this is so that if a user wants to change their personal information such as name, surname, phone number, etc. they can do it.
  - **index.html**: in here you can find the search form for the cars that are available in the database, following certain parameters.
  - **landing.html**: a simple landing page that just shows some basic front-end, so that we make the website more user-friendly.
  - **layout.html**: this just imports most of the static files & creates the navbar that the user always has on top.
  - **login.html**: in here users with an existing account can log-in to access more features on the website.
  - **profile.html**: a simple profile viewer for any user to see their profile or others.
  - **register.html**: a long form so that new users can create their account.
  - **search.html**: the results for the search form on "index.html".
  - **staff.html**: a small site that staff members can access for a simple look at users & cars that exist.
- **\static\car_rental**: this is the path to the **script.js** & **styles.css** files that I used to customize my front-end, plus another folder (**\static\car_rental\photos**) that contains all of the images that are used on my front-end for customization purposes.
- **images**: this is the path where the images that are asociated with the cars are stored, & are mainly accessed when a user wants to see any car on **cars.html**.

**Django files:**

- **`__init__.py`**: empty file that is used to mark a directory as a Python package.
- **`admin.py`**: this file only registers my models to the **/admin** path, so that staff members or superusers can saccess the information on my databases.
- **`urls.py`**: this is the logic that connects the requests that the user submits to their response functions on my **`views.py`**.
- **`models.py`**: in here you can find the models that my page uses to create the databases, which you can see on my **Models** part on this file.
- **`views.py`**: here you can see the functions that handle the logic & requests between the user & the server, with more than 200 lines of many different Python functions.
