## **PySparkApp** - второе тестовое задания для компании MindBox на позицию стажёра Python / C# Backend разработчика

</br>

### **Используемые технологии:** Python (3.12), PySpark (3.5.1)

</br>

### **Как запустить проект:**

1. Склонировать репозиторий себе в локальную директорию
    ```
    git clone git@github.com:mrForza/PySparkApp.git
    ```
2. Перейти в локальную директорию и создать виртуальное окружение
    ```
    python -m venv .venv
    ```
3. Активаировать виртуальное окружение
    ```
    source .venv/Scripts/activate
    ```
4. Обновить пакетный менеджер pip
    ```
    python -m pip install --upgrade pip
    ```
5. Установить все необходимые зависимости из файла _requirements.txt_
    ```
    pip install -r requirements.txt
    ```
6. Перезагрузить IDE при необходимости

</br>

## **Структура проекта:**
```
├── README.md <--- Файл с описанием проекта
├── constants.py <--- Скрипт, в котором указаны необходимые константы и пути к csv файлам 
├── data <--- Директория с csv файлами, 
│   ├── categories.csv
│   ├── product_category.csv
│   └── products.csv
├── data_handler.py <--- Основной скрипт по обработке данных с помощью модуля PySpark
├── main.py <--- основной скрипт проекта
└── requirements.txt <--- Зависимости для проекта
```

</br>

## **Архитектура проекта:**
* Скрипт _main_ запускает необходимые методы класса _PySparkHandler_
* Класс _PySparkHandler_ в скрипте _data_handler_ служит некоторой обёрткой над функционалом модуля _pyspark_. В нём происходит работа с датафреймами, а также с выборками
* В директории _data_ находятся файлы формата csv, в которых описаны продукты, а также их категории. Класс _PySparkHandler_ берёт информацию для датафреймов из этих csv файлов
* Структура products.csv имеет следующий вид:

    id | name | quantity | price |
    --- | --- | --- | ---
    1 | Куриное филе | 20 | 350

* Структура categories.csv имеет следующий вид:

    id | name
    --- | ---
    1 | Молочка

* Для реализации связи _многие ко многим_ создан дополнительный файл product_category.csv, который имеет следующий вид:

    id | product_id | category_id
    --- | --- | ---
    1 | 2 | 15

</br>

## **Реализация логики получения продуктов с существующими категориями:**
* Для того, чтобы получить все имена товаров, у которых есть котегории, и соответсвтующие категории, мы должны применить два _INNER JOIN'а_. Первый соединаяет датафреймы product_data и product_category_data. Второй соединаяет датафрейма product_category_data и category_data.
* Если бы у нас были таблицы БД с такими же атрибутами, то мы бы ввели на языке SQL следующий запрос:

    ```
    SELECT product.name, category.name FROM product
    INNER JOIN product_category ON product.id = product_category.product_id
    INNER JOIN category ON category.id = product_category.category_id;
    ```

</br>

## **Реализация логики получения имени продуктов без категорий**
* После первой операции мы можем получить две выборки: Первая выборка содержит всевозможные продукты, а вторая содержит только те продукты, у которых есть категория. Чтобы найти имена продуктов без категорий, нужно применить оператор разности двух выборок
* На языке SQL мы бы написали следующий запрос:

    ```
    SELECT product.name FROM product EXCEPT
    SELECT product.name FROM product
    INNER JOIN product_category ON product.id = product_category.product_id
    INNER JOIN category ON category.id = product_category.category_id;
    ```
* Для нашего текущего датасета мы бы получили значения: **Мускатный орех, Семена лотоса и Кунжут**, так как у этих продуктов нет соответствующей категории в файле _categories.csv_
* Все действия, применённые с помощью библиотеки PySpark основаны на этих SQL запросах

</br>

Автор работы: _Громов Роман_

Дата: _27.03.2024_