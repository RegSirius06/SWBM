# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:27:19 2023

@author: Stefan
"""

import shutil
import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler

from SWBM.settings import BASE_DIR

source_file = os.path.join(BASE_DIR, "db.sqlite3")
destination_directory = os.path.join(BASE_DIR, "backup")

def copy_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

def rename_file(destination_path):
    now = datetime.datetime.now()
    current_date = now.strftime("%d.%m.%Y")
    current_time = now.strftime("%H.%M")
    new_filename = f"{current_date}_{current_time}.sqlite3"
    new_path = os.path.join(destination_path, new_filename)
    return new_path

def main():
    try:
        copy_file(source_file, destination_directory)
        new_path = rename_file(destination_directory)
        shutil.move(os.path.join(destination_directory, "db.sqlite3"), new_path)
    except FileExistsError:
        return
    except FileNotFoundError:
        return

    print("Copied  succesfully!")

    """
    while True:
        now = datetime.datetime.now()
        current_hour = now.hour
        
        # Проверяем время
        if current_hour == 13 or current_hour == 22:
            # Копируем файл
            copied_file = copy_file(source_file, destination_directory)
            
            # Переименовываем скопированный файл
            new_path = rename_file(destination_directory)
            shutil.move(destination_directory + "\\db.sqlite3", new_path)
        else:
            time.sleep(3600)
            continue
        
        # Ожидаем до следующего дня
        nine_hours = (datetime.timedelta(hours=9)).total_seconds()
        fifteen_hours = (datetime.timedelta(hours=15)).total_seconds()
        time.sleep(nine_hours if current_hour== 13 else fifteen_hours)
    """

if __name__ == "__main__":
    if not os.path.isdir(destination_directory):
        os.makedirs(destination_directory)
    scheduler = BackgroundScheduler()
    scheduler.add_job(main, 'interval', hours=12)
    time.sleep(3600 * ((24 - datetime.datetime.now().hour) % 12))
    main()
    scheduler.start()
    while True: pass
