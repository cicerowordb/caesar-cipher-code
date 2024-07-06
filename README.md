
# A Caesar Cipher Example

This repository contains an example of a Caesar Cipher, an ancient encryption technique. The Caesar Cipher shifts letters by a fixed number of steps in the alphabet. This project is designed to demonstrate basic encryption techniques using Python, Flask, and Docker, along with continuous integration and deployment practices using GitHub Actions. Additionally, the deployment aspect covers a simple Kubernetes setup using K3S in AWS.

### Requirements

* Functional Python3 development environment.
* Functional Docker environment for image build and use (optional).
* GitHub account for workflow execution (optional).
  * This repostory and equivalent [manifests repository](https://github.com/cicerowordb/caesar-cipher-manifests).
  * Include secrets: `secrets.DOCKER_USERNAME`, `secrets.DOCKER_PASSWORD`, and `secrets.MANIFESTS_REPOSITORY_AUTH_URL`.
  * For `secrets.MANIFESTS_REPOSITORY_AUTH_URL` use the format: `https://USER:TOKENT@github.com/cicerowordb/caesar-cipher-pipeline.git`.
* Kubernetes cluster. Using K3S running from AWS (optional).
  * ArgoCD for deployment.
  * Istio and 

### Running locally without Docker

To test and develop locally without the need for Docker, you can set up and run the application directly in your Python development environment. This is particularly useful for developers who want to quickly make changes and test functionalities without going through the process of building Docker images. Follow the steps below to configure and run the application:

```bash
# create virtual environment
python3 -m venv development
source development/bin/activate

# install application requirements
python3 -m pip install -r requirements.txt

# run application
gunicorn --bind 0.0.0.0:5000 --workers 4 index:app

# access and make your manual tests
# check images in the next sections

# stop with control+c

# deactivate virtual environment
deactivate
```

### Building and running with Docker

Build a Docker image of the Caesar Cipher application using the latest codebase and run it locally to ensure everything is packaged correctly.

```bash
# build docker image
docker build -t caesar-cipher:$(head -n1 CHANGELOG.md|tr -d "# ") .

# run docker image
docker run -d --name caesar-cipher -p 5000:5000 caesar-cipher:$(head -n1 CHANGELOG.md|tr -d "# ")

# run a shell inside a container
docker exec -it caesar-cipher bash

# remove docker container
docker rm caesar-cipher --force
```

### Manual tests results

Here are the results from manual testing to demonstrate the functionality of the Caesar Cipher. The tests confirm that the encryption and decryption processes are handled correctly by the application. Below are screenshots showing the application's UI before and after a cipher operation.

* Before send:

  ![before-send](img/doc001.png)

* After send:

  ![after-send](img/doc002.png)

### Manual tests with cURL

Below are several manual test commands using curl to demonstrate the application's response to different inputs and shifts. These commands test the encryption logic with various string inputs and shift values, verifying both the application's functionality and its error handling.

```bash
curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=123abcABC&shift=1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# expected: 234bcdBCD

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=234bcdBCD&shift=-1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# expected: 123abcABC

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=HELLO&shift=2' \
    | grep -E '(Encrypted Text:|HTTP/)'
# expected: JGNNQ

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=staySafe&shift=0' \
    | grep -E '(Encrypted Text:|HTTP/)'
# expected: staySafe

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=abc123!@#&shift=1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# expected: bcd234"A$

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=&shift=1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# expected: 
```

### Running unit tests

Execute the following commands to run unit tests for the Caesar Cipher application. These tests ensure the encryption and decryption functionality works as expected.

```bash
# install test libraries 
pip install -r requirements-test.txt

# run unit tests from the rrepository's root folder
export PYTHONPATH=$PWD
pytest -s
```

### Running static checks

Perform static analysis to ensure code quality, security, and dependency safety using tools Pylint, Safety, and Bandit.

#### Lint with Pylint

Check the Python code for stylistic errors and programming standards. This helps maintain code quality and consistency across the project.

```bash
  pylint --fail-under=9 *.py
```

#### Check dependencies with Safety

Ensure there are no known vulnerabilities in the dependencies specified in the `requirements.txt` file.

```bash
safety check -r requirements.txt
```

#### Check security with Bandit

Perform a security analysis to find common security issues in the Python code. This is important for maintaining a secure application.

```bash
bandit *.py
```
