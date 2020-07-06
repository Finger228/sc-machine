/*
* This source file is part of an OSTIS project. For the latest info, see http://ostis.net
* Distributed under the MIT License
* (See accompanying file COPYING.MIT or copy at http://opensource.org/licenses/MIT)
*/

#include "wikparModule.hpp"

SC_IMPLEMENT_MODULE(WikiParserModule)

sc_result WikiParserModule::InitializeImpl()
{
  m_wikpasService.reset(new WikiParserPythonService("wikiparser/main.py"));
  m_wikpasService->Run();
  return SC_RESULT_OK;
}

sc_result WikiParserModule::ShutdownImpl()
{
  m_wikpasService->Stop();
  m_wikpasService.reset();
  return SC_RESULT_OK;
}
