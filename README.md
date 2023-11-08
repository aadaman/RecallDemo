# RecallDemo
 Recall.ai Demo App

I've pacakaged my Vitrual environment with this.  If you want to use your own, delete the "RecallDemoEnv" folder and run this command to create a new virtual environment.  To use the included one, only run the activation command
python -m venv RecallDemoEnv

From the RecallDemoApp directory, activate the environment
source RecallDemoEnv/bin/activate

Install packages
pip install django
pip install requests

In the RecallDemoApp/RecallDemo/RecallDemo directory, copy local_settings.py.sample to local_settings.py
cp local_settings.py.sample local_settings.py

In local_settings.py, enter your Recall API Key, as well as your Django Secret Key which can be found in settings.py

From the In the RecallDemoApp/RecallDemo/ directory, run the following commands to build out the database:
python manage.py makemigrations RecallDemoApp
python manage.py migrate 

When done, exit the virtual environment with the following command:
deactivate
