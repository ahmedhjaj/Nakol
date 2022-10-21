# Nakol Project
## CS50x
> CS50x: Introduction to Computer Science is Introduction to the intellectual enterprises of computer science and the art of programming. 

> This is my final project for CS50x Course.

## Project Explainations

Nakol, "We Eat" in Arabic, is a website for EJUST students/university students who live in dorms to find and connect food mates for ordering food or going to resturants.

### Features include

- Registration and Login
- Add a post with number of people to join, resturant details, and comments
- Preview delivery and in-resturant posts
- Select and join parties through posts
- Access the Dashboard to see other's information: number, name, and email.
- Add resturants

## Tables used in the Project (sqlite3)

![Tables Visual](/static/QuickDBD-export.png)

- TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
- TABLE sqlite_sequence(name,seq);
- UNIQUE INDEX username ON users (username);
- TABLE cuisines (rest_id INTEGER, cuisine TEXT NOT NULL, FOREIGN KEY(rest_id) REFERENCES resturants(id));
CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER, rest_id INTEGER, time_from TEXT NOT NULL, time_to TEXT NOT NULL, number_of_people NUMERIC NOT NULL , order_type TEXT NOT NULL, comments TEXT, current_people NUMERIC DEFAULT 1 NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(rest_id) REFERENCES resturants(id));
- TABLE dashboard (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_post INTEGER, user_id INTEGER, Foreign KEY(id_post) REFERENCES posts(id), FOREIGN KEY (user_id) REFERENCES users(id));
- TABLE resturants (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,resturant_name TEXT NOT NULL, resturant_number NUMERIC NOT NULL, dine_in BOOL NOT NULL, delivery BOOL NOT NULL, location TEXT NOT NULL);
- TABLE profile (user_id INTEGER, number numeric NOT NULL, email TEXT NOT NULL,name TEXT NOT NULL, building NUMERIC NOT NULL, room NUMERIC NOT NULL , FOREIGN KEY(user_id) REFERENCES users(id));

## Technologies used

The site was built using Flask (Python), SQLite3 for the database, CSS, bootstrap5 and javascript. Also, I hashed the passwords for safety.

## Conculusion

It was very interesting to create this project from scratch using Flask and I used a lot of new resources for me, which I had never worked with before. I spent a lot of time studying and testing before implementing the code. All references to the pages I used as a support are commented on in the code.

I learned a lot from this project, and I was very happy with the result.





