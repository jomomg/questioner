# Questioner

Questioner is an api for posing questions for events. Users can log in to the app and post questions for their particular event. Other users can then vote on these questions.

It is made with Django.

#### Features

  - Users can sign up
  - Users can create events
  - Users can create questions for events
  - Users can vote on questions

#### Installation

- Clone this repository
- Set up a virtual environment with > Python 3.6
- Install requirements with ```pip install -r requirements```
- Run server with ```./manage.py runserver```

### Endpoints

The following endpoints are available

| Endpoint | Description |
| ------ | ------ |
| ```POST /auth/register``` | Register a user |
| ```POST /auth/login``` | Login a user |
| ```POST /api/events``` | Create an event |
| ```GET /api/events``` | Get all events |
| ```GET /api/events/<event_id>``` | Get a specific event |
| ```POST /api/questions``` | Create a question |
| ```GET /api/questions``` | Get all questions |
| ```GET /api/questions/<question_id>``` | Get a question |
| ```PATCH /api/questions``` | Edit a question |
