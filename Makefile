.PHONY: setup up down

setup:
	@echo "Setting up backend and frontend environments..."
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && flutter pub get

# up:
# 	@echo "Starting the backend and frontend..."
# 	@echo "Backend starting..."
# 	cd backend && source venv/bin/activate && uvicorn main:app --reload &
# 	@echo "Frontend starting..."
# 	cd frontend && flutter run
up:
	@echo "Starting the backend and frontend..."
	@echo "Stopping any existing backend..."
	-@pkill -f "uvicorn main:app" || true
	@echo "Backend starting..."
	cd backend && source venv/bin/activate && uvicorn main:app --reload &
	@echo "Frontend starting..."
	cd frontend && flutter run

down:
	@echo "Stopping all processes..."
	killall -9 uvicorn flutter
