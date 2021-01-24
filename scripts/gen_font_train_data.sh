#!/bin/bash

python3 scripts/gen_font_dataset.py \
--root_dir dataset/font_train \
--font_dir dataset/ch_fonts_train \
--font_file dataset/font_file_train.json \
--char_file dataset/char_file.json \
--img_size 128