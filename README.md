# devil API

FastAPI-based REST API for managing resources on a devil server. It acts as a thin wrapper around the underlying devil control interface exposed via a local UNIX domain socket, providing authenticated endpoints for DNS, FTP, repositories, ports, SSL certificates, virtual hosts, websites, and databases (MySQL, PostgreSQL, MongoDB).

## Description

This project exposes a secure HTTP interface to common devil server operations. The application:

- Runs a FastAPI app with multiple routers (dns, ftp, info, mail, mongo, mysql, pgsql, port, repo, ssl, vhost, www).
- Authenticates every request using an API key provided via X-API-Key header or Authorization: Bearer token.
- Communicates with the local devil service over a UNIX domain socket at /var/run/devil2.sock.
- Maps JSON command lists to the devil service and returns parsed JSON responses.
- Handles socket-level and protocol-level errors consistently, converting them into API-friendly HTTP responses.

Environment-driven behavior:
- Authentication requires DEVIL_API_KEY set at process start (loaded from the environment or a .env file).
- Optional rate-limiting on authentication failures (per-IP) using DEVIL_AUTH_FAIL_THRESHOLD and DEVIL_AUTH_BLOCK_SECONDS.
- Logging level can be controlled via LOG_LEVEL.

## Features

- Auth
  - API key authentication via X-API-Key or Authorization: Bearer token
  - Per-IP rate limiting for repeated failed auth attempts (429 Too Many Requests)
- Health check endpoint: GET /health
- DNS management: add zones and records (with validation for CAA/MX/SRV), list zones/records, delete
- FTP accounts: create, delete, change password, change/recalc quota, list
- Repository management: create/delete repositories, change visibility, add/delete accounts, change account passwords, list
- Port reservations: reserve (specific or random), release, list (TCP/UDP)
- SSL certificates: add/delete/get for WWW and mail (support for Let’s Encrypt on WWW)
- Virtual hosts: list available IPs, filter by type (private/public/all)
- Website (WWW) management: add/remove domains, options, Matomo stats access and accounts, etc.
- Databases
  - MySQL: users, databases, privileges management (rich schema with validation)
  - PostgreSQL: create/delete DB, change password, enable extensions, list
  - MongoDB: create/delete DB, change password, list
- Robust socket client with:
  - Timeouts
  - JSON protocol enforcement
  - Rich error mapping:
    - 503 on connection issues
    - 502 on protocol errors
    - 400 on devil-reported errors

## Installation

Prerequisites:
- Python 3.11+
- A devil service available via UNIX domain socket at /var/run/devil2.sock (running on the same host)
- A valid API key to configure in your environment

1. Clone the repository
    ```sh
    git clone https://github.com/devil-imps/devil-api.git
    cd devil-api
    ```

2. Installation

    a) Using [UV](https://docs.astral.sh/uv/) (recommended)
    > Unfortunately, currently there is no UV installed on devil servers, you can use [Lilith: Devil's Package Manager](https://github.com/devil-imps/helpers/tree/inferno/lilith) to install UV.
    ```sh
    uv sync
    ```

    b) Using PIP editable install
    ```sh
    # Create and activate a virtual environment
    virtualenv .venv
    source .venv/bin/activate

    # Install dependencies
    pip install -e .
    ```

Set environment variables (in shell or in a .env file):
```sh
export DEVIL_API_KEY="your-secret"
# Optional:
export LOG_LEVEL="INFO"
export DEVIL_AUTH_FAIL_THRESHOLD="5"
export DEVIL_AUTH_BLOCK_SECONDS="300"
```

## Usage

Run the API with uvicorn:
```sh
# Change port number to your reserved port, use `devil port add tcp random devil-api` to reserve random one
# If installed via UV you can run `uv run uvicorn app.main:app --port 8000` or activate venv using `source .venv/bin/activate` to run command below
uvicorn app.main:app --port 8000
```

Health check (no auth required):
```sh
curl http://localhost:8000/health
# {"status":"ok"}
```

Authenticated request using X-API-Key:
```sh
curl -H "X-API-Key: your-secret" http://localhost:8000/info/limits
```

Authenticated request using Bearer token:
```sh
curl -H "Authorization: Bearer your-secret" http://localhost:8000/info/limits
```

Example: Reserve a random TCP port
```sh
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret" \
  -d '{"type":"tcp","random":true,"description":"devil-api-test"}' \
  http://localhost:8000/port/add
```

Notes:
- Every non-/health endpoint is protected and requires a valid API key.
- Authentication failures are tracked per client IP address; repeated failures can lead to 429 responses for a configurable block duration.

## Configuration

- DEVIL_API_KEY (required): API key required to access all protected endpoints
- LOG_LEVEL (optional): e.g., INFO, DEBUG
- DEVIL_AUTH_FAIL_THRESHOLD (optional, default 5): number of failed attempts before blocking
- DEVIL_AUTH_BLOCK_SECONDS (optional, default 300): block duration in seconds

Create a local .env file to load automatically:
```
DEVIL_API_KEY=your-secret
LOG_LEVEL=INFO
DEVIL_AUTH_FAIL_THRESHOLD=5
DEVIL_AUTH_BLOCK_SECONDS=300
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE License. See the [LICENSE](LICENSE) file for details.
