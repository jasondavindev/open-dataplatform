package common

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type SchemaRegistrySubjectResponse struct {
	Schema string `json:"schema"`
}

type SchemaRegistryModule struct {
	schemas map[string]string
}

func (t *SchemaRegistryModule) GetSchema(topicName string) string {
	if schema, ok := t.schemas[topicName]; ok {
		return schema
	}

	fmt.Printf("[REQUEST] Finding the schema for subject %s\n", topicName)

	url := fmt.Sprintf("http://localhost:8081/subjects/%s-value/versions/latest", topicName)
	response, err := http.Get(url)

	if err != nil {
		log.Fatal(err)
	}

	var body SchemaRegistrySubjectResponse

	err = json.NewDecoder(response.Body).Decode(&body)

	if err != nil {
		log.Fatal(err)
	}

	t.schemas[topicName] = body.Schema

	return t.schemas[topicName]
}

func NewSchemaRegistryModule() SchemaRegistryModule {
	return SchemaRegistryModule{schemas: map[string]string{}}
}
