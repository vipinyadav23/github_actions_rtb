test:
	python -m pytest -q

docker-build:
	docker build -t genai-cicd-demo:local .

docker-run:
	docker run --rm -p 8080:8080 genai-cicd-demo:local
