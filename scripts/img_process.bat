:: Resize everything.
cd ../data/revision_2

:: Resize everything.
magick mogrify -resize 50x50 *.png

:: Extent everything out to a single SQUARE size.
magick mogrify -background black -gravity center -extent 50x50 *.png

cd ../../scripts
