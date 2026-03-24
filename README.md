# Financial Control Project

This project is a financial control system with AI agent integration via WhatsApp.

## Development Setup

### Using Docker (Recommended)

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your variables
3. Run `docker-compose up --build` to start the development environment with PostgreSQL and WAHA for WhatsApp testing

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (local for dev, Supabase for prod)
- `TWILIO_ACCOUNT_SID`: Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Twilio phone number for sandbox
- Other variables as needed

## Production Setup

For production, set `DATABASE_URL` to your Supabase instance and remove `WAHA_BASE_URL` to use Twilio.

## Code Standards

- Code can be in Portuguese, but comments must be in English
- Follow Pylint standards
- No redundant code, follow naming conventions, avoid memory waste

## GitHub Actions

PRs to development, qa, and main branches will run CI with Pylint checks.