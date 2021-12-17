package audio

import (
	"audio_service/common"
	"github.com/iFaceless/godub"
	"github.com/iFaceless/godub/converter"
	"log"
	"path"
)

func ConcatFiles(files []string, finishFileName string) string {

	var segments []*godub.AudioSegment
	for _, file := range files {

		newSegment, _ := godub.NewLoader().Load(file)
		segments = append(segments, newSegment)

	}

	segment, _ := godub.NewEmptyAudioSegment()
	segment, errAppend := segment.Append(segments...)
	if errAppend != nil {
		log.Fatal(errAppend)
	}

	return export(segment, finishFileName)
}

func export(segment *godub.AudioSegment, finishFileName string) string {
	newPth := path.Join(common.ExportFilesDirectory(), finishFileName)
	errExport := godub.
		NewExporter(newPth).
		WithDstFormat("ogg").
		WithBitRate(converter.MP3BitRatePerfect).
		Export(segment)

	if errExport != nil {
		log.Fatal(errExport)
	}

	return newPth
}
