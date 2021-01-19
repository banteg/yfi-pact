import pytest


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture()
def yfi(interface):
    return interface.YFI("0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e")


@pytest.fixture()
def timelock(interface, a):
    timelock = interface.Timelock("0x026d4b8d693f6c446782c2c61ee357ec561dfb61")
    gov = a.at(timelock.governance(), force=True)
    return interface.Timelock(timelock, owner=gov)


@pytest.fixture()
def pact(YearnPact, a):
    return YearnPact.deploy({"from": a[0]})


@pytest.fixture()
def treasury(a, web3):
    return a.at(web3.ens.resolve("ychad.eth"), force=True)
