SERVICE := mrkt-data-analytics

ifeq ($(ENV),)
$(error ENV needs to be defined. e.g.: make deploy ENV=dev)
endif

build:
	docker build -t $(SERVICE) .

run: build
	docker run -it -p 8080:8080 $(SERVICE)

deploy:
	gcloud app deploy app.$(ENV).yaml --project=v1-dev-main --version=$(shell date +%Y%m%d-%H%M)

logs:
	gcloud app logs tail \
		--service=$(SERVICE) \
		--version=`gcloud app instances list --project=v1-dev-main | grep $(SERVICE) | awk '{print $$2}'` \
		--project=v1-dev-main \
		| grep -v '/health-check'