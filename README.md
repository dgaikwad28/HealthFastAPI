# HealthFastAPI

## Setup

To set up the project, follow these steps:

- Ensure that you have docker is installed and running on your environment.
- Clone the repository: 
  ```
   git clone https://github.com/healthtechinnovations.git
  ```

- Configure the settings in the settings.py file. Please copy example.env as .env and change based on requirement
  ```
  cp env/example.env env/.env
  ```
- run docker-compose file 
  ```
  docker-compose build --no-cache
  docker-compose up -d
  ```

## Project Structure

### Folder info
- The `app` directory contains the main application code, including routers, models, settings, and main application file.
- The `database` directory contains the database models and session setup.
- The `env` directory contains the environment variables file.
- The `logging.json` file contains the logging configuration.

### Configuration
The application uses environment variables for configuration, which can be set in the `.env` file.

### Database
The application uses SQLAlchemy for database management. Database models are defined in the `database/models.py` file, and the database session is set up in the `database/session.py` file.

## Logging
### application uses a logging configuration defined in the `logging.json` file.


## Endpoints
- `/docs`: Swagger UI documentation for the API.
- `/redoc`: ReDoc documentation for the API.
- `POST /users/`: Create a new user.
- `GET /users/{user_id}/`: Get user details by ID.
- `POST /patients/`: Create a new patient record.
- `GET /patients/{patient_id}/`: Get patient record by ID.
- `POST /physicians/`: Create a new physician record.
- `GET /physicians/{physician_id}/`: Get physician record by ID.
- `POST /records/`: Create a new health record.
- `GET /records/{record_id}/`: Get health record by ID.


## Documentation

### API Documentation

The API documentation is available at the following endpoints:
- /docs: Provides Swagger UI documentation for the API
- /redoc: Provides ReDoc documentation for the API

### Postman Documentation
Please refer to the postman collection in docs to test it locally. 
