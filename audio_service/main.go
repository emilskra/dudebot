package main

import (
	"audio_service/api/v1"
	"github.com/julienschmidt/httprouter"
	"github.com/kelseyhightower/envconfig"
	"net/http"
)

type Config struct {
	Token string `envconfig:"TOKEN"`
}

func main() {

	var cfg Config
	errConfig := envconfig.Process("", cfg)
	if errConfig != nil {
		return
	}
	router := httprouter.New()
	router.GET("/concat", api_v1.Concat)

	errServer := http.ListenAndServe(":8080", router)
	if errServer != nil {
		return
	}
}
