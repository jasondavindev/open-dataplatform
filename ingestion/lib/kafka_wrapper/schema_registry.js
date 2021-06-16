const { v4: uuidV4 } = require('uuid');
const { SchemaRegistry } = require('@kafkajs/confluent-schema-registry');
const avroRegistry = require('avro-schema-registry');

const createRegistry = (schemaRegistryHost) => {
  const confluentRegistry = new SchemaRegistry({ host: schemaRegistryHost });
  const avroSchemaRegistry = avroRegistry(schemaRegistryHost);

  const encodeMessage = async (topic, payload) => {
    const valueSchema = await avroSchemaRegistry.getSchemaByTopicName(
      `${topic}-value`
    );

    const keySchema = await avroSchemaRegistry.getSchemaByTopicName(
      `${topic}-key`
    );

    const key = uuidV4();

    const encodedPayload = await confluentRegistry.encode(
      valueSchema.id,
      payload
    );

    const encodedKey = await confluentRegistry.encode(keySchema.id, key);

    return {
      key: encodedKey,
      value: encodedPayload,
    };
  };

  return {
    registry: confluentRegistry,
    avroRegistry: avroSchemaRegistry,
    encodeMessage,
  };
};

module.exports = { createRegistry };
