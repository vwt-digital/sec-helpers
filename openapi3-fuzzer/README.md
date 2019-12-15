# Simple fuzzer for OpenAPI 3 specification based APIs

## What does this fuzzer do?

1. Sends various attack patterns to all the endpoints
2. Verifies if the response matches those defined in the OAS3 spec file and complains if it doesn't
3. Complains loudly if an endpoint returns an internal server error (status code 500 and higher)

## Why does this OpenAPI fuzzer exist?

Because it's much easier to integrate into a CICD pipeline, being written in Python and open-source.

It was also quicker to write this than to figure out how other fully featured and complex OAS3 supporting security tools like SoapUI from Smartbear, AppSecInsight from Rapid7 or OWASP ZAP work in a CICD pipeline. 

## How do I use this?

1. git clone
2. virtualenv venv
3. source venv/bin/activate
3. python openapi3-fuzzer.py --help
    ````
    usage: openapi3-fuzzer.py [-h] [--auth AUTH] base_url

    positional arguments:
    base_url     Base URL of the OAS3 API, e.g. https://dev.myapi.example,
                without trailing slash

    optional arguments:
    -h, --help   show this help message and exit
    --auth AUTH  Authorization header field, e.g. "Bearer longbase64string", or
                "Basic shortb64string"
    ````

## What OAS3 definitions are actually supported?

1. GET requests to URL's with or without path parameters
1. POST requests to URL's with or without path parameters
2. POST requestBody schemas in application/json containing:
    * string
    * integer

## Example output

Internal server error:

````
GET fuzzing /managers/expenses/{expenses_id}/attachments

* INTERNAL SERVER ERROR
  Endpoint returned 500 but expected one of [200]
  GET https://dev.myapi.example/managers/expenses/99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999/attachments
````

Response doesn't conform to the OAS3 spec:

````
--------------------------------------------
GET fuzzing /employees/expenses/{expenses_id}

- Unexpected status code
  Endpoint returned 404 but expected one of [200, 'default']
  GET https://dev.myapi.example/employees/expenses/)$#***^
````

````
POST fuzzing /employees/expenses/{expenses_id}

- Unexpected status code
  Endpoint returned 400 but expected one of [201, 'default']
  POST https://dev.myapi.example/employees/expenses
{
    "amount": "123",
    "cost_type": "123",
    "note": ";sleep 10",
    "transaction_date": "123"
}
````

## LICENSE

GPL3