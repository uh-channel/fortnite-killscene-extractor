# Fortnite Kill-Scene Extractor
Python script for kill scene detection and extraction from playing video of Fortnite.

This script scan the video, and after detecting the kill point, cut out the each kill scene to the output directory without re-encoding.

## Requirement

* Python > 3.2 
* tesseract 4.0.0
* pytesseract 
* ffmpeg

## Confirmed Environment

* Ubuntu 18.04 on WSL
* Video captured from Nintendo Switch

## Installation

1. Download `ext.py` to your local.

## Usage

```sh
$ python3 ext.py interval pre_margin post_margin input_file output_dir
```

### Arguments

|             |                                             |
| ----------- | ------------------------------------------- |
| interval    | detection interval seconds                  |
| pre_margin  | margin seconds to cut before detected point |
| post_margin | margin seconds to cut after detected point  |
| input_file  | input file path                             |
| output_dir  | directory path to output                    |

## Constraints

* fixed 30 fps
* fixed mp4 format