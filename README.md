REST API Docs 
REST API designed for authenticated user to view his/her electricity consumptions limits overall as well as view data of authenticated user on daily and monthly basis. This API is designed using Python programming language and SQLite database. 

Python version:  Python3.7

Amount of time spent on this project:  12 hours approx.  


Resource Description:
---------

Open Endpoints
--------------------------------------------------------

Open endpoints require no Authentication.

  •	Login:   GET/login/


Login
--------
Used to collect a Token for a registered User.

URL : /login/

Method : GET

Auth required : NO


Data constraints

{"username": "[valid user name]",     "password": "[password in plain text]" }


Data example

{"username": "a201",     "password": "201" }


Success Response

  Code : 200 OK
  
  Content example
  
{"token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d" }


Error Response

Condition : If 'username' and 'password' combination is wrong.

  Code : 401 UNAUTHORIZED
  
  Content :
  
{ “Could not verify” }





Endpoints that require Authentication
---------------------------------------------------------

Closed endpoints require a valid Token to be included in the header of the request. A Token can be acquired from the Login view above.

Current User related

Each endpoint manipulates or displays information related to the User whose Token is provided with the request

  •	 Limits: GET/limits/

  •	Data:   GET/data/

Limits
---------------------------
Get limits 
Get the minimum and maximum value for date consumption and temperature for monthly and daily data for the given (authenticated) user.


URL: /limits/

Method: GET

Authentication required: YES

Permissions required: None

Success Response

  Code: 200 OK
  
  Content examples
  
For a User with name: 'a201' on the local database where that User has saved a name, id and password information.

{
    "limits": {
        "days": {
            "consumption": {
                "maximum": 59,
                "minimum": 5
            },
            "temperature": {
                "maximum": 31,
                "minimum": -12
            },
            "timestamp": {
                "maximum": "2015-12-30 ",
                "minimum": "2014-09-01 "
            }
        },
        "months": {
            "consumption": {
                "maximum": 1121,
                "minimum": 670
            },
            "temperature": {
                "maximum": 14,
                "minimum": 5
            },
            "timestamp": {
                "maximum": "2015-12-01 ",
                "minimum": "2014-03-01 "
            }
        }
    }
} 





Data
--------------------------------

Data of Current User

Return the requested type and amount of data for the authenticated user 

URL: /data/

Method: GET

Authentication required: YES

Permissions required: None

Success Responses

Condition: Header parameters provided are valid and User is authenticated.

  Code: 200 OK
  
  Content example: Response will reflect back the updated information. 
  
A User with name of 'a201', passing header parameters  ' start=2014-04-01’ & ‘count=8’ & ‘resolution=M':

 {
    "data": [
        [
            "2014-03-01 ",
            1004,
            8
        ],
        [
            "2014-04-01 ",
            822,
            14
        ],
        [
            "2014-05-01 ",
            1110,
            7
        ],
        [
            "2014-06-01 ",
            1076,
            9
        ]
    ]
}  

Error Response

Condition: If provided x-access-token is invalid.

  Code: 401 UNAUTHORIZED
  
  Content example:
  
{
    "message": "Token is invalid!"
} 



