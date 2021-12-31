package storage

import (
	"log"
	"os"
)

type Storage interface {
	DownloadFiles(files *[]string) ([]string, error)
	DownloadFile(filepath string, file string) error
}

func NewStorage() Storage {
	return TelegramStorage{}
}

func ClearFiles(files *[]string) {
	for _, file := range *files {
		err := os.Remove(file)
		if err == nil {
			log.Println(err)
		}
	}

}
