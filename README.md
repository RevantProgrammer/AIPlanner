This is a project to help automate planning for businesses using AI.


How to use:
1. Create a virtual environment and download all dependencies in **environment.yaml** file
2. Create a .env file by following the scaffold in **.env.example**
3. Make and add your 'Ollama' or any other LLM API Key inside the **.env** file
4. If you change any keys in the **.env** file, ensure to replicate those changes in _config/settings.py_
5. Add your Google **credentials.json** inside _credentials/_ directory
6. Make a `users.yaml` file inside the _auth/_ directory.
7. Using the `sign_up.py` script in models, create a login. Remember username and password. 
8. While still in the same respository, run the command: `streamlit run app.py`
9. Test the project out! :)