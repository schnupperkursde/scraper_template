## What is this?

This repo exists to ease the development of scrapers for schnupperkurs.de.
It has a simple template for a selenium based web scraper and a docker image
which ensures compatibility with our production environment.

## How do I use it?

### Requirements

##### 0. Open a terminal
* Windows: https://www.digitalcitizen.life/ways-launch-powershell-windows-admin
* MacOs: https://www.wikihow.com/Open-a-Terminal-Window-in-Mac
* Ubuntu: https://askubuntu.com/questions/183775/how-do-i-open-a-terminal

##### 1. Install Docker:
* Windows: https://docs.docker.com/docker-for-windows/install/
* MacOs: https://docs.docker.com/docker-for-mac/install/
* Ubuntu: https://docs.docker.com/install/linux/docker-ce/ubuntu/

##### 2. Install docker-compose:
https://docs.docker.com/compose/install/

##### 3. Clone this repository
Execute this command in a terminal to clone the repo in the current directory.

```
git clone https://github.com/schnupperkursde/scraper_template.git
```

### Getting Started

##### 1. Copy the template file
Choose a suitable name and rename the template:
```
cp selenium_template.py my_scraper.py
```

##### 2. Build and start the docker container

```
docker-compose build
docker-compose run scraper
```
#### 3. Execute your script inside the container
```
/workdir # python my_scraper.py
```

#### 4. Implement the scraper
Add the functionality in the function ``` parse``` in your renamed scraper file ```my_scraper.py```
Checkout [example.py](https://github.com/schnupperkursde/scraper_template/blob/master/example.py) for a full scraper example.

### Verify your script
Please ensure the following points:
#### 1. script correctnes
Please ensure that your script correctly extracts the requests data and exports it to an Excel file.
#### 2. script runtime
Please ensure that your script finishes execution reliably within 30 minutes. Scripts taking longer than this will be
cancelled and regarded as erroneous.
#### 3 script indepedence
Please ensure that your scripts only uses libraries and files provided by the docker image.
Please *do not* depend on any files not provided by the docker image.
If you need a library not provided by the docker image, open an issue: https://github.com/schnupperkursde/scraper_template/issues.
#### 4. script reproducibility
Please ensure your script delivers the same result every time executed.
#### 5. correct paths
Please ensure that your script writes to the path '/workdir/output/'. 

## Something is missing in the docker image. What can I do?
Do not hesitate to open an issue: https://github.com/schnupperkursde/scraper_template/issues. 
We will add anything you need.
## Something is wrong with the template. What can I do?
Do not hesitate to open an issue: https://github.com/schnupperkursde/scraper_template/issues. 
We will try to find a solution for your problem.
