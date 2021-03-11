# Shorty
"Shorty" is a URL shortener microservice that transforms valid URLs to smaller and frendlier URLs. to achieve that, it integrates with 3rd party URL shortening providers like TinyURL and Bitly.

# Table of Contents
***
1. [Technologies](#technologies)
2. [Design](#design)
3. [Run](#run)
4. [Usage](#usage)
5. [Future work](#future-work)
6. [Time taken](#time-taken)
***
# Technologies
### List of technologies used within the project:
- Python 3.9
- flask (version 1.1.2)
- pytest (version 6.2.2)
- requests (version 2.25.1)
***
# Design
The service implements the "Chain of responsibility" behavioral pattern, supporting a fallback strategy in case of providers' failure
***
# Run
### To run the application using *Venv*, the following steps must be performed:
1. `$python3 -m venv venv`
2. `$source venv/bin/activate`
3. `$pip3 install -r requirements.txt`
4. `$python3 ./run.py`
### To run the application using *Docker*, just excecute the following:
`$bash start.sh`
***
# Usage
Request

"Shorty" can be accessed through a single `Post /shortlinks` endpoint that accepts a JSON payload, following the requirements below:
| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The URL to shorten                 |
| provider | string | N        | The provider to use for shortening |

For example
```json
{
    "url": "https://example.com",
    "provider": "bitly"
}
```
or
```json
{
    "url": "https://example.com"
}
```

Response

For **Valid** requests, the response should look like:

Status code: OK 200

Body:
```json
{
    "url": "https://example.com",
    "link": "https://bit.ly/8h1bka"
}
```
For **Invalid** requests, depending on the type of the error, the response should look like:

Status code: 422 UNPROCESSABLE ENTITY

Body:
```json
{
    "message": "'provider' expected to be one of 'tinyurl, bitly'"
}
```
***
# Future work
### TODO things, that are missing from the current deliverable:
- Enhance providers' testing (add mocks)
- Write more extensive unit and integration tests
- Add PythonDoc blocks for classes, methods, and functions
