# Financial Control Project

This project is a financial control system with AI agent integration via WhatsApp and Telegram.

## Project Structure

```
├── app/                          # Main application code
│   ├── api/                      # API endpoints
│   ├── core/                     # Core functionality
│   ├── models/                   # Database models
│   ├── services/                 # Business logic services
│   └── tools/                    # Utility tools
├── config/                       # Configuration files (ignored by git)
├── notebooks/                    # Jupyter notebooks for development
├── scripts/                      # PowerShell scripts for database operations
│   └── restore_from_supabase.ps1 # Database migration script
├── docker-compose.yml            # Docker services configuration
├── Dockerfile                    # Application container definition
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## Quick Start

### Prerequisites
- Docker Desktop installed ([download aqui](https://www.docker.com/products/docker-desktop))
- PostgreSQL CLI tools (para operações de banco)

### Ambientes suportados
- **Local (VSCode debug)**: app rodando localmente, DB pode estar em Docker ou local
- **Dev (Docker Compose)**: API + DB + pgAdmin + ngrok em containers
- **Production**: deploy em servidor/container com variáveis CI/CD

### Principais variáveis de ambiente
- `APP_ENV`: local | development | production
- `DATABASE_URL`: postgresql://user:password@host:5432/financial_control
- `CONVERSATION_ENCRYPTION_KEY`
- `SITE_CONFIG_URL`

### Environment Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ControleFinanceiro
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. **Start all services**
```bash
docker-compose up -d
```

This will automatically start:
- **Flask API** on `http://localhost:5000`
- **PostgreSQL Database** on `localhost:5432`
- **pgAdmin** (Database viewer) on `http://localhost:5050`
- **ngrok** (Public tunnel) on `http://localhost:4040`

## Database Setup

### Database Migration (Supabase → Local Docker)

To copy your production database (Supabase) to your local development environment:

#### Automatic Script (Recommended)

1. **Ensure your `.env` file is configured** with Supabase credentials
2. **Run the migration script**:
```bash
# Windows PowerShell
.\scripts\restore_from_supabase.ps1
```

#### Script Features

- ✅ **Automatic dump** from Supabase using environment variables
- ✅ **Progress feedback** with status messages
- ✅ **Error handling** with detailed messages
- ✅ **Uses SQL format** for compatibility
- ✅ **Backup file preservation** for safety

#### Prerequisites

- PostgreSQL CLI installed (`pg_dump` command available)
- Docker containers running (`docker-compose up -d`)
- Supabase credentials configured in `.env` file

#### Manual Steps (Alternative)

```bash
# 1. Dump from Supabase
pg_dump --dbname $SUPABASE_HOST --format plain -f supabase_backup.dump

# 2. Copy to Docker container
docker cp supabase_backup.dump controlefinanceiro-db-1:/tmp/

# 3. Restore in local database
docker exec -it controlefinanceiro-db-1 psql -U user -d financial_control -f /tmp/supabase_backup.dump
```

```bash
# Windows PowerShell
.\migrate-db.ps1

# Or with custom parameters
.\migrate-db.ps1 -SupabaseHost "your-host.supabase.co" -SupabaseUser "postgres"
```

#### Option 2: Manual Steps

```bash
# 1. Dump from Supabase
pg_dump -h db.banvuekhactuvueikbny.supabase.co -U postgres -d postgres -F c -f supabase_backup.dump

# 2. Copy to Docker container
docker cp supabase_backup.dump controlefinanceiro-db-1:/tmp/

# 3. Restore in local database
docker exec -it controlefinanceiro-db-1 pg_restore --clean -U user -d financial_control -v /tmp/supabase_backup.dump
```

#### Script Features

- ✅ **Automatic dump** from Supabase
- ✅ **Clean restore** (removes existing data)
- ✅ **Progress verification** (counts records)
- ✅ **Error handling** with detailed messages
- ✅ **Backup file preservation** for safety

#### Prerequisites

- PostgreSQL CLI installed (`pg_dump` command available)
- Docker containers running (`docker-compose up -d`)
- Supabase credentials in `.env` file

## Integration Setup

### WhatsApp Integration (Twilio)

### Step 1: Start the Project
```bash
docker-compose up
```

### Step 2: Get the Public URL
After about 5-10 seconds, open **ngrok dashboard** at:
```
http://localhost:4040
```

Look for the **Forwarding** line (similar to):
```
https://1234-5678-90ab.ngrok.io -> http://localhost:5000
```

Copy the HTTPS URL (e.g., `https://1234-5678-90ab.ngrok.io`)

### Step 3: Configure in Twilio

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging** → **WhatsApp** → **Sandbox Settings**
3. Paste your ngrok HTTPS URL + your webhook endpoint in the **When a message comes in** field:
   ```
   https://1234-5678-90ab.ngrok.io/api/v1/whatsapp/webhook
   ```
4. Set method to **HTTP POST**
5. Save and test with WhatsApp

### Telegram Integration

The project also supports Telegram integration. Configure your Telegram credentials in `config/telegram_credentials.json`:

```json
{
    "app_id": "your-telegram-app-id",
    "api_hash": "your-telegram-api-hash",
    "AppTitle": "AgenteFinanceiro"
}
```

**Note:** Telegram credentials are stored in the `config/` directory which is ignored by git for security.

---

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Configure these variables:

### Database Configuration
- `SUPABASE_HOST`: Supabase connection string (format: `postgresql://user:password@host:port/database`)
- `SUPABASE_USER`: Supabase username (usually `postgres`)
- `SUPABASE_DB`: Supabase database name (usually `postgres`)

### Local Database Configuration
- `CONTAINER_NAME`: Docker container name (default: `controlefinanceiro-db-1`)
- `DB_USER`: Local PostgreSQL username (default: `user`)
- `DB_NAME`: Local database name (default: `financial_control`)

### External Services
- `NGROK_AUTHTOKEN`: (Optional) Your ngrok auth token for persistent URLs ([get here](https://dashboard.ngrok.com/auth))
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio WhatsApp sandbox number

### Telegram Configuration (if used)
- Telegram credentials should be placed in `config/telegram_credentials.json` (ignored by git)

---

## Accessing the Database

### Via pgAdmin (Recommended)
1. Open `http://localhost:5050`
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin`
3. Add a connection to PostgreSQL:
   - Host: `db`
   - Port: `5432`
   - Username: `user`
   - Password: `password`
   - Database: `financial_control`

### Via Command Line
```bash
psql -h localhost -p 5432 -U user -d financial_control
```

## Development

### Code Standards

- Code can be in Portuguese, but comments must be in English
- Follow Pylint standards (configuration in `.pylintrc`)
- No redundant code, follow naming conventions, avoid memory waste

### GitHub Actions

PRs to development, qa, and main branches will run CI with Pylint checks.

### Database Schema

The database schema includes the following main tables:

- **bancos** - Bank information
- **cartoes** - Credit/debit cards
- **categorias** - Transaction categories
- **entradas_realizadas** - Income entries
- **saidas_realizadas** - Expense entries
- **compras_cartoes** - Card purchases
- **faturas_cartoes_de_credito** - Credit card bills
- **limites_de_compras** - Purchase limits
- **historico_de_mensagens** - Message history (WhatsApp/Telegram)
- **logs** - Application logs
- **research** - Research queries

### API Endpoints

The Flask API provides endpoints for:
- Financial data management
- AI agent interactions
- WhatsApp/Telegram webhooks
- Database operations

Base URL: `http://localhost:5000/api/v1/`

## Troubleshooting

### Common Issues

1. **Port already in use**: Make sure no other services are running on ports 5000, 5432, 5050, or 4040
2. **Database connection failed**: Ensure Docker containers are running with `docker-compose ps`
3. **Migration script fails**: Check your `.env` file has correct Supabase credentials
4. **ngrok tunnel not working**: Check your internet connection and ngrok auth token

### Useful Commands

```bash
# View running containers
docker-compose ps

# View container logs
docker-compose logs [service-name]

# Restart services
docker-compose restart

# Clean up (remove containers and volumes)
docker-compose down -v

# Rebuild containers
docker-compose up --build
```