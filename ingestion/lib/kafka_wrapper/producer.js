const { Kafka } = require('kafkajs');

const createProducer = async (kafkaBroker) => {
  const kafka = new Kafka({
    clientId: 'api-ingestion',
    brokers: [kafkaBroker],
  });

  const producer = kafka.producer();
  await producer.connect();

  const sendMessage = async (topic, payload) => {
    await producer.send({
      topic,
      messages: [payload],
    });
  };

  return {
    producer,
    sendMessage,
  };
};

module.exports = { createProducer };
