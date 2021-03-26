package common

import (
	"os"
	"strings"
)

type Config struct {
	Port                    string
	Brokers                 []string
	SchemaRegistryAddresses []string
}

func CreateConfig() *Config {
	port := os.Getenv("PORT")
	brokers := strings.Split(os.Getenv("BROKERS"), ",")
	schemaRegistry := strings.Split(os.Getenv("SCHEMA_REGISTRY_ADDRESSES"), ",")

	config := &Config{
		Port:                    port,
		Brokers:                 brokers,
		SchemaRegistryAddresses: schemaRegistry,
	}

	return config
}
