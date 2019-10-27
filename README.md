# video-subtitle-translator
This is a python application that is used to translate movie subtitles .srt from any language into Polish.
Regular expressions have been used so that Google Translator does not replace the file format.
You can change the destination language in the target = "pl".

## You must generate your own token from Google Cloud Platform for use.

## Use
python3 app.py

The application will ask for the source file .srt
will create an empty file with the extension .pl.srt
and start translating
