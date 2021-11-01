
![](https://static.tickets-platform.com/img/pages/39/2131/255/media/2/desktop/image_group-4.jpg?ts=1567173136)

# Formula One Dashboard
Repository containing all the ressources used to create a dashboard using Formula One data carried out as part of an advanced programming course.

## Table of content

  * [Motivation](#motivation)
  * [Setting everything up](#setting-everything-aspect)
  * [Requirements](#requirements)
  * [Time to run the app](#time-to-run-the-app)


## Motivations

As a Formula One amator, I was interested in creating a simple dashboard to play with a little part of the huge amount of data the formula one api is providing. As part of my master 2's advanced programming course, I decided to construct this project by using mainly Dash (and Plotly) libraries that I've never used before.

I tried to implement some interesting graphs and features but I know that a lot of improvments are possible.

NB : I got inspired a lot by the work made by Christopher Jeon. You can find his work and his public statistics app about Formula One here : https://github.com/christopherjeon/F1STATS-public

## Setting everything up

This project has been made under a Windows OS. For Linux and Mac Users feel free to check by yourself the documentation related to your own explotation system.
Note that I cannot guarantee that the application works perfectly under other exploitation systems as it does under Windows.

The whole application has been coded using python 3.8.5 so be sure to update your python version if you are using an older one.

To check your current version on python simply open your command prompt and use the following command : 

```bash
python --version
```

If your version of python is older than the 3.8.5, I strongly recommand you to update your version of python before running the application's script.

## Requirements

Before runing the app you will have to install ( or atleast update ) all python's module listed in the requirements.txt file that you can find in the repository.

You will also need to set up your own path for the 'app' folder and for the 'data' folder.

Simply open the 'path_.py' file in a text editor or your favorite IDE and replace the three dots bewteen quotation marks with your own path as follow : 

```diff
-You will also need to set up your own path for the 'app' folder and for the 'data' folder.
-Simply open the 'path_.py' file in a text editor or your favorite IDE and replace the three dots bewteen quotation marks with your own path as follow : 
```

```bash

def app_path():

    app_path = r'...\Plotly_Dash_F1_App'


    return str(app_path)

def data_path():

    data_path = r'...\Plotly_Dash_F1_App\data'
    
    return str(data_path)

```
```diff
-BE CAREFUL :
-Be sure that all the files dowloaded are located in the same single file on your computer.
-Then in your IDE, change your working directory and choose the Plotly_Dash_F1_App as your current working directory.
```

You're now able to run the app.

## Time to run the app 
```diff
+Download the entire repository zip file, just go to Code -> Download ZIP.
+Extract the Plotly_Dash_F1_App file in the location desired.
+Remember that you will need to set this file as your current working directory in your IDE.
```

To access to the application, open the 'index.py' file in your favorite IDE and simply run the whole section.

Then copy/paste ( use your mouse ! using ctrl-c will stop running the application ) the http link that appears in your console into your web browser.

You can also lauch the appication using the command prompt :

Open the command prompt by typing 'cmd' in the path where the 'Plotly_Dash_F1_app' is location then use the command line:

```bash
python index.py
```


