up:
	@ docker-compose up --build
down:
	@ docker-compose down -v

worker:
	@ docker-compose logs -f worker
	
test:
	@ docker-compose exec worker python start_workflow.py