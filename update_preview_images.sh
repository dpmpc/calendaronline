#!/bin/bash

URL="http://localhost:8000/preview?format="
DST_FOLDER="web/creator/static/images/"
FORMATS="P PW PF L LF LM 1 V 26 26L 26S"

for FORMAT in $FORMATS
do
	echo "Creating preview image for format $FORMAT..."
	rm tmp-?.png
	curl "$URL$FORMAT" --output tmp.pdf
	pdftoppm -png -scale-to 598 tmp.pdf tmp
	magick tmp-?.png -bordercolor black -border 1 -append -resize 598x598 -background "rgb(255 255 255 / 0%)" -gravity center -extent 600x600 "${DST_FOLDER}preview-$FORMAT.png"
done
