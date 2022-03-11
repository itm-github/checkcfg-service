# Служба Windows. Создание, установка

- основа: https://github.com/HaroldMills/Python-Windows-Service-Example/blob/master/example_service.py
- использовать python 3.8.5
- windows service (делать на чистой виртуалке установив python для всех пользователей, пакеты устанавливаем без вирт окружения)
- ставить все пакеты в ком строке от имени админа




- создание исполняемого файла

```powershell

pip install -r requirements.txt
pip install pywin32

```





```powershell
pyinstaller --hidden-import win32timezone --hidden-import schedule -F .\win_service.py --name checkCfgService.exe

```
