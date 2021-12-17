package storage

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"

	"audio_service/common"
)

const token string = ""

type FilePathAnswer struct {
	file_path string
}

func DownloadFiles(files *[]string) []string {

	var downloadedFiles []string

	for _, file := range *files {
		filepath := common.DataDirectory() + file
		err := DownloadFile(filepath, file)
		if err != nil {
			log.Fatal(err)
		}

		downloadedFiles = append(downloadedFiles, filepath)
	}

	return downloadedFiles
}

func DownloadFile(filepath string, file string) error {
	filePathURL := "https://api.telegram.org/bot" + token + "/getFile?file_id=" + file

	// Get the file path
	respFilePath, err := http.Get(filePathURL)
	if err != nil {
		return err
	}
	defer respFilePath.Body.Close()

	var filePathResponse FilePathAnswer
	json.NewDecoder(respFilePath.Body).Decode(&filePathResponse)
	downLoadURL := "https://api.telegram.org/bot" + token + "/" + filePathResponse.file_path

	// Get the file
	respFile, err := http.Get(downLoadURL)
	if err != nil {
		return err
	}
	defer respFile.Body.Close()

	// Create the file
	out, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer out.Close()

	// Write the body to file
	_, err = io.Copy(out, respFile.Body)
	return err
}
