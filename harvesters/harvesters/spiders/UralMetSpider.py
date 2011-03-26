# -*- coding: utf-8 -*-
__author__ = 'ignatov'

import MySQLdb
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

def remove_duplicate_spaces(str):
    return " ".join(str.split())

def prettify(str):
    return str.replace(u"ШВЕЛЛЕР", u"Швеллер").replace(u"г/к", u"горячекатаный")

class UralMetSpider(BaseSpider):
    name = "td-uralmet.ru"
    human_name = u"Торговый Дом «УралМет»"
    allowed_domains = ["td-uralmet.ru"]
    start_urls = [
        "http://td-uralmet.ru/arma1",
        "http://td-uralmet.ru/arma3",
        "http://td-uralmet.ru/shveller",
        "http://td-uralmet.ru/#2",
        "http://td-uralmet.ru/balka",
        "http://td-uralmet.ru/truba",
        "http://td-uralmet.ru/kvadrat",
        "http://td-uralmet.ru/ugolok",
        "http://td-uralmet.ru/shestigrannik",
        "http://td-uralmet.ru/list",
        "http://td-uralmet.ru/polosa",
    ]
    supplier_id = None

    def __init__(self):
        BaseSpider(self).__init__(self.name)
        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="",
                               db="purchase",
                               charset="utf8",
                               use_unicode=True)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO nomenclature_supplier (name, site, type_id) VALUES ('%s', '%s', %d)" %
                (self.human_name, "http://" + self.name, 2)
                )
            self.supplier_id = conn.insert_id()
        except MySQLdb.IntegrityError:
            cursor.execute(
                "SELECT id FROM nomenclature_supplier WHERE name = '%s'" % self.human_name
                )
            self.supplier_id = cursor.fetchone()[0]
        cursor.close()
        conn.commit()
        conn.close()

    def parse(self, response):
        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="",
                               db="purchase",
                               charset="utf8",
                               use_unicode=True)
        cursor = conn.cursor()

        hxs = HtmlXPathSelector(response)
        table = hxs.select("//table[@class='table1']/tbody/tr[position() != 1]")
        for product in table:
            name = product.select('td[1]/text()').extract()
            price = product.select('td[last()]/text()').extract()
            if name:
                try:
                    cursor.execute(
                        "INSERT INTO nomenclature_product (name, price) VALUES ('%s', '%s')" %
                        (prettify(remove_duplicate_spaces(name[0])), price[0])
                        )
                    product_id = conn.insert_id()
                    try:
                        cursor.execute(
                            "INSERT INTO nomenclature_product_suppliers (product_id, supplier_id) VALUES (%d, %d)" %
                            (product_id, self.supplier_id)
                            )
                    except MySQLdb.IntegrityErrot:
                        pass
                except MySQLdb.IntegrityError:
                    cursor.execute(
                        "SELECT id FROM nomenclature_product WHERE name = '%s'" %
                        prettify(remove_duplicate_spaces(name[0]))
                        )
                    product_id = cursor.fetchone()[0]
                    try:
                        cursor.execute(
                            "INSERT INTO nomenclature_product_suppliers (product_id, supplier_id) VALUES (%d, %d)" %
                            (product_id, self.supplier_id)
                            )
                    except MySQLdb.IntegrityError:
                        pass
        cursor.close()
        conn.commit()
        conn.close()