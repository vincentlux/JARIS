# JARIS
Just Another Really Intelligent System

# How to


## Installation
### For backend Flask API:

`pip install -r requirements.txt` 

### For frontend framework (Vue.js):

`cd ./app` 

`npm install`

### For socket.io (speech):
`cd ./app/speech-ws` 

 `npm install`


## Run 

### Start Flask api

`cd api`

`python app.py`

### Start Vue.js

`cd app`

`npm run dev`

### Start socket.io

`cd app/speech-ws`

`node app`
* __You need to:__
    * __Generate Google speech api json file from [here](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries)__
    * __Put generated json file under app/speech-ws__
    * __insert your own json filename into app.js after `keyFileName`__  


## For solr indexing (only need to do one time to set up as a service)
`cd ./solr`

`python csv_xml.py` to convert all csv instance into xml 

To make a new core:
* log into server and `sudo su - solr -c "/opt/solr/bin/solr create -c jaris"`

To add fields:
`bash schema.sh`

