An API to perform CRUD operations with Courses
## How to use:
1. Clone [this](https://github.com/BorodaUA/courses_api) repository
2. Inside the repository folder create ".env" file, with following data (example):
    - SECRET_KEY=env super secret key
    - DATABASE_URI=sqlite:////usr/src/app/db/courses.db
    - DATABASE_FILE_PATH=/usr/src/app/db/courses.db
    - TEST_DATABASE_URI=sqlite:////usr/src/app/db/test_courses.db
    - TEST_DATABASE_FILE_PATH=/usr/src/app/db/test_courses.db
3. Create Docker image for the project
```
docker build -t ${PWD##*/}-image .
```
4. Run project`s Docker container
```
docker run -d -p 4000:4000 -v ${PWD}:/usr/src/app --name ${PWD##*/}-container ${PWD##*/}-image
```
5. Run project`s tests
```
docker exec -it ${PWD##*/}-container /bin/sh -c "cd tests; pytest -s -o log_cli=true"
```
6. Run project`s flask app
```
docker exec -it ${PWD##*/}-container python run.py
```
7. Visit app main page [http://localhost:4000/api/1.0/](http://localhost:4000/api/1.0/)