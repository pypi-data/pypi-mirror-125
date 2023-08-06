# ImprovadoTest  
Python back-end test task

## Installation

```
pip install vkinfo
```
## Usage  
---

### **1. Generate access_token**  
**Why do you need one:**  
Indicates you as the one who is trying to get information, and wether or not you are allowed to.  

For example: If user has private account and only his friends can acccess their info, or their music tastes are very singular, so only you can see it. VK just needs to know whos asking, otherwise its kinda creepy.

**How to get one:**  
command below will open VK auth page and ask to grant permessions for this app.

```
vkinfo token
```

Then, you'll be redirected to blank page. Copy access_token from url of this page.  
![https://oauth.vk.com/blank.html#access_token={your_token}&expires_in=BAN&user_id=BAN5](imgs/auth.png)

Congrats! This is your access token for the next 24 hours. 

### 2. Run script

```
vkinfo run {access_token} {search_user_id}
```


## Parameters
---

### Global

* `log-path`: Path for the log file.

### Exporting

* `export-path`: Path for the log file.
* `export-format`: Format for the export (choices: `csv` | `json` | `tsv`).


## Example
---

```
vkinfo run asfajhskaaalx 1478202 --format tsv --path ~/projects/lalareport --log-path ~/projects/lalalogs.log
```

Command above will: get friends list of user `1478202` using token `asfajhskaaalx` and save it as `tsv` file in `~/projects/lalareport.tsv` and log file saved in `~/projects/lalalogs.log`
## Endpoints
---

### VK API endpoints used

* /method/friends.get
* /method/stats.TrackVisitor
* /method/users.get
* /authorize


## Дополнение
---

### *Модульность и структура*  
- Проект имеет структуру файлов и распределение по функционалу.  
  - config файл с константами по умолчанию
  - exceptions для кастомных исключений и их обработки
  - get_token может запускаться как main
  - vk_api создает собственный класс-сессию для текущего пользователя с основными параметрами, новый функционал легко добавить как метод класса.
  - папка util содержит вспомогательные функции, такие как обработка данных и export класс
- Редактирование представленного и добавление нового функционала.  
  - с помощью VkApiSess.method_execute() можно использовать любые(get) методы api vk + произвольные параметры, а не только friends.get
  - полученные данные имеют представление pandas.Dataframe и обрабатываются в util.parsers в зависимости от поствленной задачи
  - класс exporter получает на вход pandas.Dataframe и делает с ним всё что можно и нельзя

### *Чистые логи*  
- Чтобы не пугать пользователя кучей страшных символов, логи делятся.  
  - Те, что видны в консоли(info): отображают ход выполнения программы.  
  - Дебаг, логи внешних модулей и полные описания ошибок записываются в файл.
- То же самое с ошибками, адекватные люди не будут копаться в traceback'ах, поэтому все исключения вызывают SystemExit с коротким сообщением, а неадекватные могут посмотреть в лог файле. 

### *Простая установка через pip*
- Проект загружен на PyPi для максимальной простоты установки

### *Оптимальный анализ данных*
- Для анализа данных выбрал pandas потому что он удобный, универсальный, гибкий и вообще клёвый.
- Также выбор pandas обусловлен капом на друзей в 10к, для таких размеров это показалось оптимальным вариантом(подробнее в комментах vk_api.py). Но это вряд ли оптимальная стратегия для более массивных данных.

### *Замечания*
- Особо важные комменты на русском ибо понимание > понты

- Писал и тестировал на wsl2 Ubuntu20.04

- Во время получения токена(а точнее открытия браузера) есть косяк, 
но это никак не мешает работе скрипта и косяк только wsl

- Не приспособлено и даже не запускалось на Windows

- python3.8.10