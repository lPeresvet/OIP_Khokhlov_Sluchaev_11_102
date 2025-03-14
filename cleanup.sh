#!/bin/bash

DIR="./out"

find "$DIR" -maxdepth 1 ! -name ".gitkeep" -type f -delete

echo "Все файлы, кроме .gitkeep, удалены из директории $DIR"
