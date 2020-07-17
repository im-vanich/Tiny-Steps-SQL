# TinySteps -  simple service for the selection of tutors

You are going to create a site that will have a "database" in the form of JSON files.

When responding to a request, data from the "database" must be read, and when saving user orders, the data must be written to the "database".

1. Describe the routes

2. Copy mock data to JSON file
    - Write a script that from the mock data in data.py will save it to our "database".
    
3. Выведите страницу преподавателя
    - examine the mock data,
    - read instructor data from JSON file,
    - edit the template,
    - check the result,
    - display a sign of employment,
    - make a link to the booking page from the time selection button(form a link like / booking / 215 / monday / 12).
    
4. Implement a booking page   
    - study the template,
    - display the form using the data about the teacher, as well as the day and time
    - display data on the time and day of the week in hidden fields from the request address (like / booking / 215 / monday / 12)
    
5. Implement a booking completion page   
    - accept data via booking_done,
    - save the data in the JSON file booking.json. Don't lose your application when registering new ones!
    - display a message that everything is successful
    
6. Implement a pick request complete page
    - accept data via request,
    - save the data in a JSON file request.json. Don't lose your application when registering new ones!
    - display a message that everything is successful,
    - check that the request was recorded in the file.
    
7. Implement a goal page 
    - get the target,
    - get a list of teachers, filter teachers by goal,
    - display them on the page in descending order of rating
    
8. Display the main page
    - get 6 random teachers
    - display them on the page,
    - add links to goals
    
9. Add another target
   – проверьте, что, используя цели в шаблонах, вы всегда получаете их из python- кода
   – добавьте новую цель "для программирования" преподавателям   8,9,10,11
   – проверьте, что цель корректно отображается на всех страницах


## Dependencies

All requirements are listed in the file: `requirements.txt`.
