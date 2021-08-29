import yaml
import json
import os
import argparse

parser = argparse.ArgumentParser(description='Generates ARM templates from a parser YAML file')
parser.add_argument('-p', '--path', required=True, metavar='C:\\path\\to\\folder\\file.json', type=str, dest='path',
                    help='Full path to the folder containing the YAML files')
args = parser.parse_args()
path = os.path.abspath(args.path)
arm_template = json.load(open('Template.json', 'r'))
print (f'Creating ARM template for parser {path}')

(folder, filename) = os.path.split(os.path.abspath(path))
fname = f'{filename[:-5]}.json'

with open(path) as file:
    parserYaml = yaml.load(file, Loader=yaml.FullLoader)
title = parserYaml["Parser"]["Title"]
alias = parserYaml["ParserName"]
query = parserYaml["ParserQuery"]
Product = parserYaml["Product"]["Name"]
Schema = parserYaml["Normalization"]["Schema"]

data_section=arm_template['resources'][0]['resources'][0]
data_section['name'] = alias
data_section['properties']['query'] = query
data_section['properties']['FunctionAlias'] = alias
data_section['properties']['displayName'] = title

with open(os.path.join(folder, f'{fname}'), 'w') as jf:
    json.dump(arm_template, jf, indent=2)