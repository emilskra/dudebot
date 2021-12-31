package main

import (
	apiV1 "audio_service/api/v1"
	"github.com/gofiber/fiber/v2"
	"log"
)

func main() {
	app := fiber.New()

	app.Get("/ping", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World 👋!")
	})

	app.Post("/concat", apiV1.Concat)

	err := app.Listen(":8080")
	if err != nil {
		log.Fatal(err)
	}

}
