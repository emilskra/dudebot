package audio

import (
	"audio_service/common"
	"os"
	"path"
	"testing"
)

func TestConcatFiles(t *testing.T) {

	var files []string
	dir, _ := os.Getwd()

	fixturesDir := path.Join(dir, "fixtures")

	files = append(files, path.Join(fixturesDir, "seg1.ogg"))
	files = append(files, path.Join(fixturesDir, "seg2.ogg"))

	exportedFile, err := ConcatFiles(files, "chat_id.ogg")

	_ = os.Remove(*exportedFile)
	_ = os.Remove(common.ExportFilesDirectory())

	if err != nil {
		t.Errorf("Error: %v", err)
	}
}
