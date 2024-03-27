from data_handler import PySparkHandler

from constants import PRODUCTS_FILE_PATH, CATEGORIES_FILE_PATH, PRODUCT_CATEGORY_FILE_PATH


if __name__ == '__main__':
    try:
        py_spark_handler = PySparkHandler(PRODUCTS_FILE_PATH, CATEGORIES_FILE_PATH, PRODUCT_CATEGORY_FILE_PATH)
        py_spark_handler.print_products_with_categories()
        py_spark_handler.print_products_without_category()
    except Exception:
        print('Check your PySpark module! May be it should have additional package')
