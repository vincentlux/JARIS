# JARIS
Just Another Really Intelligent System

# Issues to think about:
* Define user group
* Define input speech scope
    1. Medical definition
    2. Usage?
* How to summary

# Todo
<!-- * ~~Google cloud speech api implementation~~ (0203)
* Connect with python backend (0204-0205) -->
* filter stop words (start a new api)



# How to


## Installation
`pip install -r requirements.txt` 

`cd ./app` 

`npm install` all dependencies for Vue.js

`cd ./app/speech-ws` 

 `npm install` dependencies for websocket


## Run 
`cd ./api`

`python app.py` to start flask api


`npm run dev` in `./app` to start Vue.js
* To specify port: `HOST=0.0.0.0 PORT=8080 npm run dev`

`node app` in `./app/speech-ws` to start websocket
* You may need to insert Google Speech API json file into app.js after `keyFileName`  




<!-- ## For search by keyword (test)
1. git clone this repo
2. `pip install -r requirements.txt`
3. `python search.py --test --keyword percutaneous` 
    * `--test`: test mode
    * `--keyword`: keyword you want to search. e.g. `--keyword thermal` -->



## For solr indexing (only need to do one time to set up as a service)
`cd ./solr`

`python csv_xml.py` to convert all csv instance into xml 

To make a new core:
* log in server and `sudo su - solr -c "/opt/solr/bin/solr create -c jaris"`

To add fields:
`bash schema.sh`

