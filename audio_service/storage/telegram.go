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
	"path"
)

var TOKEN = os.Getenv("TOKEN")

type TelegramStorage struct {
}

type TelegramFile struct {
	FilePath string `json:"file_path"`
}

type TelegramFileInfo struct {
	Result TelegramFile `json:"result"`
}

func (t TelegramStorage) DownloadFiles(files *[]string) ([]string, error) {

	if len(*files) == 0 {
		return nil, errors.New("files not provided")
	}

	var downloadedFiles []string

	for _, file := range *files {
		filepath := path.Join(common.DataDirectory(), file+".ogg")
		err := t.DownloadFile(filepath, file)
		if err != nil {
			return nil, err
		}

		downloadedFiles = append(downloadedFiles, filepath)
	}

	return downloadedFiles, nil
}

func (t TelegramStorage) DownloadFile(filepath string, file string) error {

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

	filePathURL := "https://api.telegram.org/bot" + TOKEN + "/getFile?file_id=" + file

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

	downLoadURL := "https://api.telegram.org/file/bot" + TOKEN + "/" + fileTelegram.FilePath

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
