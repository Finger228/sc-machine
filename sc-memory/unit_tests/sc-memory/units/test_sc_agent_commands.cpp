/*
 * This source file is part of an OSTIS project. For the latest info, see http://ostis.net
 * Distributed under the MIT License
 * (See accompanying file COPYING.MIT or copy at http://opensource.org/licenses/MIT)
 */

#include "test_sc_agent_commands.hpp"

#include "sc-memory/sc_timer.hpp"
#include "sc-memory/sc_wait.hpp"
#include "sc-test-framework/sc_test_unit.hpp"

#include <thread>

ScAddr ATestCommandEmit::ms_keynodeParam1;
ScAddr ATestCommandEmit::ms_keynodeParam2;

utils::ScLock testInitLock;
SC_AGENT_ACTION_IMPLEMENTATION(ATestCommandEmit)
{
  if (GetParam(requestAddr, 0) == ATestCommandEmit::ms_keynodeParam1 &&
      GetParam(requestAddr, 1) == ATestCommandEmit::ms_keynodeParam2)
  {
    testInitLock.Unlock();
    return SC_RESULT_OK;
  }

  testInitLock.Unlock();
  return SC_RESULT_ERROR;
}

UNIT_TEST(ATestCommandEmit)
{
  ScMemoryContext ctx(sc_access_lvl_make_min, "ATestCommandEmit");
  ATestCommandEmit::InitGlobal();

  SC_AGENT_REGISTER(ATestCommandEmit);

  testInitLock.Lock();
  ScAddr const cmd = ScAgentAction::CreateCommand(
    ctx,
    ATestCommandEmit::GetCommandClassAddr(),
    { ATestCommandEmit::ms_keynodeParam1, ATestCommandEmit::ms_keynodeParam2 });

  SC_CHECK(cmd.IsValid(), ());

  ScWaitActionFinished waiter(ctx, cmd);
  waiter.SetOnWaitStartDelegate([&]() {
    ScAgentAction::InitiateCommand(ctx, cmd);
  });
  waiter.Wait();
  SC_CHECK_EQUAL(ScAgentAction::GetCommandResultCode(ctx, cmd), SC_RESULT_OK, ());

  SC_AGENT_UNREGISTER(ATestCommandEmit);
}
