package common

import (
	"errors"
	"log"
	"os"
	"path"
)

func DataDirectory() string {
	dir, _ := os.Getwd()

	dataDir := path.Join(dir, "data")

	_, err := os.Stat(dataDir)
	if errors.Is(err, os.ErrNotExist) {
		errDir := os.Mkdir(dataDir, 0750)
		if errDir != nil {
			log.Println(errDir)
		}
	}

	return dataDir
}

func ExportFilesDirectory() string {
	exportDir := path.Join(DataDirectory(), "export")
	_, err := os.Stat(exportDir)
	if errors.Is(err, os.ErrNotExist) {
		errDir := os.Mkdir(exportDir, 0750)
		if errDir != nil {
			log.Println(errDir)
		}
	}

	return exportDir
}
