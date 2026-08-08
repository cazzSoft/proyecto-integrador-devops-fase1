import Fastify from 'fastify';
import cors from '@fastify/cors';
import { userRoutes } from './routes/userRoutes';

export function buildApp(logger = true) {
  const app = Fastify({ logger });

  app.register(cors, {
    origin: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
  });

  app.get('/', async () => ({
    status: 'OK',
    message: 'Servidor Backend Fastify activo',
  }));

  app.register(userRoutes);
  return app;
}
