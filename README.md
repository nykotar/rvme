# RVMe
 [![travis](https://travis-ci.com/nykotar/rvme.svg?branch=master)](undefined)
 [![codecov](https://codecov.io/gh/nykotar/rvme/branch/master/graph/badge.svg?token=CXHZU7XTEZ)](undefined)


RVMe is an open source collaborative target pool website for remote viewers. 

It currently features categories of targets and precognitive mode where the target is selected at the time of reveal. The target pool is built by the community, users can upload their targets and if approved, they are added to the pool. [rvme.app](https://rvme.app).

RVMe is free and maintained by the moderators of [r/remoteviewing](https://reddit.com/r/remoteviewing).

## Features

* Six categories of targets
* Description, for additional feedback
* Precognition mode
* Personal targets
* The same target is not given twice
* Modern minimalist design
* (Planned) Localization

## Contribute

There is a lot to be done, any help is appreciated. Please see the issues if you are interested in contributing. If you want to chat [join our Discord](https://discord.gg/4sWvxzN).

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