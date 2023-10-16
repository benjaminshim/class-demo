# TODO List
Team Members: Benjamin Shim, Andy Quintuna, Bridget Kegelman, Carolina Martin

## Project Description
This API server will allow users to have a ToDo list. This will have a simple UI that is easy to use for the everyday
person. The user will be able to see their todo list items as well as add new ones and delete the ones that they have 
finished.

## User Registration
A user will be able to create an account and login.
This will allow the user to see their todo list items that will be stored in the database.

## CRUD Operations
User will be able to:
- Create ToDo list items
- Read ToDo list items
- Update ToDo list items
- Delete ToDO list items

## URL Paths
| Funstionality  | Method  | Path |
| :------------: |:-------:| :---:|
| Create todo list | POST | /todo |
| Read todo list | GET | /todo{id} |
| Update todo list | PUT | /todo{id} |
| Delete todo list | DELETE | /todo{id} |

