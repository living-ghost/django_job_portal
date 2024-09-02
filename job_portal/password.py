import os

def password():
    EMAIL_PWD_DEV = os.getenv('EMAIL_PWD')
    # Accumulate characters into a new string
    reconstructed_password = "".join([i for i in EMAIL_PWD_DEV])
    print(reconstructed_password)