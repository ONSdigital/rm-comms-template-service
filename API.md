# Communications Template Service Api

This page documents the Communications Template service API endpoints

## Classification Types
The following endpoints are associated with the classification types that are used to specify which template to use when communicating.

### Create a classification type

* `POST /classificationtypes/GEOGRAPHY`

### Delete a classification type

* `DELETE /classificationtypes/GEOGRAPHY`

### GET a classification type

* `GET /classificationtypes/GEOGRAPHY` will return the classification type or None if it doesn't exist.

### GET all classification types

* `GET /classificationtypes` will return a list of all classification types

## Communications Templates

## Create a template

* `POST /templates` with a valid template object in the request json.

## Delete a template

* `DELETE /templates/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87`

## Update a template

* `PUT /templates/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87` with a valid template object in the request json.

## Get a template by classifiers

* `GET /templates?REGION=NI` will return a communications template which matches, REGION=NI. 
Example Response
```json
{
 "classification": {
  "REGION": "NI"
  }, 
"id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89", 
"label": "test data", 
"params": "", 
"type": "EMAIL", 
"uri": "test-uri.com"}

```
## Get a template by id

* `GET /templates/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87` will return the template object which matches the template id or None if it doesn't exist.
```json
{
 "classification": {
  "GEOGRAPHY": "NI"
 }, 
"id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89", 
"label": "test data", 
"params": "", 
"type": "EMAIL", 
"uri": "test-uri.com"
}

```
