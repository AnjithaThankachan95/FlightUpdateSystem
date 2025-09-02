# FlightUpdateSystem
When a passenger tries to book or check-in, the system needs to know if the flight is On Time, Delayed, Cancelled, or Boarding.

#Project Name  
Flight Status Tracker 

#Description 
Flight Tracker is a web app that lets users check flight status by entering a flight number. It shows departure, arrival, and status using the AviationStack API. 
Built with Python and FastAPI for the backend, Jinja2 for templates, and PostgreSQL via Docker with SQLAlchemy ORM. 

#Features 
Enter flight number to check status. 

Show departure, arrival, and status. 

Keep flight number after checking. 

Clear input and results with a button. 

Fetch real-time data via AviationStack API. 

Simple login/logout interface. 

#Technologies Used 
Programming Language: Python 

Backend: FastAPI 

Frontend: HTML, Tailwind CSS, Jinja2  

Database: PostgreSQL (Docker) 

ORM: SQLAlchemy 

API: AviationStack (Open API) 

Others: Pydantic, Forms 

#Usage 
Login with your username  

Enter a flight number and click Check Status. 

View flight info. 

Click Clear to reset input. 

Use Logout to sign out. 
  

#Future Improvements  
Full user registration/authentication. 

Store search history. 

Mobile-responsive UI. 

Cache frequent flights to reduce API calls. 
