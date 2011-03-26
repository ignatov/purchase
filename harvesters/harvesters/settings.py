# Scrapy settings for harvesters project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'harvesters'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['harvesters.spiders']
NEWSPIDER_MODULE = 'harvesters.spiders'
DEFAULT_ITEM_CLASS = 'harvesters.items.HarvestersItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

