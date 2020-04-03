# XenonChecker
The Ultimate Subjective Answers Checker - INT 404 Project

[![Maintenance](https://img.shields.io/badge/Maintained%3F-YES-blueviolet.svg)](#)
[![GPLv3 license](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Generic badge](https://img.shields.io/badge/Stable-YES-<COLOR>.svg)](#)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](#)
[![forthebadge](https://forthebadge.com/images/badges/makes-people-smile.svg)](#)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-electricity.svg)](#)
[![forthebadge](https://forthebadge.com/images/badges/ages-12.svg)](#)



#### SUPPORT THE WORK & DEV

[![GitHub stars](https://img.shields.io/github/forks/satyajiit/XenonChecker?style=social)](https://github.com/satyajiit/XenonChecker/network) &nbsp;
[![GitHub stars](https://img.shields.io/github/stars/satyajiit/XenonChecker?style=social)](https://github.com/satyajiit/XenonChecker/stargazers)
&nbsp;
[![GitHub followers](https://img.shields.io/github/followers/satyajiit?style=social&label=Follow&maxAge=2592000)](https://github.com/satyajiit?tab=followers)

### USPS & FEATURES

* Flask
* Responsive Material Design
* Add new questions on the go.
* Analysis of newly added questions

### DEPENDENCY

* Rake_nltk
* Flask

### STEPS TO RUN ON LOCAL SYSTEM

#### STEP1:
Get the following dependencies:
```
pip install rake-nltk
pip install PyDictionary
pip install flask
pip install nltk
```
#### STEP2:
Download nltk Data if not done:
```
python -m nltk.downloader all
```

#### STEP3:
Thats it 😉
```
python app.py
```


### DEPLOY TO FIREBASE HOSTING WITH CLOUD RUN
Want to deploy on firebase hosting?
CloudRun will make it possible by providing a CDN.

#### STEP1:
Create a direcory structure of the following (Create files manually like firebase.json etc which do not exist on this repo):
```
XenonChecker (root dir)
├── server
| ├── src
|    └── app.py
|    └── templates
|       └── all files like index.html 
|    └── static
|        └── all files like js 
| ├── Dockerfile
├── static
|  └── leave empty
├── firebase.json
├── .firebaserc
```
#### STEP2:
Dockerfile
```
FROM python:3.7

RUN pip install Flask gunicorn
RUN pip install rake-nltk
RUN pip install nltk
RUN pip install PyDictionary

COPY src/ app/
WORKDIR /app

RUN python -m nltk.downloader all -d /usr/local/nltk_data

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 8 app:app
```
#### STEP3:
From Server dir execute the following (Make sure you have performed gcloud init and set the project id):
```
gcloud builds submit --tag gcr.io/[PROJECT-ID]/[ANY_NAME_OF_SERVICE]
//Hit yes if asked to enable APIs

gcloud run deploy --image gcr.io/[PROJECT-ID]/[ANY_NAME_OF_SERVICE] --memory 1G
//Select fullyManaged Cloud run and region to us-central1
```
#### STEP4:
Setup Firebase files:
.firebaserc
```
{
    "projects" :{
        "default" : "xenonchecker"
    }
}
```
firebase.json
```
{

"hosting" : {

    "public" : "static",
    "ignore" : [
        "firebase.json"
    ],
    "rewrites" : [{
"source" : "**",
"run" : {

    "serviceId" : "[ANY_NAME_OF_SERVICE]"
}
    }]
}

}
```
#### STEP5:
Deploy on firebase hosting:
```
firebase deploy --only hosting  
```

* Feel free to reach me , if you are stuck!

### SCREENSHOTS FROM MOBILE
<img src="/screenshots/1.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;
<img src="/screenshots/2.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;

<img src="/screenshots/3.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;
<img src="/screenshots/4.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;

<img src="/screenshots/5.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;
<img src="/screenshots/6.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;

<img src="/screenshots/7.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;
<img src="/screenshots/8.jpg" height="617" width="400" />&nbsp;&nbsp;&nbsp;&nbsp;






#### Lots of Hardwork has been made on this project
[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://satyajiit.xyz)
[![GitHub followers](https://img.shields.io/github/followers/satyajiit?style=social&label=Follow&maxAge=2592000)](https://github.com/satyajiit?tab=followers)
