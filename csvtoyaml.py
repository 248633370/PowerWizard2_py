#!/usr/bin/env python

'''
 The csv file must have a valid header as 1st line.
Based on header fill the dictionary and subdictionary for yaml format file.
'''
import csv
import yaml
import collections
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
	for line in cfgread:
		for i in range(len(line)):
			if n == 1:
				header.append(line[i])
		subdict = dict(zip(header,line))
		params[line[0]] = subdict
		n=n+1
	print str(params['ParamID'])

# Enable needed params
enable_params = [ 'TOTAL_KW_PCT', 
                'REAL_POWER', 
                'PH_A_RMS_CURRENT', \
                'PH_B_RMS_CURRENT', \
                'PH_C_RMS_CURRENT', \
                'B_PH_A_L2L_VOLTS', \
                'B_PH_B_L2L_VOLTS', \
                'B_PH_C_L2L_VOLTS', \
                'ENG_COOL_TMP', \
                'AUTO_STRT_STOP', \
                'ADEM_OIL_PRESS', \
                'ADEM_COOL_TEMP', \
                'DL_ENG_OIL_TEMP', \
                'DL_INST_FUEL_CON', \
                'ENG_OP_MODE', \
                'RTC', \
                'LOSS_OF_UTILITY',
                 \
                'BAT_VOLTS', \
                'GEN_FREQ_OK', \
                'GEN_VOLTS_OK']

for en_param in enable_params:
    params[en_param]['Enable'] = '1'
# Sorting yaml by key
#ordered_params = collections.OrderedDict(sorted(params.items()))
# open file for yaml store
yamlfile = codecs.open(outfile, 'w+', 'utf-8')
yamlfile.write(yaml.dump(collections.OrderedDict(sorted(params.items())), encoding='utf-8', allow_unicode=True))

