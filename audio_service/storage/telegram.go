package storage

import (
	"audio_service/common"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

const token string = "1502829486:AAHr60kaoCuoh5880Y9chqsx4Vr6ZrZWiQs"

type TelegramFile struct {
	FilePath string `json:"file_path"`
}

type TelegramFileInfo struct {
	Result TelegramFile `json:"result"`
}

func DownloadFiles(files *[]string) ([]string, error) {

	if len(*files) == 0 {
		return nil, errors.New("files not provided")
	}

	var downloadedFiles []string

	for _, file := range *files {
		filepath := common.DataDirectory() + file + ".ogg"
		err := DownloadFile(filepath, file)
		if err != nil {
			log.Fatal(err) // TODO: make normal log
			return nil, err
		}

		downloadedFiles = append(downloadedFiles, filepath)
	}

	return downloadedFiles, nil
}

func DownloadFile(filepath string, file string) error {

	fileTelegram, err := getFileInfo(file)
	if err != nil {
		return err
	}

	respFile, err := getFile(fileTelegram)
	if err != nil {
		return err
	}

	defer respFile.Body.Close()

	// Create the file
	out, err := os.Create(filepath)
	if err != nil {
		log.Fatal(err)
		return err
	}
	defer out.Close()

	// Write the body to file
	_, err = io.Copy(out, respFile.Body)
	return err
}

func getFileInfo(file string) (*TelegramFile, error) {

	filePathURL := "https://api.telegram.org/bot" + token + "/getFile?file_id=" + file

	r, err := http.Get(filePathURL)
	if err != nil {
		return nil, err
	}
	if r.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("error status: %v", r.StatusCode)
	}

	defer r.Body.Close()

	var filePathResponse TelegramFileInfo
	json.NewDecoder(r.Body).Decode(&filePathResponse)

	buf, err := ioutil.ReadAll(r.Body)
	bufs := string(buf)
	fmt.Printf("Request body: %v", bufs)

	return &filePathResponse.Result, nil
}

func getFile(fileTelegram *TelegramFile) (*http.Response, error) {

	downLoadURL := "https://api.telegram.org/file/bot" + token + "/" + fileTelegram.FilePath

	// Get the file
	r, err := http.Get(downLoadURL)
	if err != nil {
		return nil, err
	}

	if r.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("error status: %v", r.StatusCode)
	}

	return r, err

}
