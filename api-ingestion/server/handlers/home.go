package handlers

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/jasondavindev/open-dataplatform/server/httputil"
)

func registerHomeHandler(r *mux.Router) {
	h := homeHandler{}
	r = r.NewRoute().PathPrefix("/v1").Subrouter()

	r.HandleFunc("/", h.Get).Methods("GET")
}

type homeHandler struct {
}

func (h *homeHandler) Get(w http.ResponseWriter, r *http.Request) {
	req := httputil.New(w, r)
	req.WriteSuccess(true, http.StatusOK)
}
