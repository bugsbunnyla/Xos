.PHONY: install dev build test lint clean deploy

install:
	cd frontend && npm install
	cd backend && pip install -r requirements.txt

dev:
	docker-compose -f docker/docker-compose.yml up -d postgres redis elasticsearch neo4j weaviate
	cd backend && uvicorn app.main:app --reload &
	cd frontend && npm run dev

build:
	cd frontend && npm run build
	docker-compose -f docker/docker-compose.yml build

test:
	cd backend && pytest -v
	cd frontend && npm test

lint:
	cd backend && black . && isort . && flake8
	cd frontend && npm run lint

clean:
	docker-compose -f docker/docker-compose.yml down -v
	rm -rf frontend/.next frontend/node_modules
	find backend -type d -name __pycache__ -exec rm -rf {} +

deploy:
	docker-compose -f docker/docker-compose.yml up -d

logs:
	docker-compose -f docker/docker-compose.yml logs -f

seed:
	cd backend && python scripts/seed_db.py
