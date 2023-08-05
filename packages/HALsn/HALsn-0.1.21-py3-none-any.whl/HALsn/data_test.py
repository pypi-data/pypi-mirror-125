from dataSupervisor import dataSupervisor
from SKU import CFP
from examples.raw_bdp import data

cfp = CFP()
sup = dataSupervisor(headers=False, s3_enable=False)

sup.set_product_map(cfp.queries)
sup.lst = data
sup.localfile = '~/GENERIC_HEADER_TEST.csv'

sup.interpreted_parse()
print(sup.df)
sup.export_csv()