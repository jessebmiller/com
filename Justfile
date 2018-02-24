build_name = "jesse/bmiller.com"
site_name = `cat CNAME`


# Build the environment
build:
	docker build -t {{build_name}} .


# Generate the static files
generate: build
	docker run -v `pwd`/_site:/out {{build_name}}


# deploy to ipfs
deploy: generate
	docker run -d --rm --name ipfs -v `pwd`/_site:/{{site_name}} ipfs/go-ipfs
	sleep 1
	until docker exec ipfs ipfs swarm peers; do echo "Waiting for peers"; sleep 1; done
	docker exec ipfs ipfs add -r {{site_name}}
	docker stop ipfs


stop:
	docker stop ipfs

# Local Variables:
# mode: makefile
# End:
