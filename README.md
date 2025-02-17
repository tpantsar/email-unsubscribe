# Python-Email-Auto-Unsubscribe

## .env file

```shell
EMAIL=""
PASSWORD=""
```

## Claim App Password for your email

Go to [Google Account](https://myaccount.google.com/), search for "App Passwords" and create a new one for your email.
Paste the code in the .env file.

## Virtual environment, dependencies and running the script

```shell
python -m venv .venv
source .venv/Scripts/activate # Windows / MacOS
source .venv/bin/activate # Linux

pip install -r requirements.txt
python main.py
```

## Resources

- [Google Account](https://myaccount.google.com/)
