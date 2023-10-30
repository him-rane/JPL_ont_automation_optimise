import pytest

from functional_smoke import functional_smoke
from setup import Setup

setup = Setup()
setup.update_driver()
driver = setup.get_driver()
obj = functional_smoke(driver)

def test_1():
    assert obj.TC_Functional_Smoke_10()

def test_2():
    assert obj.TC_Functional_Smoke_26()

def test_3():
    assert obj.TC_Functional_Smoke_27()
def test_4():
    assert obj.TC_Functional_Smoke_28_1()

def test_5():
    assert obj.TC_Functional_Smoke_28_1()
def test_6():
    assert obj.TC_Functional_Smoke_28_2()

def test_7():
    assert obj.TC_Functional_Sanity_002_1()
def test_8():
    assert obj.TC_Functional_Sanity_002_2()
def test_9():
 assert obj.TC_Functional_Sanity_002_3()


