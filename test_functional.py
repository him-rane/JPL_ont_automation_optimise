import pytest

from functional_smoke import functional_smoke
from setup import Setup

setup = Setup()
setup.update_driver()
driver = setup.get_driver()
obj = functional_smoke(driver)



def test_Functional_Sanity_002_1():
    assert obj.TC_Functional_Sanity_002_1()
def test_Functional_Sanity_002_2():
    assert obj.TC_Functional_Sanity_002_2()
def test_Functional_Sanity_002_3():
    assert obj.TC_Functional_Sanity_002_3()

def test_Functional_Sanity_4():
    assert obj.TC_Functional_Smoke_4()
def test_Functional_Sanity_5():
    assert obj.TC_Functional_Sanity_5()
def test_Functional_Sanity_7():
    assert obj.TC_Functional_Sanity_7()

def test_Functional_Sanity_9():
    assert obj.TC_Finctional_Smoke_9()

def test_Functional_Sanity_10():
    assert obj.TC_Functional_Smoke_10()

def test_Functional_Sanity_12_47():
    assert obj.TC_Functional_Smoke_12_47()

def test_Functional_Sanity_26():
    assert obj.TC_Functional_Smoke_26()

def test_Functional_Sanity_27():
    assert obj.TC_Functional_Smoke_27()

def test_Functional_Sanity_28_1():
    assert obj.TC_Functional_Smoke_28_1()

def test_Functional_Sanity_28_2():
    assert obj.TC_Functional_Smoke_28_2()

def test_Functional_Sanity_29_30():
    assert obj.TC_Functional_Smoke_29_30()

def test_Functional_Sanity_32():
    assert obj.TC_Functional_Smoke_32()

def test_Functional_Sanity_33():
    assert obj.TC_Functional_Smoke_33()

def test_Functional_Sanity_35():
    assert obj.TC_Functional_Smoke_35()

def test_Functional_Sanity_36():
    assert obj.TC_Functional_Smoke_36()

def test_Functional_Sanity_37():
    assert obj.TC_Functional_Smoke_37()

def test_Functional_Sanity_39():
    assert obj.TC_Functional_Smoke_39()

def test_Functional_Sanity_40():
    assert obj.TC_Functional_Smoke_40()

def test_Functional_Sanity_41():
    assert obj.TC_Functional_Smoke_41()
def test_Functional_Sanity_42():
    assert obj.TC_Functional_Smoke_42()

def test_Functional_Sanity_46():
    assert obj.TC_Functional_Smoke_42()

def test_Functional_Sanity_55():
    assert obj.TC_Functional_Sanity_55()

def test_Functional_Sanity_56():
    assert obj.TC_Functional_Sanity_56()

def test_Functional_Sanity_57():
    assert obj.TC_Functional_Smoke_57()


