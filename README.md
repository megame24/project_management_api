# project_management_api
[![Build Status](https://travis-ci.org/megame24/project_management_api.svg?branch=staging)](https://travis-ci.org/megame24/project_management_api) [![codecov](https://codecov.io/gh/megame24/project_management_api/branch/staging/graph/badge.svg)](https://codecov.io/gh/megame24/project_management_api)

### Deployed test api on heroku
- link: https://test-proj-m-api.herokuapp.com/
- Admin credentials (for testing purposes): email: `admin@projm.com`, password: `Adm1nP@ssw0rd`

### API documentation
- link: https://test-proj-m-api.herokuapp.com/api/doc

### Installation

Ensure you have python 3.7 and virtualenv installed

- Clone repo and navigate to root directory
```
git clone https://github.com/megame24/project_management_api.git && cd project_management_api
```
- Create and activate virtual environment
```
virtualenv -p python3.7 venv && source venv/bin/activate
``` 
- Referencing the `.env-sample` file, create a `.env` file
- Install dependencies
```
pip install -r requirements.txt
```
- Run migrations
```
flask db migrate
flask db upgrade
```
- Run app
```
flask run
```
- Run test
```
pytest
```

### Assumptions

The following are some of the assumptions and design decisions made while developing this application


- Database seeded admin(s): The admin(s) are seeded into the database, only regular users can sign up

- Created stories are assigned to all admin(s) by default: Once a story is created, any admin can retrieve it and approve or reject

- Users can't update created stories

- Users can only retrieve stories they created

- Admins can retrieve all stories in the application

### License

MIT