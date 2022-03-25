NAME	:= ${IMAGE_NAME}
$(eval TAG:=$(shell git log -1 --pretty=%H))
IMG	:= ${NAME}:${TAG}
LATEST	:= ${NAME}:latest

build:
	docker build -f ./Dockerfile -t ${IMG} .
	docker tag ${IMG} ${LATEST}

push:
	@docker push ${NAME}

login:
	@docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
