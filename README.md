# Egor-bot

Telegram bot for nutrition information and food mapping.

## Overview
Egor-bot is a multi-component system consisting of a Telegram bot, an admin interface, and a React-based frontend. It provides users with information about nutrition and food products, likely supporting FODMAP-related dietary needs.

## Stack
- **Language:** Python 3.10+
- **Telegram Framework:** [Aiogram 3.4.0](https://docs.aiogram.dev/)
- **Database:** MySQL 8.0 / SQLAlchemy
- **Frontend:** React (Vite, React Router)
- **Deployment:** Docker, Docker Compose, Nginx, Certbot
- **Admin Panel:** Django (implied by `manage.py` in docker-compose)

## Project Structure
```text
.
├── main.py              # Bot entry point
├── create_obj.py        # Bot and DB initialization
├── handlers/            # Telegram command handlers (client, admin, inline)
├── models/              # Database models
├── features/            # Core logic (search, formatting, etc.)
├── keybords/            # Telegram keyboards
├── inline_butn/         # Inline keyboard buttons
├── middleware/          # Bot middlewares (e.g., user checking)
├── sql_bd/              # SQL connection logic
├── frontend/            # React frontend application
├── Deploy/              # Deployment configurations (Nginx, SSL, DB dumps)
├── docker-compose.yml   # Docker orchestration
└── tests/               # Pytest test suite
```

## Requirements
- Python 3.10+
- Node.js & npm (for frontend)
- Docker & Docker Compose
- MySQL Server (if running locally without Docker)

## Setup & Run

### Local Bot Setup
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory (see [Environment Variables](#environment-variables)).
5. Start the bot:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend/foodmap_front
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run in development mode:
   ```bash
   npm run dev
   ```

### Docker Deployment
1. Ensure `.env` is configured.
2. Create `Deploy/ssl` directory and add your SSL certificates if required.
3. Run with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

## Environment Variables
The following variables should be defined in your `.env` file:

| Variable | Description |
|----------|-------------|
| `TOKEN` | Telegram Bot Token |
| `DB_HOST` | MySQL database host |
| `DB_PORT` | MySQL database port |
| `MYSQL_USER` | MySQL username |
| `MYSQL_PASSWORD` | MySQL password |
| `MYSQL_DATABASE` | MySQL database name |
| `DEBUG` | Set to `True` for polling mode, `False` for webhook mode |
| `WEB_SERVER_HOST` | Webhook server host |
| `WEB_SERVER_PORT` | Webhook server port |
| `WEBHOOK_URL` | Base URL for webhook |
| `WEBHOOK_PORT` | Port for webhook |
| `WEBHOOK_PATH` | Path for webhook |
| `WEBHOOK_SECRET` | Secret token for webhook |
| `ADMIN_APP_PASS` | Path/context for admin app build |
| `FODMAP_APP_PATH` | Path/context for fodmap app build |

## Scripts
- `main.py`: Main entry point for the Telegram bot.
- `win_bot_start.bat`: Batch script for starting the bot on Windows.
- `init_letincrypt.sh`: Script for initializing Let's Encrypt certificates.
- `Deploy/scripts/req_webhook.py`: Script related to webhook configuration.
- `frontend/foodmap_front/package.json` scripts:
  - `npm run dev`: Start Vite development server.
  - `npm run build`: Build frontend for production.
  - `npm run lint`: Run ESLint.

## Tests
The project uses `pytest`.

### Running Tests
1. Install testing dependencies:
   ```bash
   pip install pytest pytest-asyncio mock
   ```
2. Run all tests:
   ```bash
   python3 -m pytest tests/
   ```

Note: The tests use an in-memory SQLite database by default if MySQL connection parameters are not provided in the environment or when running under `pytest`.

## TODO
- [ ] Document specific API endpoints for the frontend.
- [ ] Add license information.
- [ ] Detail the database schema.
- [ ] Add instructions for `Deploy/db_dump`.

## License
TODO: Add license information.

