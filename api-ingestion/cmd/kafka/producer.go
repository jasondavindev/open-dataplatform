package kafka

import (
	"fmt"
	"log"
	"time"

	"github.com/dangkaka/go-kafka-avro"
)

func CreateProducer(brokers []string, schemaRegServers []string) *kafka.AvroProducer {
	producer, err := kafka.NewAvroProducer(brokers, schemaRegServers)

	if err != nil {
		log.Fatalf("Could not create avro producer: %s\n", err)
	}

	return producer
}

func SendMessage(producer *kafka.AvroProducer, schema string, topic string, value string) {
	key := time.Now().String()
	err := producer.Add(topic, schema, []byte(key), []byte(value))

	if err != nil {
		fmt.Printf("Could not send the message: %s\n", err)
	}
}
