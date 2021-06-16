const { createRegistry } = require('./schema_registry');
const { createProducer } = require('./producer');

class KafkaWrapper {
  static async factory({ SCHEMA_REGISTRY_URL, KAFKA_BROKER }) {
    const producer = await createProducer(KAFKA_BROKER);
    const registry = createRegistry(SCHEMA_REGISTRY_URL);

    const instance = new KafkaWrapper();
    instance._registry = registry;
    instance._producer = producer;

    return instance;
  }

  sendMessage = async ({ body, params: { topic } }, res) => {
    const response = { topic, body };

    try {
      await this._sendMessage({ topic, body });
      return res.status(201).json(response);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  };

  _sendMessage = async ({ topic, body }) => {
    const payload = await this._registry.encodeMessage(topic, body);
    console.log(`Sending message payload=${JSON.stringify(body)}`);

    await this._producer.sendMessage(topic, payload);
  };
}

module.exports.StreamingModule = KafkaWrapper;
