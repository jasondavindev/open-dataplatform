package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/jasondavindev/open-dataplatform/server/handlers"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()
	r := handlers.NewRoter()

	port := os.Getenv("PORT")

	fmt.Printf("Starting the server on port %s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
