// Vehicle Service Digital Twin
// Routes grounded in: postman/specs/Vehicle Service Spec/index.yaml
//                     postman/collections/Vehicle Service Collection/

const http = require('http');

// ── helpers ──────────────────────────────────────────────────────────────────
function readBody(req) {
  return new Promise((resolve) => {
    let raw = '';
    req.on('data', (c) => (raw += c));
    req.on('end', () => {
      try { resolve(JSON.parse(raw)); } catch { resolve({}); }
    });
  });
}

function json(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(payload),
  });
  res.end(payload);
}

// ── seed data (mirrors collection examples) ──────────────────────────────────
const SEED = [
  { id: 1, nickName: 'The Lisa Marie', vin: '4M2DV11W4RDJ53329',
    make: 'Mercury', model: 'Villager', year: '1994', miles: 159864 },
  { id: 2, nickName: 'Dolly', vin: 'JN8AZ2KR1AT169594',
    make: 'Nissan', model: 'Cube', year: '2010', miles: 59000 },
];

const REQUIRED_FIELDS = ['nickName', 'vin', 'make', 'model', 'year', 'miles'];

// ── server ───────────────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const { method, url } = req;

  // @endpoint GET /vehicles
  if (method === 'GET' && url === '/vehicles') {
    const vehicles = await pm.state.get('vs:vehicles') ?? SEED;
    return json(res, 200, vehicles);
  }

  // @endpoint POST /vehicles
  if (method === 'POST' && url === '/vehicles') {
    const body = await readBody(req);

    // 400 — missing required field
    for (const field of REQUIRED_FIELDS) {
      if (body[field] === undefined || body[field] === null || body[field] === '') {
        return json(res, 400, { message: `Request body missing required attribute: ${field}` });
      }
    }

    const vehicles = await pm.state.get('vs:vehicles') ?? [...SEED];

    // 409 — duplicate VIN
    const dup = vehicles.find((v) => v.vin === body.vin);
    if (dup) {
      return json(res, 409, {
        message: `Vehicle with VIN ${body.vin} already exists. Existing vehicle ID: ${dup.id}`,
      });
    }

    const ids = vehicles.map((v) => v.id);
    const newId = ids.length ? Math.max(...ids) + 1 : 1;
    const vehicle = {
      id: newId,
      nickName: body.nickName,
      vin: body.vin,
      make: body.make,
      model: body.model,
      year: String(body.year),
      miles: body.miles,
    };
    vehicles.push(vehicle);
    await pm.state.set('vs:vehicles', vehicles);
    return json(res, 201, vehicle);
  }

  // ── /vehicles/:id routes ───────────────────────────────────────────────────
  const idMatch = url.match(/^\/vehicles\/(\d+)$/);
  if (idMatch) {
    const id = parseInt(idMatch[1], 10);
    const vehicles = await pm.state.get('vs:vehicles') ?? [...SEED];
    const idx = vehicles.findIndex((v) => v.id === id);

    // @endpoint GET /vehicles/:id
    if (method === 'GET') {
      if (idx === -1) return json(res, 404, { message: `Vehicle with id: ${id} not found.` });
      return json(res, 200, vehicles[idx]);
    }

    // @endpoint PATCH /vehicles/:id
    if (method === 'PATCH') {
      const body = await readBody(req);
      if (!body || typeof body !== 'object' || Array.isArray(body) || Object.keys(body).length === 0) {
        return json(res, 400, { message: 'Bad request body.' });
      }
      if (idx === -1) return json(res, 404, { message: `Vehicle with id: ${id} not found.` });

      // VIN uniqueness check on update
      if (body.vin && body.vin !== vehicles[idx].vin) {
        const dup = vehicles.find((v) => v.vin === body.vin);
        if (dup) {
          return json(res, 409, {
            message: `Vehicle with VIN ${body.vin} already exists. Existing vehicle ID: ${dup.id}`,
          });
        }
      }

      const updated = { ...vehicles[idx], ...body, id };
      vehicles[idx] = updated;
      await pm.state.set('vs:vehicles', vehicles);
      return json(res, 200, updated);
    }

    // @endpoint DELETE /vehicles/:id
    if (method === 'DELETE') {
      if (idx === -1) return json(res, 404, { message: `Vehicle with id: ${id} not found.` });
      vehicles.splice(idx, 1);
      await pm.state.set('vs:vehicles', vehicles);
      res.writeHead(204);
      return res.end();
    }
  }

  // ── 404 fallback ───────────────────────────────────────────────────────────
  return json(res, 404, { message: 'Not found.' });
});

server.listen(process.env.PORT || 4500);
