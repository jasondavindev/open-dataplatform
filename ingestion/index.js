const dotenv = require('dotenv');
const express = require('express');
const { createRegistry } = require('./lib/schema_registry');
const { createProducer } = require('./lib/producer');

dotenv.config();

(async () => {
  const { PORT, SCHEMA_REGISTRY_URL, KAFKA_BROKER } = process.env;
  const producer = await createProducer(KAFKA_BROKER);
  const registry = createRegistry(SCHEMA_REGISTRY_URL);

  const app = express();
  app.use(express.json());

  app.get('/status', (_, res) => res.json({ status: 'ok' }));

  app.post('/event/:topic', async (req, res) => {
    const body = req.body;
    const topic = req.params.topic;
    const response = { topic, body };
    const payload = await registry.encodeMessage(topic, body);

    console.log(`Sending message payload=${JSON.stringify(body)}`);

    await producer.sendMessage(topic, payload);

    return res.status(201).json(response);
  });

  app.listen(PORT, () => console.log('Server listening on port', PORT));
})();
