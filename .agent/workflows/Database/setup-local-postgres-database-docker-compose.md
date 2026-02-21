---
description: Quick setup for a local Postgres database using Docker
---

1. **Install Docker Desktop**:
   - If you don't have Docker installed, download and install Docker Desktop for your OS.
   // turbo
   - Run `open https://www.docker.com/products/docker-desktop/`

2. **Create `docker-compose.yml`**:
   - Create a `docker-compose.yml` file in your project root.

   ```yaml
   version: '3.8'
   services:
     db:
       image: postgres:16-alpine
       restart: always
       environment:
         POSTGRES_DB: mydatabase
         POSTGRES_USER: myuser
         POSTGRES_PASSWORD: mypassword
       ports:
         - "5432:5432"
       volumes:
         - db_data:/var/lib/postgresql/data
   volumes:
     db_data:
   ```

3. **Start Database**:
   - Navigate to your project root and start the Docker containers.
   // turbo
   - Run `docker-compose up -d`

4. **Connect to Database**:
   - Use a client like `psql`, `DBeaver`, or `TablePlus` with:
     - Host: `localhost`
     - Port: `5432`
     - User: `myuser`
     - Password: `mypassword`
     - Database: `mydatabase`

5. **Pro Tips**:
   - To stop the database: `docker-compose down`.
   - To remove all data (use with caution!): `docker-compose down -v`.
   - Add `docker-compose.yml` to your `.gitignore` if you don't want to commit it.
