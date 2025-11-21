# InventoryHub Docker Setup

This guide shows how to run InventoryHub using Docker.

## 1. Clone the repository

```bash
git clone https://github.com/aryan-kazemian/InventoryHub.git
cd InventoryHub
```

## 2. Configure the .env file

After cloning, the repository already includes a `.env` file. You just need to update the values:

```env
SECRET_KEY="DjangoSecretKey"
DB_NAME=InventoryHubDatabase
DB_USER=postgres
DB_PASSWORD=YourLocalPassword
DB_HOST=db
DB_PORT=5432
```

Assign the appropriate values for your local environment.

## 3. Build and run with Docker

```bash
docker-compose up --build
```

First run builds the images, creates the database, and applies migrations.

Access Django at [http://localhost:8000](http://localhost:8000)

## 4. Stop the project

```bash
docker-compose down
```
