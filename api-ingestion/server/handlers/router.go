package handlers

import (
	"net/http"

	"github.com/gorilla/mux"
)

func NewRoter() http.Handler {
	r := mux.NewRouter().PathPrefix("/api").Subrouter()

	registerHomeHandler(r)

	return r
}
