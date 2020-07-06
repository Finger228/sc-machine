from common import ScModule, ScAgent, ScEventParams
from sc import *

from wikiparser.WikiDataTranslator import WikiDataTranslator
import json


class TranslatorAgent(ScAgent):

    kHello = "hello"
    kWorld = "world"

    def RunImpl(self, evt: ScEventParams) -> ScResult:  
        wikiT = WikiDataTranslator()
        wikiT.getEntities(['Berlin', 'Belarus'])
        entities = json.loads(wikiT.getJson())
        
        parsed_entities_list = []
        parsed_entities_node = self.module.ctx.HelperResolveSystemIdtf("parsed_entities", ScType.NodeConstClass)
        itFAA = self.module.ctx.Iterator3(parsed_entities_node, ScType.EdgeAccessConstPosPerm, ScType.NodeConst)
        while itFAA.Next():
            parsed_entities_list.append(self.module.ctx.HelperGetSystemIdtf(itFAA.Get(2)))
            
        for entity in entities["entities"]:
            if entity not in parsed_entities_list:
                print(entity)
                entity_node = self.module.ctx.HelperResolveSystemIdtf(entity, ScType.NodeConst)
                self.module.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, parsed_entities_node, entity_node)

                descr = entities["entities"][entity]["description"]["en"]
                print(descr)
                descr_link = self.module.ctx.CreateLink()
                self.module.ctx.SetLinkContent(descr_link, descr)
                descr_edge = self.module.ctx.CreateEdge(ScType.EdgeDCommonConst, entity_node, descr_link)

                nrel_descr = self.module.ctx.HelperResolveSystemIdtf("nrel_parsed_entity_description", ScType.NodeConstNoRole)
                self.module.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, nrel_descr, descr_edge)

        return ScResult.Ok
