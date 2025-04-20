#!/bin/bash


DIRECTORY="../out"

if [ ! -d "$DIRECTORY" ]; then
  echo "Ошибка: директория '$DIRECTORY' не существует."
  exit 1
fi

find "$DIRECTORY" -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 rm -rf {}

echo "Поддиректории в директории '$DIRECTORY' удалены."

exit 0