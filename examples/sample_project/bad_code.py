import os

api_key = "sk-demo-hardcoded-secret"
password = "123456"


def run_command(user_input):
    os.system("echo " + user_input)


def calculate(x):
    try:
        print("debug", x)
        return 100 / x
    except:
        return None

# TODO: add unit tests
