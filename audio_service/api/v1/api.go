package api_v1

import (
	"audio_service/audio"
	"audio_service/storage"
	"github.com/julienschmidt/httprouter"
	"net/http"
)

func Concat(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {

	var files []string
	var finishFileName string

	downloadedFiles := storage.DownloadFiles(&files)
	audio.ConcatFiles(downloadedFiles, finishFileName)
}
