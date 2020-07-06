import os
import time
from common import ScModule, ScKeynodes, ScPythonEventType
from keynodes import Keynodes
from TranslatorAgent import TranslatorAgent

from sc import *


class TranslatorModule(ScModule):

    def __init__(self):
        ScModule.__init__(
            self,
            ctx=__ctx__,
            cpp_bridge=__cpp_bridge__,
            keynodes=[
            ],
            )

    def OnInitialize(self, params):
        print('Initialize Translator module')        
        kHello = self.keynodes[TranslatorAgent.kHello]
        kWorld = self.keynodes[TranslatorAgent.kWorld]
        
        agent = TranslatorAgent(self)
        agent.Register(kHello, ScPythonEventType.AddOutputEdge)        

        tempEdgeAddr = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, kHello, kWorld)
        self.ctx.DeleteElement(tempEdgeAddr)

    def OnShutdown(self):        
        print('Shutting down Translator module')  
        nrel_descr = self.ctx.HelperResolveSystemIdtf("nrel_parsed_entity_description", ScType.NodeConstNoRole)
        parsed_entities_node = self.ctx.HelperResolveSystemIdtf("parsed_entities", ScType.NodeConstClass) 
        itFAF = self.ctx.Iterator3(parsed_entities_node, ScType.EdgeAccessConstPosPerm, ScType.NodeConst)

        while itFAF.Next():
            entity_node = itFAF.Get(2)
            itFAF_2 = self.ctx.Iterator5(   entity_node,
                                            ScType.EdgeDCommonConst, 
                                            ScType.LinkConst,
                                            ScType.EdgeAccessConstPosPerm,
                                            nrel_descr)
            while itFAF_2.Next():
                print("entity {}, descr: {}".format(
                                    self.ctx.HelperGetSystemIdtf(entity_node),
                                    self.ctx.GetLinkContent(itFAF_2.Get(2)).AsString()))



service = TranslatorModule()
service.Run()
