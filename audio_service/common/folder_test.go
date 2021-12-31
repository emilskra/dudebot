package common

import (
	"os"
	"testing"
)

func TestDataDirectory(t *testing.T) {

	dataPath := DataDirectory()
	err := os.Remove(dataPath)

	if err != nil {
		t.Errorf("Error: %v", err)
	}

}

func TestExportFilesDirectory(t *testing.T) {

	exportPath := ExportFilesDirectory()
	err := os.Remove(exportPath)

	if err != nil {
		t.Errorf("Error: %v", err)
	}

}
