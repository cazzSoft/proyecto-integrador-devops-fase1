import type { FastifyInstance } from 'fastify';
import client from 'prom-client';

export const register = new client.Registry();

register.setDefaultLabels({
  application: 'gestion-usuarios-backend',
});

client.collectDefaultMetrics({
  register,
  prefix: 'app_',
});

const httpRequestsTotal = new client.Counter({
  name: 'app_http_requests_total',
  help: 'Total de solicitudes HTTP recibidas por el backend',
  labelNames: ['method', 'route', 'status_code'] as const,
  registers: [register],
});

const httpRequestDuration = new client.Histogram({
  name: 'app_http_request_duration_seconds',
  help: 'Duracion de solicitudes HTTP en segundos',
  labelNames: ['method', 'route', 'status_code'] as const,
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5],
  registers: [register],
});

const requestStart = new WeakMap<object, bigint>();

export function registerMetrics(app: FastifyInstance) {
  app.addHook('onRequest', async (request) => {
    requestStart.set(request, process.hrtime.bigint());
  });

  app.addHook('onResponse', async (request, reply) => {
    const start = requestStart.get(request);
    if (!start) return;

    const durationSeconds = Number(process.hrtime.bigint() - start) / 1_000_000_000;
    const route = request.routeOptions?.url || request.url;

    const labels = {
      method: request.method,
      route,
      status_code: String(reply.statusCode),
    };

    httpRequestsTotal.inc(labels);
    httpRequestDuration.observe(labels, durationSeconds);
  });

  app.get('/metrics', async (_request, reply) => {
    reply.header('Content-Type', register.contentType);
    return register.metrics();
  });
}