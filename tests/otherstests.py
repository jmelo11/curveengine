
from parsing.others import *


def testCreateOvernightIndex():
    index = createOvernightIndex(
        'USDLibor', 2, 'USD', 'UnitedStates', 'Actual360')
    assert index.fixingDays() == 2
    assert index.currency() == ore.USDCurrency()
    assert index.fixingCalendar() == ore.UnitedStates(ore.UnitedStates.GovernmentBond)
    assert index.dayCounter() == ore.Actual360()
    try:
        createOvernightIndex('unknown', 2, 'USD', 'UnitedStates',
                             'ModifiedFollowing', False, 'Actual360')
        assert False
    except Exception as e:
        assert True


def testCreateIborIndex():
    index = createIborIndex('USDLibor', 2, '1M', 'USD',
                            'UnitedStates', 'ModifiedFollowing', False, 'Actual360')
    assert index.fixingDays() == 2
    assert index.tenor() == ore.Period(1, ore.Months)
    assert index.currency() == ore.USDCurrency()
    assert index.fixingCalendar() == ore.UnitedStates(ore.UnitedStates.GovernmentBond)
    assert index.businessDayConvention() == ore.ModifiedFollowing
    assert index.endOfMonth() == False
    assert index.dayCounter() == ore.Actual360()
    try:
        createIborIndex('unknown', 2, '1M', 'USD', 'UnitedStates',
                        'ModifiedFollowing', False, 'Actual360')
        assert False
    except Exception as e:
        assert True


def testCreateInterestRate():
    assert createInterestRate(0.01, 'Actual360', 'Simple', 'Annual').rate() == ore.InterestRate(
        0.01, ore.Actual360(), ore.Simple, ore.Annual).rate()
    try:
        createInterestRate(0.01, 'unknown', 'Simple', 'Annual')
        assert False
    except Exception as e:
        assert True
    try:
        createInterestRate(0.01, 'Actual360', 'unknown', 'Annual')
        assert False
    except Exception as e:
        assert True
    try:
        createInterestRate(0.01, 'Actual360', 'Simple', 'unknown')
        assert False
    except Exception as e:
        assert True
