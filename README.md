# MRKT-DATA-ANALYTICS
```
Service to expose APIs that collect data from multiple front ends. Data runs through the service and inserted into BigQuery for further analysis.

This is service is hosted Google's Compute Engine and uses Docker, Flask, and Python to run. 
``` 

## Setup locally
* CD into repo
* `pipenv shell`
* `pipenv install`
* `ENV=dev make build`
* `ENV=dev make run`

## Deployment
* make build ENV=dev|prod
* make deploy ENV=dev|prod
   
## Stack
* Python3
* Docker
* Flask

## Commands
* `<environment>` = dev | prod
* `ENV=<environment> make build`  -  Build the project
* `ENV=<environment> make run`  -  Run / Serve the project
* `ENV=<environment> make deploy`  -  Deploy the project to GCP
* `ENV=<environment> make logs` - See the logs from the container
   
## Refactor from mrkt-data-analytics
* reduced dependencies
* eliminate repeated code
* latest version on all dependencies
* moved to v1-dev-main
