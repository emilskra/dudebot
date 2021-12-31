package apiV1

import (
	"audio_service/audio"
	"audio_service/storage"
	"github.com/gofiber/fiber/v2"
	"net/http"
)

type concatFiles struct {
	Files          []string `json:"files"`
	FinishFileName string   `json:"finishFileName"`
}

func Concat(c *fiber.Ctx) error {

	var filesData concatFiles
	if err := c.BodyParser(&filesData); err != nil {
		return fiber.NewError(http.StatusBadRequest, err.Error())
	}

	// Download files
	fileStorage := storage.NewStorage()
	downloadedFiles, errDownload := fileStorage.DownloadFiles(&filesData.Files)
	if errDownload != nil {
		return fiber.NewError(http.StatusBadRequest, errDownload.Error())
	}

	// Concat downloaded files
	exportedFile, errExport := audio.ConcatFiles(downloadedFiles, filesData.FinishFileName)
	if errExport != nil {
		return fiber.NewError(http.StatusBadRequest, errExport.Error())
	}

	downloadedFiles = append(downloadedFiles, *exportedFile)
	defer storage.ClearFiles(&downloadedFiles)
	return c.SendFile(*exportedFile)
}
