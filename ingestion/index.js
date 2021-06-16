const dotenv = require('dotenv');
const express = require('express');
const { StreamingModule } = require('./lib/kafka_wrapper/wrapper');
const { ContentGenerator } = require('./lib/generator/index');

dotenv.config();

(async () => {
  const { PORT, SCHEMA_REGISTRY_URL, KAFKA_BROKER } = process.env;

  const streamingModule = await StreamingModule.factory({
    SCHEMA_REGISTRY_URL,
    KAFKA_BROKER,
  });
  const contentGenerator = ContentGenerator.factory();

  const app = express();

  app.use(express.json());
  app.get('/status', (_, res) => res.json({ status: 'ok' }));
  app.post('/event/:topic', streamingModule.sendMessage);
  app.get('/records', contentGenerator.generateRecords);
  app.get('/record', contentGenerator.generateRecord);
  app.listen(PORT, () => console.log('Server listening on port', PORT));
})();
