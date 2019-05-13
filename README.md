# aqa-python
Project for learning Python language and its application for various test types

## Current 'master' status
[![CircleCI](https://circleci.com/gh/npsmetana/aqa-python/tree/master.svg?style=svg)](https://circleci.com/gh/npsmetana/aqa-python/tree/master)

## Requirements
Python 3.7 or later
Allure 2.11.0 or later

## Usage
- Download project
- Run command shell in the directory where project was downloaded
- Run:
```bash
  python3 -m pytest --alluredir <allure-report-directory>
```
- View report:
```bash 
  allure serve <allure-report-directory>
```

## Used Allure tags
```
- @allure.title
- @allure.step
```
- ```allure.attach``` method used for screenshot saving


## Current progress
### What completed
- Phase1 - Python: beginning
- Phase2 - Work with files
- Phase3 - Selenium tests

### In progress
- Phase4 - Allure reports for tests

### What next
- Phase5 - API tests
- Phase6 - Tests parallel execution
