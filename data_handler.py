from pyspark.sql import SparkSession

from constants import DEFAULT_SEPARATOR, HEADER, INFER_SCHEMA


class PySparkHandler:
    def __init__(self, product_file_path: str, category_file_path: str, product_category_file_path) -> None:
        self.__spark: SparkSession = SparkSession.builder.master('local').appName('py_spark_app').getOrCreate()
        self.__product_data = self.__spark.read.csv(
            product_file_path,
            sep=DEFAULT_SEPARATOR,
            header=HEADER,
            inferSchema=INFER_SCHEMA
        )
        self.__category_data = self.__spark.read.csv(
            category_file_path,
            sep=DEFAULT_SEPARATOR,
            header=HEADER,
            inferSchema=INFER_SCHEMA
        )
        self.__product_category_data = self.__spark.read.csv(
            product_category_file_path,
            sep=DEFAULT_SEPARATOR,
            header=HEADER,
            inferSchema=INFER_SCHEMA
        )

    def __get_products_with_categories(self):
        self.__category_data.select('id', 'name')
        self.__product_data.select('id', 'name')

        return self.__product_data.join(
            other=self.__product_category_data,
            on=(self.__product_data['id'] == self.__product_category_data['product_id']),
            how='inner'
        ).join(
            other=self.__category_data,
            on=(self.__category_data['id'] == self.__product_category_data['category_id']),
            how='inner'
        ).select(self.__product_data['name'], self.__category_data['name'])

    def print_products_with_categories(self):
        print('Products with existing categories:')
        self.__get_products_with_categories().show(30)

    def print_products_without_category(self):
        products_without_category = (self.__product_data
                                     .select('name')
                                     .exceptAll((self.__get_products_with_categories()
                                                 .select(self.__product_data['name']))))
        print('Products without existing categories:')
        products_without_category.show(10)
