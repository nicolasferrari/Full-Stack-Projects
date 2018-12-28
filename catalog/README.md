Place your catalog project in this directory.

### ITEM CATALOG 
This web app is a project for the Udacity FSND Course.

### ABOUT

This project is focus on manage the CRUD operations using a database backend based in SQLAlchemy and the Flask framework to build a Restful architecture that provide the differents functionalities of the App. 
Specifically with this project users can read, create, edit and delete minerals and items within minerals. I have done a research on Wikipedia and other sites to gather some informationn about minerals and it correspondents stones(items) and create a minerals list as well as stones that belong to each mineral groups.

### Dependencies

[Vagrant](https://www.vagrantup.com/)

[Udacity Vagrant File](https://github.com/udacity/fullstack-nanodegree-vm)

[Virtual Box](https://www.virtualbox.org/wiki/Downloads)


### How to install

1-Install Vagrant & VirtualBox
2-Clone the Udacity Vagrantfile
3-Go to Vagrant directory and either clone this repo or download and place zip here
4-Launch the Vagrant VM (vagrant up)
5-Log into Vagrant VM (vagrant ssh)
6-Navigate to cd/vagrant as instructed in terminal
7-The app imports requests which is not on this vm. Run sudo pip install requests
8-Navigate to the catalog directory with cd catalog
8-Setup application database python project_database.py
9-Run the file python populate_database.py with the goal to populate the database with some real data
10-Run application using python application.py
11-Access the application locally using http://localhost:8000

### Authentication with Google log in 
To get the Google login working there are a few additional steps:

1-Go to Google Dev Console
2-Sign up or Login if prompted
3-Go to Credentials
4-Select Create Crendentials > OAuth Client ID
5-Select Web application
6-Enter name 'Minerals-App'
7-Authorized JavaScript origins = 'http://localhost:5010'
8-Authorized redirect URIs = 'http://localhost:5010/login' && 'http://localhost:5010/gconnect'
9-Select Create
10-Copy the Client ID and paste it into the data-clientid in login.html
11-On the Dev Console Select Download JSON
12-Rename JSON file to client_secrets.json
13-Place JSON file in the catalog directory that you cloned from here
14-Run application using python application.py
