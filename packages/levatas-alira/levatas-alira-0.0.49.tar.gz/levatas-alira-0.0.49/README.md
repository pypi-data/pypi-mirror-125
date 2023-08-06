# alira

## Running the test suite

To run the test suite, you can follow the instructions below:

1. Create a `.env` file in the root of the project with your AWS credentials
2. Create and activate a virtual environment
3. Install the requirements from the `requirements.txt` file
4. Run the tests using `pytest`.

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ pytest -s
```

Here is an example of the `.env` file:

```
AWS_ACCESS_KEY_ID=<your access key>
AWS_SECRET_ACCESS_KEY=<your secret key>
AWS_REGION_NAME=<your region>
```

To run the AWS integration tests:

```shell
$ pytest -s -m aws
```

