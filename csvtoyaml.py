#!/usr/bin/env python

import sys, csv, yaml, codecs
# Make utf8 default encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# constants and init vars
params = {}
header = []
subdict = {}
n=1
# utf_8_encoder(
#start process of csv
with open("Params_wDataTypes.csv", 'r') as csvfile:
	cfgread = csv.reader(csvfile, delimiter=';', quotechar='"')
#	cfgread = unicode_csv_reader(csvfile, delimiter=';', quotechar='"')
	for line in cfgread:
		for i in range(len(line)):
			if n == 1:
				header.append(line[i])
			if type(line[i]) == 'string':
				print i
				print 'string'
		subdict = dict(zip(header,line))
		params[line[0]] = subdict
		n=n+1
	print str(params['ParamID'])
	print str(params['ADEM_COOL_TEMP']['DisplayText'])
# open file for yaml store
yamlfile = codecs.open("newParamByRegister_wDataTypes.yaml", "r+", "utf-8")
yamlfile.write(yaml.dump(params, encoding='utf-8', allow_unicode=True))

'''if __name__ == "__main__":
    main()
'''
