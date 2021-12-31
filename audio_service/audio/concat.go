package audio

import (
	"audio_service/common"
	"github.com/iFaceless/godub"
	"path"
)

func ConcatFiles(files []string, finishFileName string) (*string, error) {

	var segment *godub.AudioSegment

	for _, file := range files {

		newSegment, _ := godub.NewLoader().Load(file)
		if segment == nil {
			segment = newSegment
		} else {
			segment, _ = segment.Append(segment, newSegment)
		}
	}

	return export(segment, finishFileName)
}

func export(segment *godub.AudioSegment, finishFileName string) (*string, error) {
	newPth := path.Join(common.ExportFilesDirectory(), finishFileName)
	errExport := godub.
		NewExporter(newPth).
		WithDstFormat("ogg").
		Export(segment)

	if errExport != nil {
		return nil, errExport
	}

	return &newPth, nil
}
