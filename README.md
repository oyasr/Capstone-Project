# Flasky Store API
This is an API to the infamous Flasky online Store. Stores and sellers are able to add their products to Flasky to be viewed by millions of users around the world! As a part of Udacity's Fullstack Developer Nanodegree, it serves as the Capstone Project that bundles all what is learned through the course of this nanodegree.\
\
All backend code follows [**PEP8 style guidelines**](https://www.python.org/dev/peps/pep-0008/)
## Getting Started
### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and postgresql installed on their local machines.\
From the Capstone-Project folder run `pip install -r requirements.txt`. All required packages are included in the requirements file./
To run the application locally run the following command:

    python flasky.py runserver
    
This command puts the application in development which shows an interactive debugger in the console and restarts the server whenever changes are made.\
The application is run on `http://127.0.0.1:5000/` by default.
### Tests
In order to run tests, just run the following command:

    python flasky.py test tests
    
The tests are written using the standard [**unittest**](https://docs.python.org/2/library/unittest.html) package from the Python standard library. The *setUp()* and *tearDown()* methods run before and after each test, and any methods that have a name that begins with *test_* are executed as tests.\
\
The *setUp()* method tries to create an environment for the test that is close to that of a running application. It first creates an application configured for testing and activates its context. This step ensures that tests have access to current_app, like regular requests.Then it creates a brand-new database that the test can use when necessary. The database and the application context are removed in the *tearDown()* method.
### Project Structure
    ├── Capstone-Project/
        ├── app/
        |    ├── main/
        |    |    ├── __init__.py
        |    |    ├── errors.py
        |    |    ├── views.py
        |    ├── auth/
        |    |    ├── __init__.py
        |    |    ├── auth0.py
        |    |    ├── errors.py
        |    |    ├── views.py
        |    ├── __init__.py
        |    ├── models.py
        ├── env/
        ├── migrations/
        ├── tests/
        |    ├── __init__.py
        |    ├── test_basics.py
        |    ├── test_category_model.py
        |    ├── test_product_model.py
        ├── config.py
        ├── flasky.py
        ├── requirements.txt
        ├── setup.sh
         
This structure has four top-level folders:
* The Flask application lives inside a package generically named *app*.
* The *migrations* folder contains the database migration scripts.
* Unit tests are written in a *tests* package.
* The *env* folder contains the Python virtual environment.

There are also a few new files:
* *requirements.txt* lists the package dependencies to regenerate identical virtual environments.
* *config.py* stores the configuration settings.
* *flasky.py* launches the application and other application tasks.
* *setup.sh* contains the environment variables.
## API Reference
### Getting Started
The base URL is currently hosted at **Heroku** on the follwing address https://sample-project-flasky.herokuapp.com/ . This link will redirect you to the authentication page hosted on **Auth0**. The instructions for authentication, RBAC, permissions, etc are discussed in the next section.\
\
As mentioned in the **Pre-requisites and Local Development** this api can be hosted locally at the default `http://127.0.0.1`. 
### Authentication and Authorization
Currently there are three roles defined for this api:
* **Admin**: the flask store admin who has full access over the application.
* **Seller**: any store that can view and add products.
* **Customer**: a regular user who can only view products.

These roles are configured completely in Auth0, with each role having distinctive permission claims included in the signed JWT.\
\
**Signing in as an Admin**: 
* email: admin@flasky.com
* password: flasky_admin1

The returned access token contains the following permissions: `delete:products`, `patch:products`, `post:new-category`, `post:new-product`.

**Signing in as a Seller**: 
* email: seller@flasky.com
* password: flasky_seller1

The returned access token contains the following permissions: `post:new-product`.

**Signing in as a Customer**: 
* email: customer@flasky.com
* password: flasky_customer1

The returned access token has no custom permissions.

After signing in as one of the previous roles the access token is available to you from the URL. Make sure to save the token if you want to test some endpoints using **Postman**, despite you can find role based tokens included in the *setup.sh* file, using your own fresh tokens is recommended.
### Error handling
Errors are returned as JSON objects in the follwing format:

    {
        "success": False,
        "error": 404,
        "message": "resource not found
    }
    
The API will return main five error types when requests fail:
* `400`: Bad Syntax
* `404`: Resource Not Found
* `422`: Bad Request
* `405`: Method Not Allowed
* `500`: Internal Server Error

In addition to a custom implemented *AuthError* class that will rais an error if a authentication-related request fails.
### Endpoints
#### GET /categories
* General: Returns the whole list of various product categories and a success vlaue.
* Authorization: No authorization required
* Sample: `curl https://sample-project-flasky.herokuapp.com/categories`

      {"categories":[
        {
          "id":1,
          "name":"Electronics"
        },
        {
          "id":2,
          "name":"Home Appliances"
        },
        {
          "id":3,
          "name":"Kitchen"
        },
        {
          "id":4,
          "name":"Fashion"
        },
        {
          "id":5,
          "name":"Jewerly"
         }
        ],
      "success":true
      }
    
#### POST /categories
* General: Creates a new category using the submitted name. Returns the id of the created category, success vlaue and the number of total categories
* Authorization: Only the **Admin** role is authorized.
* Sample: `curl https://sample-project-flasky.herokuapp.com/categories -X POST -H "Content-Type: application/json" -H "Bearer: <ACCESS_TOKEN>" -d '{"name":"Machinery"}'`

      {
        "success": True,
        "created": 6,
        "total_categories": 6
      }
      
#### GET /categories/<category_id>/products
* General: 
  * Returns the list of products that belong to a specific category.
  * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
* Authorization: No authorization required
* Sample: `curl https://sample-project-flasky.herokuapp.com/categories/2/products`

      {"current_category":
        {"id":2,"name":"Home Appliances"},
          "page":1,"products":[
            {
              "category":"Home Appliances",
              "description":"20K Washing Manchine",
              "id":6,
              "in_stock":true,
              "name":"Washing Manchine",
              "price":1499
            },
            {
              "category":"Home Appliances",
              "description":"Fridge with deep freezer",
              "id":7,
              "in_stock":true,
              "name":"Fridge",
              "price":1999
            },
            {
              "category":"Home Appliances",
              "description":"3HP AC",
              "id":8,
              "in_stock":true,
              "name":"Air Conditioner",
              "price":1499
            }
         ],
        "success":true,
        "total_category_products":3
      }
      
#### GET /products
* General: 
  * Returns a list of products, success value, total number of products and page number.
  * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
* Authorization: No authorization required
* Sample: `curl https://sample-project-flasky.herokuapp.com/products`

      {"page":1,"products":[
        {
          "category":"Electronics",
          "description":"256 GB iPhone X",
          "id":1,
          "in_stock":true,
          "name":"iPhone X",
          "price":999
        },
        {
          "category":"Electronics",
          "description":"27 inch 2k ips Monitor",
          "id":2,
          "in_stock":true,
          "name":"Asus Monitor",
          "price":499
        },
        {
          "category":"Electronics",
          "description":"Lenovo gaming laptop",
          "id":3,
          "in_stock":true,
          "name":"LenovoY540",
          "price":1099
        }
       ],
      "success":true,
      "total_products":8
      }
      
#### GET /products/<product_id>
* General: Returns a specifict product by its id.
* Authorization: No authorization required.
* Sample: `curl https://sample-project-flasky.herokuapp.com/products/1`

      {
        "current_category":
          {
            "id":1,
            "name":"Electronics"
          },
            "product":
            {
              "category":"Electronics",
              "description":"256 GB iPhone X",
              "id":1,
              "in_stock":true,
              "name":"iPhone X",
              "price":999
            },
        "success":true
      }
      
#### POST /products
* General: Creates a new product using the submitted name, description, price and category id. Returns the id of the created category, success vlaue and the number of total categories.
* Authorization: The **Admin** and the **Seller** roles are authorized.
* Sample: `curl https://sample-project-flasky.herokuapp.com/products -X POST -H "Content-Type: application/json" -H "Bearer: <ACCESS_TOKEN>" -d '{"name":"Galaxy Note 10", "description":"128GB galaxy note 10", "price":"999", "category_id":1}'`

      {
        "success": True,
        "created": 9,
        "total_products": 9
      }
      
#### PATCH /products/<product_id>
* General: Updates an existing product price using the submitted new price. Returns the id of the updated product and a sucess value.
* Authorization: Only the **Admin** role is authorized.
* Sample: `curl https://sample-project-flasky.herokuapp.com/products/1 -X PATCH -H "Content-Type: application/json" -H "Bearer: <ACCESS_TOKEN>" -d '{"price":"799"}'`

      {
        "success": True,
        "updated": id
      }

#### DELETE /products/<product_id>
* General: Deletes an existing product using its id. Returns the id of the deleted product and a sucess value.
* Authorization: Only the **Admin** role is authorized.
* Sample: `curl -X DELETE https://sample-project-flasky.herokuapp.com/products/1`

      {
        "success": True,
        "deleted": id
      }
## Deployment
* First step is to `touch Procfile` and add the following line to it `web: gunicorn flasky:app`. This instructs **Heroku** to find the app instance inside the *flasky.py* file and run a Gunicorn server which is a pure-Python HTTP server for WSGI applications.
* Create the Heroku app using `heroku create <name_of_your_app>`. The output will include a git url for your Heroku application. Copy this as, we'll use it in a moment.
* Add git remote for Heroku to local repositoy using the following command: `git remote add heroku <heroku_git_url>`.
* Add postgresql add on for our database `heroku addons:create heroku-postgresql:hobby-dev --app <name_of_your_application>`.
* Run `heroku config --app <name_of_your_application>` in order to check your configuration variables in Heroku. You will see DATABASE_URL and the URL of the database you just created.
* Push it up! `git push heroku master`.
* Once your app is deployed, run migrations by running: `heroku run python manage.py db upgrade --app <name_of_your_application`>.
## Authors
Yours truly, Osama
## Acknowledgements
The awesome team at Udacity, my family and my close friends.\
This work is a tribute to the soule of my dear friend [Ahmed Alaa](https://www.facebook.com/nickoslavi) who tragically passed away on the 28th of June 2020.\
Rest in peace my dear friend, may Allah bless you.
