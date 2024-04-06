# Box.com application with OAuth and Explorer UI widget

This is a demo application that authenticates against Box.com and then
shows the files and folders for the authenticated user.

Retrieve your Box.com credentials
1. Login to your Box account and click on "Dev Console" in the bottom left.
2. Create a new application using OAuth2.
3. Copy the Client ID and Client Secret.

After cloning the source 
1. Create a Python virtual environment  
    ```
    python -m venv .venv
    . .venv/bin/activate
   ```
2. Install the required dependencies ```pip install -r requirements.txt```
3. Create a instance/settings.py file and add your CLIENT_ID, CLIENT_SECRET and REDIRECT_URI.
  ```#instance/settings.py
    CLIENT_ID='client_id'
    CLIENT_SECRET='client_secret'
    REDIRECT_URI='http://localhost:5000/box-auth'
  ```
4. Run the application ```flask --app flaskr run --debug```
5. Open browser at http://localhost:5000/index.html