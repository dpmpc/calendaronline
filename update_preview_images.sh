#!/bin/bash

URL="http://localhost:8000/preview?format="
DST_FOLDER="web/creator/static/images/"
FORMATS="P PW PF L LF 1 V"

for FORMAT in $FORMATS
do
	echo "Creating preview image for format $FORMAT..."
	curl "$URL$FORMAT" --output tmp.pdf
	pdftoppm -png -scale-to 598 tmp.pdf | convert png:- -bordercolor black -border 1  -background "rgb(255 128 0 / 100%)" -gravity center -extent 600x600 "${DST_FOLDER}preview-$FORMAT.png"

done
