
SHELL = /bin/bash

build:
	docker build --tag cog:latest .

shell:
	docker build --tag cog:latest .
	docker run --name docker --volume $(shell pwd)/:/data --rm -it cog:latest /bin/bash

test:
	docker build --tag cog:latest .
	docker run -w /var/task/ --name cog \
		--env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		--env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		--env AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} \
		--env AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
		--env Message='{"url": "https://s3-us-west-2.amazonaws.com/remotepixel-pub/tests/dg_post_yutu/1313020.tif", "bucket": "remotepixel-pub", "key": "tests/dg_post_yutu/1313020_cog.tif"}' \
		-itd cog:latest /bin/bash
	docker exec -it cog bash -c 'python3 -m cog_translator.scripts.cli'
	docker stop cog
	docker rm cog

clean:
	docker stop cog
	docker rm cog

REGION = us-east-1
SERVICE = cog-translator
VERSION = 1.1.0
push:
	eval `aws ecr get-login --no-include-email`
	aws ecr describe-repositories --region ${REGION} --repository-names ${SERVICE} > /dev/null 2>&1 || \
		aws ecr create-repository --region ${REGION} --repository-name ${SERVICE} > /dev/null
	docker build --tag cog-translator:master .
	docker tag cog-translator:master "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${SERVICE}:${VERSION}"
	docker push "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${SERVICE}:${VERSION}"
