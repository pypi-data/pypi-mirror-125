Changelog of threedi-raster-edits
===================================================


0.16 (2021-10-28)
-----------------

- Fixed release error


0.15 (2021-10-28)
-----------------

- More efficient loading of threedirastergroup


0.14 (2021-10-28)
-----------------

- ThreediAPI and ThreediResults are now optional.


0.13 (2021-10-19)
-----------------

- Fixed vector reprojections
- Added inflated rasterloops for rasters
- Added rasterloops for rastergroups
- Added inflated rasterloops for rastergroups
- Added bbox clipping for rasters


0.12 (2021-09-13)
-----------------

- Improved difference algorithm
- Remove geometry fixed at every call, now call once with veotor.fix()
- fid= -1 will result in a fid which is the count


0.11 (2021-09-06)
-----------------

- Token release


0.10 (2021-09-06)
-----------------

- Added sqlite-model support
- Added api support


0.9 (2021-05-06)
----------------

- Changed black format.


0.8 (2021-05-06)
----------------

- Added clips for rasters
- Added custom line string lengths
- Added vector interpolation
- Added (partly) fix threedi rasters


0.7 (2021-03-26)
----------------

- Fixed release process (same for 0.6/0.6).


0.4 (2021-03-26)
----------------

- Fixed release process.
- Fixed tests.
- Added logging.
- Better memory usage of rasters.
- Small changes in vector, geometries.

0.3 (2021-03-25)
----------------

- Automated pypi release.


0.2 (2021-03-12)
----------------

- Changed the syntax of raster class
- Changed the imports to the main script: E.g., from threedi_raster_edits import raster, rastergroup etc.
- Changed the readme.
- Rewritten the geometry structure.


0.1 (2021-03-11)
----------------

- Initial project structure created with cookiecutter and
  https://github.com/nens/cookiecutter-python-template
