.PHONY: build run clean

build:
	docker build -t mlops-task .

run:
	docker run --rm mlops-task

clean:
	rm -f metrics.json run.log