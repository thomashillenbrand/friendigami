# Friendigami

Track every possible hangout combination between your friend group. Add friends, and Friendigami automatically generates all possible combinations (pairs, trios, quads, etc.) so you can check them off as they happen. Includes a Twilio SMS integration so anyone can text in a hangout and the app will log it.

## How It Works

Given a set of friends, Friendigami generates every possible combination of size 2 through N. For example, with friends `TH`, `MW`, and `RZ`, it generates:

| Size | Combinations |
|------|-------------|
| 2 | TH-MW, TH-RZ, MW-RZ |
| 3 | MW-RZ-TH |

Each combination is tracked as **occurred** or **not yet**. The goal: complete them all.

## Features

- **Friend Management** — Add, edit, and delete friends with short unique IDs (e.g. `TH`, `MW`)
- **Auto-Generated Combinations** — All possible groupings are created automatically when friends are added or removed
- **Occurrence Tracking** — Click any combination to toggle its occurred status, with timestamps
- **Filtering** — Filter combinations by group size, occurred status, and specific friends (multi-select dropdown)
- **Progress Tracking** — See how many combinations you've completed out of the total
- **SMS Integration** — Text friend IDs to a Twilio number (e.g. `TH, MW, RZ`) and get a response confirming whether it's a new combination or already logged
- **Self-Hostable** — Dockerized with Cloudflare Tunnel support, designed to run on a Raspberry Pi

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Pydantic
- **Frontend:** Vanilla HTML/CSS/JavaScript (no build step)
- **Database:** SQLite
- **Deployment:** Docker, Cloudflare Tunnel

## Project Structure

```
friendigami/
├── app/
│   ├── main.py                  # FastAPI app with lifespan startup
│   ├── init_db.py               # Database seeding script
│   ├── api/
│   │   ├── routes_friends.py    # Friend CRUD endpoints
│   │   ├── routes_combinations.py  # Combination list/toggle endpoints
│   │   └── routes_twilio.py     # Twilio SMS webhook
│   ├── db/
│   │   ├── base.py              # SQLAlchemy engine and Base
│   │   └── session.py           # Session factory and DI helper
│   ├── models/
│   │   ├── friend.py            # Friend ORM model
│   │   ├── combination.py       # Combination ORM model (with occurred tracking)
│   │   └── friend_combinations.py  # Many-to-many association table
│   ├── repositories/
│   │   ├── friend_repository.py
│   │   └── combination_repository.py
│   ├── schemas/
│   │   ├── friend_schema.py
│   │   └── combination_schema.py
│   ├── services/
│   │   ├── friend_service.py    # Friend logic + combo generation triggers
│   │   └── combination_service.py  # Combo generation, filtering, toggling
│   └── static/
│       └── index.html           # Single-page web UI
├── Dockerfile
├── docker-compose.yml           # App + Cloudflare Tunnel
├── requirements.txt
├── .env.example
└── README.md
```

## Local Development

### Prerequisites

- Python 3.12+ (via mamba, conda, or system Python)

### Setup

```bash
# Create environment
mamba create -n friendigami python=3.12 -y

# Install dependencies
mamba run -n friendigami pip install -r requirements.txt

# Run the app
mamba run -n friendigami uvicorn app.main:app --reload
```

The app starts at [http://localhost:8000](http://localhost:8000). The database is auto-created on first startup.

### Docker (Local)

To run locally with Docker without Cloudflare Tunnel:

```bash
# Build and start just the app
docker build -t friendigami .
mkdir -p data
docker run -p 8000:8000 -v ./data:/app/data -e DATABASE_URL=sqlite:///data/friendigami.db friendigami
```

Or use Docker Compose (starts both the app and Cloudflare Tunnel):

```bash
cp .env.example .env
# Edit .env and set CLOUDFLARE_TUNNEL_TOKEN (or omit the cloudflared service)
mkdir -p data
docker compose up -d
```

The app is available at [http://localhost:8000](http://localhost:8000).

### Optional: Seed the database

```bash
mamba run -n friendigami python -m app.init_db
```

## API Reference

### Friends

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/friends` | List all friends |
| `GET` | `/friends/{symbol}` | Get a friend by ID |
| `POST` | `/friends` | Create a friend |
| `PUT` | `/friends/{symbol}` | Update a friend |
| `DELETE` | `/friends/{symbol}` | Delete a friend (and related combinations) |

**Request body** (POST/PUT):
```json
{
  "symbol": "TH",
  "first_name": "Tom",
  "last_name": "H"
}
```

### Combinations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/combinations` | List all combinations |
| `GET` | `/combinations/{id}` | Get a combination by ID |
| `PATCH` | `/combinations/{id}/toggle` | Toggle occurred status |
| `POST` | `/combinations/regenerate` | Regenerate all combinations (resets occurred) |

**Query parameters** for `GET /combinations`:
- `size` (int) — Filter by group size
- `occurred` (bool) — Filter by occurred status

**Combination ID format:** Friend symbols sorted alphabetically and joined with `-` (e.g. `MW-RZ-TH`)

### SMS Webhook

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sms/webhook` | Twilio incoming message webhook |

Expects a standard Twilio POST with a `Body` field containing comma-separated friend IDs:
```
TH, MW, RZ
```

Responds with TwiML:
- `"New combination logged! (MW-RZ-TH)"` — if the combination hadn't occurred yet
- `"Already happened! (MW-RZ-TH)"` — if it was already logged
- Error message if symbols are invalid

## Deployment (Raspberry Pi + Docker)

### 1. Get a Domain

Buy a domain and add it to [Cloudflare](https://dash.cloudflare.com) (point nameservers to Cloudflare).

### 2. Create a Cloudflare Tunnel

1. In the Cloudflare dashboard: **Zero Trust > Networks > Tunnels > Create a tunnel**
2. Name it `friendigami`
3. Copy the tunnel token
4. Add a public hostname route:
   - Subdomain: `friendigami` (or whatever you prefer)
   - Domain: your domain
   - Service: `http://friendigami:8000`

### 3. Deploy

```bash
# On the Raspberry Pi
git clone <your-repo-url>
cd friendigami

# Configure
cp .env.example .env
# Edit .env and set CLOUDFLARE_TUNNEL_TOKEN

# Create persistent data directory
mkdir -p data

# Start
docker compose up -d
```

The app is now live at `https://friendigami.yourdomain.com`.

### 4. Configure Twilio

1. Create a [Twilio](https://www.twilio.com) account and buy a phone number
2. In the Twilio console, configure the phone number's messaging webhook:
   - URL: `https://friendigami.yourdomain.com/sms/webhook`
   - Method: `POST`

Now anyone can text that number with friend IDs to log hangouts.

## Scaling Notes

The number of combinations grows fast with more friends:

| Friends | Total Combinations |
|---------|-------------------|
| 4 | 11 |
| 6 | 57 |
| 8 | 247 |
| 10 | 1,013 |
| 12 | 4,083 |

This is the sum of C(n, k) for k = 2 to n. SQLite handles this fine for typical friend group sizes.
