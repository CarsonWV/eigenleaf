:: Grab pixel dimensions, source, and destination paths.
SET /A pixels = %1
SET source=%2
SET destination=%3

echo %destination%, %source%

:: Duplicate the original test set.
:: /y - Suppresses prompting to confirm that you want to overwrite an existing destination file.
:: /i - Creates directory if it doesn't exist.
:: /q - Suppresses the display of xcopy messages.
xcopy /y /i /q %source% %destination%

:: Jump to the copied directory.
cd %destination%

:: Shrink every image to fit in a X by X box.
magick mogrify -resize %pixels%x%pixels% *.png

:: Extent everything out to a single SQUARE size.
magick mogrify -background black -gravity center -extent %pixels%x%pixels% *.png
