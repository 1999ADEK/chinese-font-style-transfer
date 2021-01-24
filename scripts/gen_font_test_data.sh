#!/bin/bash

python3 scripts/gen_font_dataset.py \
--root_dir dataset/font_test \
--font_dir dataset/ch_fonts_test \
--font_file dataset/font_file_test.json \
--char_file dataset/char_file.json \
--img_size 128 \
--test \
--num_imgs 10