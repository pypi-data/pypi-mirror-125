# Eugenia's http executor

Method to call http API

## Installation

Use pip:

    pip install ehttp-executor

Please use Python 3.8 and above

## How to use

Create the input dictionary, then invoke the method with these parameters:

- HTTP URL
- Process name
- Input dictionary

Example:

    from ehttp_executor.ehttp_caller import call_python_api

    input_data = {
    "status": "Loaded",
    "statusCode": 404,
    "testDate": "16/07/2030",
    "abruptEnd": True,
    "logs": [
        "Rodrigo logged in",
        "Henry logged in",
        "Rodrigo logged out",
        "Henry logged out"
    ],
    "developers": [
        {
        "name": "Rodrigo",
        "age": 43,
        "logins": [
            {
            "loginInfo": "Login saturday 5AM"
            },
            {
            "loginInfo": "Logout saturday 8AM"
            }
        ]
        },
        {
        "name": "Henry",
        "age": 46,
        "logins": [
            {
            "loginInfo": "Login thursday 9AM"
            },
            {
            "loginInfo": "Logout monday 11AM"
            }
        ]
        }
    ]
    }
    json_output = call_python_api("http://localhost:5000/", "PythonBBasic261020211724", input_data)
    print (type(json_output))
    print (json_output)

