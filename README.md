# RVMe
 [![travis](https://travis-ci.com/nykotar/rvme.svg?branch=master)](undefined)
 [![codecov](https://codecov.io/gh/nykotar/rvme/branch/master/graph/badge.svg?token=CXHZU7XTEZ)](undefined)


RV Me is a modern target pool website for remote viewers. It was created to solve common issues with today's target pools and to provide viewers with the best tools for training and practice.

The website was built around the concept of a collaborative target pool. This means that the pool was not put together a single person or group, but anyone is free to contribute with their own target. With this model, we hope to achieve a bigger quantity and variety of targets than common target pools. Every target must be approved before added to the pool, and every target has a difficulty level, description, tasking, and additional feedback - which allows viewers not only to train with proper tasking, but also find more feedback when needed.

RV Me is currently in beta and features difficulty level selection, precognitive mode (target is selected at the time of reveal), target sharing with public link and personal targets (encrypted private pool for viewing personal targets). In addition, the app doesn't let viewers get the same target twice.

RV Me is free and maintained by the moderators of [r/remoteviewing](https://reddit.com/r/remoteviewing).

[rvme.app](https://rvme.app)

## Features

* Three difficulty levels (beginner, intermediate and advanced)
* Additional feedback
* Precognition mode
* Personal targets
* The same target is not given twice
* Target share link
* Modern minimalist design
* (Planned) Localization

## Contributing

There are many ways to contribute to RV Me. Whether if it's a bug report, suggestion, pull request or simply uploading targets, any help is very appreciated. We would like this to be a project built by the community, for the community - getting involved and sharing your thoughts and experiences is very important in order to push this project forward. Join the discussion in [r/remoteviewing's discord server](https://discord.gg/4sWvxzN).

# Running the project for development

Clone the repository and:

```
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

# License
[GNU AGPLv3](https://github.com/nykotar/rvme/blob/master/LICENSE)