curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"id","type":"text_general","stored":true }}' http://104.248.61.45:8983/solr/jaris/schema
curl -X POST -H 'Content-type:application/xml' --data-binary '{"add-field":{"name":"content","type":"string","stored":true }}' http://104.248.61.45:8983/solr/jaris/schema
