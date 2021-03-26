package main

import (
	"io/ioutil"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jasondavindev/open-dataplatform/cmd/common"
	mkafka "github.com/jasondavindev/open-dataplatform/cmd/kafka"
	"github.com/joho/godotenv"
)

var kafkaServers = []string{"broker:29092"}
var schemaRegistryServers = []string{"http://schema-registry:8081"}

func main() {
	godotenv.Load()

	config := common.CreateConfig()

	router := gin.Default()

	router.POST("/event/:event", sendEventHandler(config))

	router.Run(":" + config.Port)
}

func sendEventHandler(cfg *common.Config) func(c *gin.Context) {
	schemaRegistryModule := common.NewSchemaRegistryModule(cfg)
	producer := mkafka.CreateProducer(cfg.Brokers, cfg.SchemaRegistryAddresses)

	return func(c *gin.Context) {
		body, _ := ioutil.ReadAll(c.Request.Body)
		event := c.Param("event")

		schema := schemaRegistryModule.GetSchema(event)

		mkafka.SendMessage(producer, schema, event, string(body))

		c.JSON(http.StatusOK, gin.H{
			"event": event,
		})
	}
}
