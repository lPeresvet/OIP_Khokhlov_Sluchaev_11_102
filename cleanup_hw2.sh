#!/bin/bash


DIRECTORY="./out"

# Проверяем, существует ли директория.
if [ ! -d "$DIRECTORY" ]; then
  echo "Ошибка: директория '$DIRECTORY' не существует."
  exit 1
fi

# Находим все поддиректории в указанной директории и удаляем их.
# find "$DIRECTORY" -mindepth 1 -maxdepth 1 -type d -print0  :  Ищет поддиректории
# xargs -0 rm -rf {}                       :  Удаляет найденные поддиректории

find "$DIRECTORY" -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 rm -rf {}

echo "Поддиректории в директории '$DIRECTORY' удалены."

exit 0