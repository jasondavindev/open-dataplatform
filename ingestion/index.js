const dotenv = require('dotenv');
const express = require('express');
const { StreamingModule } = require('./lib/kafka_wrapper/wrapper');
const { ContentGenerator } = require('./lib/generator/index');

dotenv.config();

(async () => {
  const { PORT, SCHEMA_REGISTRY_URL, KAFKA_BROKER, HAS_KAFKA } = process.env;

  const contentGenerator = ContentGenerator.factory();

  const app = express();

  app.use(express.json());
  app.get('/status', (_, res) => res.json({ status: 'ok' }));
  app.get('/records', contentGenerator.generateRecords);
  app.get('/record', contentGenerator.generateRecord);

  if (HAS_KAFKA) {
    const streamingModule = await StreamingModule.factory({
      SCHEMA_REGISTRY_URL,
      KAFKA_BROKER,
    });

    app.post('/event/:topic', streamingModule.sendMessage);
  }

  app.listen(PORT, () => console.log('Server listening on port', PORT));
})();
