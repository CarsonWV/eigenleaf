:: Grab pixel dimensions.
SET /A p = %1

:: Resize everything.
cd ../data/revision_2

:: Resize everything.
magick mogrify -resize %p%x%p% *.png

:: Extent everything out to a single SQUARE size.
magick mogrify -background black -gravity center -extent %p%x%p% *.png

cd ../../scripts
