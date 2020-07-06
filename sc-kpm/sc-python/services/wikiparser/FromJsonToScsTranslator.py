import json
import requests
import re

f = open('input.json', 'rt')
info = json.loads(f.read())
f.close()


for ent_info in info['entities'].values():
    if ent_info['identifier'].find('/') != -1:
        continue
    scs = open('sc_out\\{}.scs'.format(ent_info['identifier']), 'wt', encoding='utf-8')
    scs.write(ent_info['identifier']+'\n')
    scs.write('=> nrel_main_idtf:\n')
    for lang, label in ent_info['label'].items():
        scs.write('\t[{}] (* <- lang_{};; *);\n'.format(label, lang))
    scs.write('<- rrel_key_sc_element: ...\n(*\n\t<- sc_definition;;\n\t<= nrel_sc_text_translation:')
    for lang, description in ent_info['description'].items():
        scs.write('\n\t\t... (* -> rrel_example: [{}] (* <-lang_{};; *);; *);'.format(description, lang))
    scs.write(';\n*);\n')

    try:
        image_url = ent_info['image_url']
        image_format = re.findall(r'\.\w*$', image_url)[0]
        image_format = image_format[1:]
        image = requests.get(image_url)
        image_file = open('sc_out\\images\\{}_image.{}'.format(ent_info['identifier'], image_format), 'wb')
        image_file.write(image.content)
        image_file.close()
        scs.write('<- rrel_key_sc_element: ...\n(*\n\t<-sc_illustration;;\n\t<=nrel_sc_text_translation: ...\n')
        scs.write('\t(*\n\t\t-> rrel_example: "file://images/{}_image.{}"'.format(ent_info['identifier'], image_format))
        scs.write(' (* => nrel_format: format_{};; *);;\n\t*);;\n*);\n'.format(image_format))
    except KeyError:
        pass

    scs.write('<-sc_node_not_relation;;')
    scs.close()

for rlt in info['relations'].values():
    scs = open('sc_out\\{}.scs'.format(rlt['identifier']), 'wt', encoding='utf-8')
    scs.write(rlt['identifier']+'\n')
    scs.write('=> nrel_main_idtf:\n')
    for lang, label in rlt['label'].items():
        scs.write('\t[{}] (* <- lang_{};; *);\n'.format(label, lang))
    scs.write('<- rrel_key_sc_element: ...\n(*\n\t<- sc_definition;;\n\t<= nrel_sc_text_translation:')
    for lang, description in rlt['description'].items():
        scs.write('\n\t\t... (* -> rrel_example: [{}] (* <-lang_{};; *);; *);'.format(description, lang))
    scs.write(';\n*);\n')
    scs.write('<-sc_node_norole_relation;;')
    scs.close()

f = open('sc_out\\triplets.scs', 'w')
for triplet in info['triplets']:
    scs = open('sc_out\\triplets.scs', 'at', encoding='utf-8')
    scs.write('{} => {}: {};;\n'.format(triplet[0], triplet[1], triplet[2]))
    scs.close()
