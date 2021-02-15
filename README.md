# Table of Contents
***
1. [Technologies](#technologies)
2. [Installation](#installation)
3. [Design](#design)
4. [Future work](#future-work)
5. [Time taken](#time-taken)
***
# Technologies
### List of technologies used within the project:
- Python 3.9
- flask (version 1.1.2)
- pytest (version 6.2.2)
- requests (version 2.25.1)
***
# Design
The Initial design of the service was based on the Factory method pattern, however, because of the requirement to support a fallback strategy in case of providers' failure, the "Chain of responsibility" behavioral pattern was selected for a more scalable solution.
***
# Run
### In order for the application to Run, the following steps must be performed:
1. `$python3 -m venv venv`
2. `$source venv/bin/activate`
3. `$pip3 install -r requirements.txt`
4. `$python3 ./run.py`
***
# Future work
### TODO things, that are missing from the current deliverable:

- Write more extensive unit and integration tests
- Add PythonDoc blocks for classes, methods, and functions
***
##### * Time taken
The implementation took approximately 5 days of development from which including:
- 2 days to get familiar with the framework and the tools used (how things work, research documentation, experiments)
- 3 days spent in the design, implementation, and testing
