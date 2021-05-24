const dotenv = require('dotenv');
const express = require('express');
const KafkaAvro = require('kafka-avro');

dotenv.config();

const createProducer = async (kafkaBroker, schemaRegistry) => {
  const kafkaAvro = new KafkaAvro({
    kafkaBroker,
    schemaRegistry,
  });

  await kafkaAvro.init();

  return kafkaAvro.getProducer();
};

(async () => {
  const { PORT, SCHEMA_REGISTRY_URL, KAFKA_BROKER } = process.env;

  const app = express();
  app.use(express.json());

  const producer = await createProducer(KAFKA_BROKER, SCHEMA_REGISTRY_URL);

  app.get('/status', (_, res) => res.json({ status: 'ok' }));

  app.post('/event/:topic', (req, res) => {
    const body = req.body;
    const topic = req.params.topic;
    const response = { topic, body };

    producer.produce(topic, -1, body);

    console.log(response);
    return res.status(201).json(response);
  });

  app.listen(PORT, () => console.log('Server listening on port', PORT));
})();
