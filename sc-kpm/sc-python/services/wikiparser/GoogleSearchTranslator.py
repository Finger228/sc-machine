from wikiparser.BaseTranslator import BaseTranslator
import urllib
import requests
from bs4 import BeautifulSoup


class GoogleSearchTranslator(BaseTranslator):
    # desktop user-agent
    _USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    _MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    # google search URL
    _URL = 'https://google.com/search?q={}'

    def getEntity(self, entity, lang='en'):
        if lang == 'en':
            query = 'definition of a word "{}"'.format(entity)
        if lang == 'de':
            query = 'Definition eines Wortes "{}"'.format(entity)

        query = query.replace(' ', '+')

        headers = {"user-agent": self._USER_AGENT}
        resp = requests.get(self._URL.format(query), headers=headers)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = []
            for vmod in soup.find_all('div', class_='vmod', jsname='r5Nvmf'):
                part_of_speech = vmod.find(
                    'div', class_='lW8rQd').find('span').text
                definition = vmod.find(
                    'div', class_='QIclbb XpoqFe').find('span').text
                results.append({
                    'part_of_speech': part_of_speech,
                    'definition': definition
                })

            self._info['entities'][entity.lower().replace(' ', '_')] = {
                'identifier': entity.lower().replace(' ', '_'),
                'label': {lang: entity},
                'description': {lang: results[0]['definition']}
            }

    def getEntities(self, entities):
        for entity in entities:
            self.getEntity(entity)


if __name__ == '__main__':
    googleT = GoogleSearchTranslator()
    googleT.getEntity('jazz', lang='de')
    f = open("output_g.json", "wt")
    f.write(googleT.getJson())
    f.close()
