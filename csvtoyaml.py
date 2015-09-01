#!/usr/bin/env python

'''
 The csv file must have a valid header as 1st line.
Based on header fill the dictionary and subdictionary for yaml format file.
'''
import csv
import yaml
import codecs
import sys
# Make utf8 default encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# constants and init vars
infile = 'Params_wDataTypes.csv'
outfile = 'newParams_wDataTypes.yaml'
params = {}
header = []
subdict = {}
n=1

#start process of csv
with open(infile, 'r') as csvfile:
	cfgread = csv.reader(csvfile, delimiter=';', quotechar='"')
#	cfgread = unicode_csv_reader(csvfile, delimiter=';', quotechar='"')
	for line in cfgread:
		for i in range(len(line)):
			if n == 1:
				header.append(line[i])
		subdict = dict(zip(header,line))
		params[line[0]] = subdict
		n=n+1
	print str(params['ParamID'])
	print str(params['ADEM_COOL_TEMP']['DisplayText'])
# open file for yaml store
yamlfile = codecs.open(outfile, 'w+', 'utf-8')
yamlfile.write(yaml.dump(params, encoding='utf-8', allow_unicode=True))
#yamlfile = open(outfile, 'w+')
#yamlfile.write(yaml.dump(params))


'''if __name__ == "__main__":
    main()
'''
