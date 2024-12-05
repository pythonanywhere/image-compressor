[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Welcome

Hello. Want to get started with Flask quickly? Good. You came to the right place. This Flask application framework is pre-configured with **Flask-SQLAlchemy**, **Flask-WTF**, **Fabric**, **Coverage**, and the **Bootstrap** frontend (among others). This will get your Flask app up and running on Heroku or PythonAnywhere quickly. Use this starter, boilerplate for all you new Flask projects. Cheers!


Preview the skeleton app here - [http://www.flaskboilerplate.com/](http://www.flaskboilerplate.com/)


### Screenshots

![Pages](https://github.com/realpython/flask-boilerplate/blob/master/screenshots/pages.png)

![Forms](https://github.com/realpython/flask-boilerplate/blob/master/screenshots/forms.png)


### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/realpython/flask-boilerplate.git
  $ cd flask-boilerplate
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)


### Deploying to PythonAnywhere

1. Install [Git](http://git-scm.com/downloads) and [Python](http://install.python-guide.org/) - if you don't already have them, of course.

  > If you plan on working exclusively within PythonAnywhere, which you can, because it provides a cloud solution for hosting and developing your application, you can skip step one entirely. :)

2. Sign up for [PythonAnywhere](https://www.pythonanywhere.com/pricing/), if you haven't already
3. Once logged in, you should be on the Consoles tab.
4. Clone this repo:
  ```
  $ git clone git://github.com/realpython/flask-boilerplate.git
  $ cd flask-boilerplate
  ```

5. Create and activate a virtualenv:
  ```
  $ virtualenv venv --no-site-packages
  $ source venv/bin/activate
  ```

6. Install requirements:
  ```
  $ pip install -r requirements.txt
  ```

7. Next, back on PythonAnywhere, click Web tab.
8. Click the "Add a new web app" link on the left; by default this will create an app at your-username.pythonanywhere.com, though if you've signed up for a paid "Web Developer" account you can also specify your own domain name here. Once you've decided on the location of the app, click the "Next" button.
9. On the next page, click the "Flask" option, and on the next page just keep the default settings and click "Next" again.
Once the web app has been created (it'll take 20 seconds or so), you'll see a link near the top of the page, under the "Reload web app" button, saying "It is configured via a WSGI file stored at..." and a filename.  Click this, and you get to a page with a text editor.
10. Then update the following lines of code:

  from

  ```
  project_home = u'/home/your-username/mysite'
  ```

  to

  ```
  project_home = u'/home/your-username/flask-boilerplate'
  ```

  from

  ```
  from flask_app import app as application
  ```

  to

  ```
  from app import app as application
  ```

11. Save the file.
12. Back on the Web tab, scroll down to the "Virtualenv" section, and click on the "Enter path to a virtualenv, if required" link.  In the input that pops up, enter `/home/your-username/flask-boilerplate/venv` (changing "your-username" appropriately) and hit return.
13. Click the green "Reload" button at the top of the page.
14. Go to the website http://your-username.pythonanywhere.com/ (or your own domain if you specified a different one earlier), and you should see something like this - [http://www.flaskboilerplate.com/](http://www.flaskboilerplate.com/).

*Now you're ready to start developing!*

### Learn More

1. [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/python)
2. [PythonAnywhere - Help](https://www.pythonanywhere.com/help/)
1. [Flask Documentation](http://flask.pocoo.org/docs/)
2. [Flask Extensions](http://flask.pocoo.org/extensions/)
1. [Real Python](http://www.realpythonfortheweb.com) :)

