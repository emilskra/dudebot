package apiV1

import (
	"audio_service/audio"
	"audio_service/storage"
	"github.com/gin-gonic/gin"
	"net/http"
)

type files struct {
	files          []string
	finishFileName string
}

func Concat(c *gin.Context) {

	var json files
	if err := c.ShouldBindJSON(&json); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	downloadedFiles, errDownload := storage.DownloadFiles(&json.files)
	if errDownload != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": errDownload.Error()})
		return
	}

	exportedFile, errExport := audio.ConcatFiles(downloadedFiles, json.finishFileName)
	if errExport != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": errExport.Error()})
		return
	}

	c.File(*exportedFile)
}
