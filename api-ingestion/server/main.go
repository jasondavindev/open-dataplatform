package main

import (
	"io/ioutil"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/jasondavindev/open-dataplatform/cmd/common"
	mkafka "github.com/jasondavindev/open-dataplatform/cmd/kafka"
	"github.com/joho/godotenv"
)

var kafkaServers = []string{"localhost:9092"}
var schemaRegistryServers = []string{"http://localhost:8081"}

func main() {
	godotenv.Load()

	router := gin.Default()

	router.POST("/event/:event", sendEventHandler())

	PORT := os.Getenv("PORT")

	router.Run(":" + PORT)
}

func sendEventHandler() func(c *gin.Context) {
	schemaRegistryModule := common.NewSchemaRegistryModule()
	producer := mkafka.CreateProducer(kafkaServers, schemaRegistryServers)

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
