# TinySteps -  simple service for the selection of tutors

You are going to create a site that will have a SQlite.


1. Create the Teacher Model
    - Install and connect SQLAlchemy.
    - Describe the model for the teacher.
    - Check that the primary key, types and constraints are in order.

2. Create a "Booking" model
    - Describe the booking model.
    - Link the model with a teacher (one to many) relationship.
    - Check that the primary key, types and constraints are in order.
    
3. Create a Sort Requisition Model
    - Describe the model.
    - Check that the primary key, types and constraints are in order.
    
4. Populate the database   
    - Connect and configure migrations inside the app.py file
    - Initialize migrations with flask db init
    - Write or migration command, which imports the data from JSON teachers base
    
5. Modify the teacher's route   
    - Replace getting data from a file to execute a query in the database.
    - When the teacher does not exist, roll out a 404.
    
6. Modify the target route, for example, "to move"   
    - Get instructors with a filter and sort query.
    
7. Modify the main route    
    - Replace getting data from a file to execute a query in the database.
    
8. Refine the route and booking page with feedback   
    - Combine routes for displaying and submitting a form into one
    - Validate the form: all fields must be completed.
    - Replace the write to the file with the write to the database.
    
9. Modify the route and page of the application for selection  
    - Combine routes for displaying and submitting a form into one
    - Validate the form: all fields must be completed.
    - Replace the write to the file with the write to the database


## Dependencies

All requirements are listed in the file: `requirements.txt`.
