
![](https://static.tickets-platform.com/img/pages/39/2131/255/media/2/desktop/image_group-4.jpg?ts=1567173136)

# Formula One Dashboard
Repository containing all the ressources used to create a dashboard using Formula One data carried out as part of an advanced programming course.

## Table of content

## Motivations

## Setting everything up

This project has been made under a Windows OS. For Linux / Mac User feel free to check by yourself the documentation related to your own explotation system.
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

```bash

def app_path():

    app_path = r'...\Plotly_Dash_F1_App'


    return str(app_path)

def data_path():

    data_path = r'...\Plotly_Dash_F1_App\data'
    
    return str(data_path)

```

Last but not least, be sure that all the files dowloaded are located in the same single file on your computer, otherwise the application cannot be launched.

## Time to run the app 

To access to the application, open the 'index.py' file in your favorite IDE and simply run the whole script.

Then copy/paste ( with mouse ! using ctrl-c will stop running the application ) the http link provided into your web browser.

You can also lauch the appication using the command prompt :

Open the command prompt by typing 'cmd' in the path where the 'Plotly_Dash_F1_app' is location then use the command line:

```bash
python index.py
```


