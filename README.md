An API to perform CRUD operations with Courses
### Creating Docker image for the project
```
docker build -t ${PWD##*/}-image .
```
### Running project`s Docker container
```
docker run -d -p 8080:80 -v ${PWD}:/usr/src/app --name ${PWD##*/}-container ${PWD##*/}-image
```