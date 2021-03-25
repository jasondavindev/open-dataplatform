package httputil

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)

type Request struct {
	Response http.ResponseWriter
	Request  *http.Request
	Params   KnownParameters
}

type KnownParameters struct {
	ID       string
	NumberID string
	Vertical string
}

type ErrorResponse struct {
	Error string `json:"error"`
}

func New(Response http.ResponseWriter, r *http.Request) *Request {
	vars := mux.Vars(r)
	params := KnownParameters{
		ID:       vars["id"],
		NumberID: vars["number_id"],
		Vertical: vars["vertical"],
	}
	return &Request{Response, r, params}
}

func (r *Request) Decode(value interface{}) error {
	return json.NewDecoder(r.Request.Body).Decode(value)
}

func (r *Request) WriteSuccess(body interface{}, status int) {
	if body == nil {
		r.Response.WriteHeader(status)
		return
	}

	r.Response.Header().Set("Content-Type", "application/json")
	r.Response.WriteHeader(status)
	json.NewEncoder(r.Response).Encode(body)
}

func (r *Request) WriteError(err error, status int) {
	r.Response.Header().Set("Content-Type", "application/json")
	r.Response.WriteHeader(status)
	json.NewEncoder(r.Response).Encode(ErrorResponse{
		Error: err.Error(),
	})
}
