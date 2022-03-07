# UserLoginStatus
First install all the requirements
```
pip install -r requirements.txt
```
Then these consecutive steps:
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate --run-syncdb
```
```
python3 manage.py runserver
```
##Then go to link and if you press sign in you will find email authentication.
and here you will find three APIs -
1.Create Api(GET):To view all user details and to unlock any user if locked.
2.Create Api(POST):To create new user and give the token as result for login and other purposes
3.Login Api(POST):It requires the token and password to login.
4.LogoutApi(POST:It requires only the token for that particular user.
