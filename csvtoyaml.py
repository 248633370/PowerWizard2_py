#!/usr/bin/env python

'''
 The csv file must have a valid header as 1st line.
Based on header fill the dictionary and subdictionary for yaml format file.
In ParamID key subdictionary stored width for print tables
CSV must be save with semicolon (;) and quotechar is double quotation marks (").
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
# vars for tab width
default_tab = '6'
tab_line = []
n=1

# start process of csv
with open(infile, 'r') as csvfile:
    cfgread = csv.reader(csvfile, delimiter=';', quotechar='"')
#    cfgread = csv.reader(csvfile, delimiter=';')
    for line in cfgread:
        if n == 1:
            for i in range(len(line)):
                header.append(line[i])
                if line[i] == 'ParamID':
                    tab_line.append('16')
                elif line[i] == 'DisplayText':
                    tab_line.append('40')
                elif line[i] == 'MaxVal':
                    tab_line.append('8')
                else:
                    tab_line.append(default_tab)
            subdict = dict(zip(header,tab_line))
        else:
            subdict = dict(zip(header,line))
        params[line[0]] = subdict
        n=n+1
#    print params
#    print str(params['ParamID'])

# Enable needed params
'''
                'B_PH_A_L2L_VOLTS', \
                'B_PH_B_L2L_VOLTS', \
                'B_PH_C_L2L_VOLTS', \
'''
enable_params = [ 'TOTAL_KW_PCT', 
                'REAL_POWER', 
                'PH_A_RMS_CURRENT', \
                'PH_B_RMS_CURRENT', \
                'PH_C_RMS_CURRENT', \
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
yamlfile.close()
