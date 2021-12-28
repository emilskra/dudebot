package storage

import (
	"audio_service/common"
	"errors"
	"os"
	"path"
	"testing"
)

func TestDownloadFile(t *testing.T) {

	filename := "seg.ogg"
	fileId := "AwACAgIAAxkDAAIHwWGZcgS16OrbJRJ-Swtt60VRluvLAAIMFgACJEbISKI0qwOZbMnvIgQ"
	filepath := path.Join(common.DataDirectory(), filename)
	err := DownloadFile(filepath, fileId)

	if err != nil {
		t.Errorf("Error: %v", err)
	}

	if _, err := os.Stat(filepath); errors.Is(err, os.ErrNotExist) {
		t.Errorf("Error: %v", err)
	}

	err = os.Remove(filepath)
	if err != nil {
		t.Errorf("Error: %v", err)
	}

}

func TestDownloadFiles(t *testing.T) {
	fileId := "AwACAgIAAxkDAAIHwmGZcgTEJtDVIFWNpRh7UfCmBaxGAAINFgACJEbISJ53LllDNJT7IgQ"

	files := []string{
		fileId,
	}
	downloadedFiles, err := DownloadFiles(&files)

	if err != nil {
		t.Errorf("Error: %v", err)
	}

	if len(downloadedFiles) != len(files) {
		t.Errorf("Not all files were saved")
	}

	for _, file := range downloadedFiles {
		_, err := os.Stat(file)

		if errors.Is(err, os.ErrNotExist) {
			t.Errorf("File do not exist: %v", err)
		}

		_ = os.Remove(file)

	}

}
