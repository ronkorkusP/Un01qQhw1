# Vehicle Service API — Flask Application

A lightweight Python/Flask server that implements the **Vehicle Service API**.  
It stores vehicles in memory (no database required) and protects every route with an API key.

---

## Requirements

- Python 3.14+
- pip

---

## Installation

```bash
cd app
pip install -r requirements.txt
```

---

## Running the server

### Option A — run directly

```bash
python app.py
```

### Option B — via the Flask CLI

```bash
export FLASK_APP=app.py
flask run --port 5000
```

The server listens on **`http://localhost:5000`** by default.

---

## Environment variables

| Variable  | Default         | Description                                      |
|-----------|-----------------|--------------------------------------------------|
| `API_KEY` | `postman-rocks` | The secret key clients must send in `X-API-Key`. |
| `PORT`    | `5000`          | TCP port the server binds to.                    |

### Setting the API key

```bash
# macOS / Linux
export API_KEY="my-secret-key"
python app.py

# Windows (PowerShell)
$env:API_KEY = "my-secret-key"
python app.py
```

---

## Pointing Postman at the local server

1. Open the **Local – Agent Mode** environment (or any environment you use).
2. Set the `baseUrl` variable to:

   ```
   http://localhost:5000
   ```

3. Make sure the `X-API-Key` header (or an environment variable that resolves to it) matches the `API_KEY` value the server was started with.

---

## API endpoints

All requests require the header:

```
X-API-Key: postman-rocks
```

### Create a vehicle — `POST /vehicles`

```bash
curl -s -X POST http://localhost:5000/vehicles \
  -H "Content-Type: application/json" \
  -H "X-API-Key: postman-rocks" \
  -d '{
    "nickName": "My Truck",
    "vin":      "1HGBH41JXMN109186",
    "make":     "Ford",
    "model":    "F-150",
    "year":     "2022",
    "miles":    15000
  }'
```

### Get all vehicles — `GET /vehicles`

```bash
curl -s http://localhost:5000/vehicles \
  -H "X-API-Key: postman-rocks"
```

### Retrieve a vehicle — `GET /vehicles/:id`

```bash
curl -s http://localhost:5000/vehicles/1 \
  -H "X-API-Key: postman-rocks"
```

### Update a vehicle — `PATCH /vehicles/:id`

```bash
curl -s -X PATCH http://localhost:5000/vehicles/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: postman-rocks" \
  -d '{"miles": 16500}'
```

### Delete a vehicle — `DELETE /vehicles/:id`

```bash
curl -s -X DELETE http://localhost:5000/vehicles/1 \
  -H "X-API-Key: postman-rocks"
# Returns HTTP 204 No Content on success
```

---

## HTTP status codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 200  | Successful retrieval / update                |
| 201  | Vehicle successfully created                 |
| 204  | Vehicle successfully deleted                 |
| 400  | Missing or invalid request attribute         |
| 401  | Unauthorized — missing or invalid API key    |
| 404  | Vehicle ID does not exist                    |
| 409  | A vehicle with the same VIN already exists   |
| 500  | Unexpected server-side failure               |

---

## Data model

```json
{
  "id":       1,
  "nickName": "My Truck",
  "vin":      "1HGBH41JXMN109186",
  "make":     "Ford",
  "model":    "F-150",
  "year":     "2022",
  "miles":    15000
}
```

> **Note:** `id` is assigned automatically by the server and cannot be set or changed by the client.
