# Project Overview: Vehicle-Interval-model

This repo consists of the **Model deployment** in development/test stage of the [Full-Stack Data Science Project][link]. Deploying  Machine learning model as a RESTful Serverless API leveraging the power of AWS Serverless Architecture like AWS Lambda, EventBridge, and AWS APIGateway using [Zappa][zappa_link] (the python package used for deploying serverless applicaition).

Here, the main branch is used as the production branch while development branch for the development/test purpose.

[link]:https://github.com/Mattobad/Full-Stack-Data-Science

## Technologies used:
**Python Version:** 3.8

**Libraries:** scikit-learn, Flask, flask-cors, numpy, pandas, pytest

**Cloud Technologies:** AWS Lambda, EventBridge, APIGateway

**Other packages:** Zappa, pymake, act

## Environment setup

**Anaconda:** 
```
$ conda create --name ENVNAME python=3.8
$ conda activate ENVNAME
$ pip install -r requirements.txt
```
**VirtualEnv:**
```
$ pip install virtualenv
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Directory Structure
  ``` .
      ├──.github/workflow
      │   └── python-app.yml  
      ├── zappa_app
      │   ├── app   
      │   │   ├── config
      │   │   │   └── config.py
      │   │   ├── trained-model
      │   │   │   ├── low-quantil-model_14_Impfeat.pkl
      │   │   │   ├── mid-quantil-model_14_Impfeat.pkl
      │   │   │   └── up-quantil-model_14_Impfeat.pkl
      │   │   ├── app.py
      │   │   ├── controller.py
      │   │   └── inference.py
      │   ├── tests
      │   │   ├── conftest.py
      │   │   ├── test_config.py
      │   │   ├── test_controller.py
      │   │   └── test_inference.py
      │   ├── Makefile
      │   ├── requirements.txt
      │   ├── run.py
      │   └── zappa_settings.json
      ├── .gitignore
      ├── README.md  
      └── requirements.txt
 ```

## How to run locally after you activate the virtual environment:

Command to execute the code:
```
$ cd zappa_app
$ pymake local_test
```
Command to execute the test suite:
```
$ cd zappa_app
$ pymake test
```

## Deploying Serverless application locally using Zappa
If you would like to deploy the application from your location machine, Unix or Linux Machine can directly use the following steps but for Windows Machine- docker or virtual machine (VirtualBox) is suggested.

```
# remember to activate your virtualenv that we've previously setup
$ pip install zappa
$ cd zappa_app
$ zappa init   
$ zappa deploy dev

```

That's it, easy right. Look into the [Zappa Doc][zappa_link] for further details. Enjoy!!!


## Deploying Serverless application using Zappa through CI/CD with GitHub Actions
To run the CI/CD with GitHub Actions, you can simply choose python application template from Actions (from above menu bar beside Pull requests). Then just modify as below:

1. Setup CI/CD when changes pushed to main branch
  ```
  name: Python application

  on:
    push:
      branches: [ development ]
  ```
2. Virtual machine- setup a ubuntu-latest
  ```
  jobs:
  build:
    runs-on: ubuntu-latest
  ```
 Note: Following are sequential steps after the virtual machine setup.
 
4. AWS Credentials Configuration
  ```
  #steps
    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }} # you can add secrets as constant variable
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    - uses: actions/checkout@v2
  ```
 5. Dependencies and flake8 
 ```
 - name: Set up Python 3.8           # setup python3 version
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies      # install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest
        pip install -r requirements.txt
    - name: Lint with flake8           # check for code quality
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
 ```
 
 6. Test Suites with pytest
 ```
 - name: Test with pytest
      run: |
        cd zappa_app
        pymake test
 ```
 
 7. Zappa deployment
 ```
 - name: Setup Virtual Env                             # setup virtualenv 
      run: |
        pip install virtualenv
        virtualenv ml-app
        source ml-app/bin/activate
        pip install -r requirements.txt zappa==0.52.0   # install dependencies for the application
    - name: Clean Old Deployment                        # Clean previous deployment
      run: |
        source ml-app/bin/activate
        cd zappa_app
        zappa undeploy dev --yes
    - name: Deploy to AWS dev                           # Deploy fresh application
      if: ${{ always() }}
      run: |
        source ml-app/bin/activate
        cd zappa_app
        zappa deploy dev
    - name: Tear Down Zappa on Failure                  # Tear Down incase of failure
      if: ${{ failure() }}
      run: |
        source ml-app/bin/activate
        cd zappa_app
        zappa undeploy dev --yes
 ```
 
 Note: Reasons for cleaning the previous deployment for every new deployment:
- Versioning doesn't play a role in the project as upgraded newer version always replaces the older applicaiton
- Zappa doesn't have single command(at the time of writing) to undeploy and deploy the serverless application which is required for automating the deployment.
  - you can only use `zappa update dev` command if you've already deployed using `zappa deploy dev` command.

You can also run the GitHub Actions locally using the act package. Check out the awesome package through this [link][act_package]. 


Check-out the Serverless application, live through this [link][project].

[zappa_link]: https://pypi.org/project/zappa/
[act_package]: https://github.com/nektos/act
[project]: https://bit.ly/vehicle_prj_live



      
