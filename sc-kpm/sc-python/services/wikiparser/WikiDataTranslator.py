from wikiparser.BaseTranslator import BaseTranslator
import wptools


class WikiDataTranslator(BaseTranslator):
    def getEntity(self, entity, return_claims=False):
        ent_type = 'entities'
        if entity.startswith('Q'):
            page = wptools.page(wikibase=entity, skip=['labels'], silent=True)
        elif entity.startswith('P'):
            page = wptools.page(wikibase=entity, skip=[
                                'labels', 'imageinfo'], silent=True)
            ent_type = 'relations'
        else:
            page = wptools.page(entity, skip=['labels'], silent=True)
        page.get_wikidata()
        de_page = wptools.page(wikibase=page.data['wikibase'], lang='de', skip=[
                               'labels', 'imageinfo'], silent=True)
        de_page.get_wikidata()
        self._info[ent_type][page.data['title']] = {
            'identifier': page.data['title'],
            'label': {'en': page.data['label'], 'de': de_page.data['label']},
            'description': {'en': page.data['description'], 'de': de_page.data['description']}
        }
        if page.images():
            self._info[ent_type][page.data['title']]['image_url'] = page.images()[
                0]['url']
        if return_claims:
            return page.data['claims']

    def getEntities(self, entities, return_claims=False):
        claims = {}
        for entity in entities:
            claims.update(self.getEntity(entity, return_claims=True))
        if return_claims:
            return claims

    def getEntityWithContext(self, entity):
        ent_type = 'entities'
        if entity.startswith('Q'):
            page = wptools.page(wikibase=entity, skip=['labels'], silent=True)
        elif entity.startswith('P'):
            page = wptools.page(wikibase=entity, skip=[
                                'labels', 'imageinfo'], silent=True)
            ent_type = 'relations'
        else:
            page = wptools.page(entity, skip=['labels'], silent=True)
        page.get_wikidata()
        de_page = wptools.page(wikibase=page.data['wikibase'], lang='de', skip=[
                               'labels', 'imageinfo'], silent=True)
        de_page.get_wikidata()
        self._info[ent_type][page.data['title']] = {
            'identifier': page.data['title'],
            'label': {'en': page.data['label'], 'de': de_page.data['label']},
            'description': {'en': page.data['description'], 'de': de_page.data['description']}
        }
        if page.images():
            self._info[ent_type][page.data['title']]['image_url'] = page.images()[
                0]['url']

        context = page.data['claims']
        for rlt, ents in context.items():
            rlt_page = wptools.page(
                wikibase=rlt, skip=['labels', 'imageinfo'], silent=True)
            rlt_page.get_wikidata()
            rlt_de_page = wptools.page(wikibase=rlt, lang='de', skip=[
                                       'labels', 'imageinfo'], silent=True)
            rlt_de_page.get_wikidata()
            rlt_id = rlt_page.data['title']

            self._info['relations'][rlt_id] = {
                'identifier': rlt_id,
                'label': {'en': rlt_page.data['label'], 'de': rlt_de_page.data['label']},
                'description': {'en': rlt_page.data['description'], 'de': rlt_de_page.data['description']}
            }

            for ent in ents:
                if type(ent) is str:
                    if ent.startswith('Q'):
                        ent_page = wptools.page(
                            wikibase=ent, skip=['labels'], silent=True)
                        ent_page.get_wikidata()
                        ent_de_page = wptools.page(wikibase=ent, lang='de', skip=[
                                                   'labels', 'imageinfo'], silent=True)
                        ent_de_page.get_wikidata()
                        try:
                            ent_id = ent_page.data['title']
                        except KeyError:
                            continue

                        self._info['entities'][ent_id] = {
                            'identifier': ent_id,
                            'label': {'en': ent_page.data['label'], 'de': ent_de_page.data['label']},
                            'description': {'en': ent_page.data['description'], 'de': ent_de_page.data['description']}
                        }
                        if ent_page.images():
                            self._info['entities'][ent_id]['image_url'] = ent_page.images()[
                                0]['url']

                        self._info['triplets'].append(
                            [page.data['title'], rlt_id, ent_id])


if __name__ == '__main__':
    wikiT = WikiDataTranslator()
    wikiT.getEntity('Berlin')
    # wikiT.getEntities(['Minsk', 'Belarus'])
    # wikiT.getEntityWithContext('Berlin')
    f = open("output_w.json", "wt")
    f.write(wikiT.getJson())
    f.close()

    # TODO: из json в scs
    # TODO: google search скрипт обращения к словарю (DONE)
