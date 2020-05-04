# Casting Agency 
Capstone project for Udacity Full Stack Nanodegree

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Local Database Setup
To set up local database just change LOCAL_DATABASE_URL variable in config.py file. 
After that run theses commands: (*notice: make sure virtual environment is active before running theses commands*)
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server locally

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
flask run --reload
```

Adding the --reload attribute to flask run will detect file changes and restart the server automatically.


# API Reference
**This project is currently hosted on:  [https://fsndcastingagency.herokuapp.com](https://fsndcastingagency.herokuapp.com/)**


**Authentication**: Endpoints require different levels of authentication, depending on user roles.
-   Casting Assistant
    -   Can view actors and movies
-   Casting Director
    -   Can view actors and movies
    -   Can add or remove actors
    -   Can modify actors and movie information
-   Executive Producer
    -   Can view actors and movies
    -   Can modify actors and movie information
    -   Can add or remove actors
    -   Can add or remove movies

Sample token are available on the **config.py** file, notice they are valid only for 24 hours. 

## Error handling
Errors are returned as JSON object in the following format

    {
	    "success": False,
	    "error": 400,
	    "message": "bad request"
    }
The API will return four error types when requests fails:

 - **404**: ressource not found
 - **401**:  unauthorized Request
 - **422**: unprocessable
 - **400**: bad request
 - **405**: method not allowed
 
 ## Endpoints
 ### Get  '/movies'
-   Required permission: View movies
-   Fetches available movies as an array of objects that contain a movie id, title, and release date
-   Request arguments: None

 #### Sample
 `curl --location --request GET 'https://fsndcastingagency.herokuapp.com/movies' \
--header 'Authorization Bearer {TOKEN}' `

```
 {
 	"movies":  [
 		{
 			"id":  1,
 			"release_date":  "2019-09-05",
 			"title":  "Avengers End Game"
 		},
 	],
 	"success":  true
 }
```


### Post '/movies'
-  Required permission: Post movies
-   Posts a new movie to the database. Required fields are  `title`  and  `release_date`
-   Request arguments: None
 
 #### Sample
 `curl --location --request POST 'https://fsndcastingagency.herokuapp.com/movies' \
--header 'Authorization: Bearer {TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "Black panthers",
	"release_date": "05-04-2018"
}'`

 
```
{
	"movie": [
		{
			"id": 2,
			"release_date": "05-04-2018",
			"title": "Black panthers"
		}
	],
	"success": true
}
 ```

### Patch '/movies/{movie_id}'

 -  Required permission: Edit movies
-   Edits a movie. Available fields are  `title`  and  `release_date`
-   Request arguments:  `movie_id`
-   Return the updated movie
 ### Sample
 `curl --location --request PATCH 'https://fsndcastingagency.herokuapp.com/movies/2' \
--header 'Authorization: Bearer {TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "Captain America",
	"release_date": "05-05-2017"
}'`
 
 ```
{
	"movie":[
		{
			"id":2,
			"release_date":"05-05-2017",
			"title":"Captain America"
		}
	],
	"success":true
}

```

### Delete '/movies/{movie_id}'

-   Required permission: Delete movies
-   Deletes a movie from the database.
-   Request arguments:  `movie_id`
-   Response: the deleted movie id and a boolean for success

### Sample
`curl --location --request DELETE 'https://fsndcastingagency.herokuapp.com/movies/2' \
--header 'Authorization: Bearer {TOKEN}'`

```
{
	"deleted":2,
	"success":true
}
```

### Get  '/actors'
-   Required permission: View actors
-   Fetches available actors as an array of objects that contain a actor id, name, age gender
-   Request arguments: None

 #### Sample
 `curl --location --request GET 'https://fsndcastingagency.herokuapp.com/actors' \
--header 'Authorization Bearer {TOKEN}' `

```
 {
 	"actors":  [
	 	{
		 	"id":1,
		 	"age":55,
		 	"gender":"male",
		 	"name":"Robert Downey Jr"
		 }
 	],
 	"success":  true
 }
```


### Post '/actors'
-  Required permission: Post actors
-   Posts a new actor to the database. Required fields are  `name`  , `age` and `gender`
-   Request arguments: None
 
 #### Sample
 `curl --location --request POST 'https://fsndcastingagency.herokuapp.com/actors' \
--header 'Authorization: Bearer {TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Will Smith",
	"age": 58,
	"gender": "male"
}'`

 
```
{
	"actor": [
		{
			"id": 2,
			"name": "Will Smith",
			"age": 58,
			"gender": "male"
		}
	],
	"success": true
}
 ```

### Patch '/actors/{actor_id}'

 -  Required permission: Edit actor
-   Edits an actor. Available fields are  `name`  , `age` and `gender`
-   Request arguments:  `actor_id`
-   Return the updated actor
 ### Sample
 `curl --location --request PATCH 'https://fsndcastingagency.herokuapp.com/actors/2' \
--header 'Authorization: Bearer {TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
	"age": "60"
}'`
 
 ```
{
	"actor":[
		{
			"id":2,
			"name":"Will Smith",
			"age":"60",
			"gender": "male"
		}
	],
	"success":true
}

```

### Delete '/actors/{actor_id}'

-   Required permission: delete actor
-   Deletes an actor from the database.
-   Request arguments:  `actor_id`
-   Response: the deleted actor id and a boolean for success

### Sample
`curl --location --request DELETE 'https://fsndcastingagency.herokuapp.com/actors/2' \
--header 'Authorization: Bearer {TOKEN}'`

```
{
	"deleted":2,
	"success":true
}
```


## Testing
To run the tests, run
```
python test_app.py
```