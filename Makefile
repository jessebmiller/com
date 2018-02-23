BUILD_NAME = jesse/bmiller.com


.PHONY: build
build:
	docker build -t $(BUILD_NAME) .


.PHONY: generate
generate: build
	docker run -v $(pwd)/site:/out $(BUILD_NAME)
