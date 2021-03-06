import datetime

from model_mommy import mommy
import pytest

from usaspending_api.etl.award_helpers import update_awards, update_contract_awards
from usaspending_api.references.models import Agency


@pytest.mark.django_db
def test_award_update_from_latest_transaction(agencies):
    """Test awards fields that should be updated with most recent transaction info."""

    agency1 = Agency.objects.get(id=1)
    agency2 = Agency.objects.get(id=2)

    award = mommy.make(
        'awards.Award',
        awarding_agency=agency1,
        period_of_performance_current_end_date=datetime.date(2016, 1, 1),
        description='original award'
    )

    # adding transaction with same info should not change award values
    transaction = mommy.make(
        'awards.Transaction',
        award=award,
        awarding_agency=award.awarding_agency,
        period_of_performance_current_end_date=award.period_of_performance_current_end_date,
        description=award.description,
        action_date=datetime.date(2016, 2, 1)
    )

    update_awards()
    award.refresh_from_db()

    assert award.awarding_agency == agency1
    assert award.period_of_performance_current_end_date == datetime.date(2016, 1, 1)
    assert award.description == 'original award'
    assert award.latest_transaction == transaction

    # adding an older transaction with different info updates award's total
    # obligation amt and the description (which is sourced from the
    # earliest txn), but other info remains unchanged
    mommy.make(
        'awards.Transaction',
        award=award,
        awarding_agency=agency2,
        period_of_performance_current_end_date=datetime.date(2017, 1, 1),
        description='older description',
        action_date=datetime.date(2016, 1, 1)
    )
    update_awards()
    award.refresh_from_db()

    assert award.awarding_agency == agency1
    assert award.period_of_performance_current_end_date == datetime.date(2016, 1, 1)
    assert award.description == 'older description'

    # adding an newer transaction with different info updates award's total
    # obligation amt and also overrides other values
    mommy.make(
        'awards.Transaction',
        id=999,
        award=award,
        awarding_agency=agency2,
        period_of_performance_current_end_date=datetime.date(2010, 1, 1),
        description='new description',
        action_date=datetime.date(2017, 1, 1)
    )

    update_awards()
    award.refresh_from_db()

    assert award.awarding_agency == agency2
    assert award.period_of_performance_current_end_date == datetime.date(2010, 1, 1)
    # award desc should still reflect the earliest txn
    assert award.description == 'older description'


@pytest.mark.django_db
def test_award_update_from_earliest_transaction():
    """Test awards fields that should be updated with most earliest transaction info."""

    award = mommy.make('awards.Award')
    mommy.make(
        'awards.Transaction',
        award=award,
        # since this is the award's first transaction,
        # the txn action_date will become the award
        # signed date
        action_date=datetime.date(2016, 1, 1)
    )

    # adding later transaction should not change award values
    mommy.make(
        'awards.Transaction',
        award=award,
        action_date=datetime.date(2017, 1, 1)
    )

    update_awards()
    award.refresh_from_db()

    assert award.date_signed == datetime.date(2016, 1, 1)

    # adding earlier transaction should update award values
    mommy.make(
        'awards.Transaction',
        award=award,
        action_date=datetime.date(2010, 1, 1)
    )

    update_awards()
    award.refresh_from_db()

    assert award.date_signed == datetime.date(2010, 1, 1)


@pytest.mark.django_db
def test_award_update_obligated_amt():
    """Test that the award obligated amt updates as child transactions change."""

    award = mommy.make('awards.Award', total_obligation=1000)
    mommy.make(
        'awards.Transaction',
        award=award,
        federal_action_obligation=1000,
        _quantity=5
    )

    update_awards()
    award.refresh_from_db()

    assert award.total_obligation == 5000


@pytest.mark.django_db
def test_award_update_with_list(agencies):
    """Test optional parameter to update specific awards with txn data."""
    awards = mommy.make('awards.Award', total_obligation=0, _quantity=10)
    test_award = awards[3]

    # test a single award update
    mommy.make(
        'awards.Transaction',
        award=test_award,
        federal_action_obligation=1000,
        _quantity=5
    )
    count = update_awards((test_award.id,))
    test_award.refresh_from_db()
    # one award is updated
    assert count == 1
    # specified award is updated
    assert test_award.total_obligation == 5000
    # other awards not updated
    assert awards[0].total_obligation == 0

    # test updating several awards
    mommy.make(
        'awards.Transaction',
        award=awards[0],
        federal_action_obligation=2000,
        _quantity=2
    )
    mommy.make(
        'awards.Transaction',
        award=awards[1],
        federal_action_obligation=-1000,
        _quantity=3
    )
    count = update_awards((awards[0].id, awards[1].id))
    awards[0].refresh_from_db()
    awards[1].refresh_from_db()
    # two awards are updated
    assert count == 2
    # specified awards are updated
    assert awards[0].total_obligation == 4000
    assert awards[1].total_obligation == -3000
    # other awards not updated
    assert awards[4].total_obligation == 0


@pytest.mark.django_db
def test_award_update_from_contract_transaction():
    """Test award updates specific to contract transactions."""

    # for contract type transactions,
    # the potential_total_value_of_award field
    # should updte the corresponding field on the award table
    award = mommy.make('awards.Award')
    txn = mommy.make('awards.Transaction', award=award)
    txn2 = mommy.make('awards.Transaction', award=award)
    mommy.make(
        'awards.TransactionContract',
        transaction=txn,
        potential_total_value_of_award=1000
    )
    mommy.make(
        'awards.TransactionContract',
        transaction=txn2,
        potential_total_value_of_award=1001
    )

    update_contract_awards()
    award.refresh_from_db()

    assert award.potential_total_value_of_award == 2001


@pytest.mark.django_db
def test_award_update_contract_txn_with_list(agencies):
    """Test optional parameter to update specific awards from txn contract."""

    awards = mommy.make('awards.Award', _quantity=5)
    txn = mommy.make('awards.Transaction', award=awards[0])
    mommy.make(
        'awards.TransactionContract',
        transaction=txn,
        potential_total_value_of_award=1000
    )
    # single award is updated
    count = update_contract_awards((awards[0].id,))
    awards[0].refresh_from_db()
    assert count == 1
    assert awards[0].potential_total_value_of_award == 1000

    # update multipe awards
    txn1 = mommy.make('awards.Transaction', award=awards[1])
    mommy.make(
        'awards.TransactionContract',
        transaction=txn1,
        potential_total_value_of_award=4000
    )
    txn2 = mommy.make('awards.Transaction', award=awards[2])
    mommy.make(
        'awards.TransactionContract',
        transaction=txn2,
        potential_total_value_of_award=5000
    )
    # multiple awards updated
    count = update_contract_awards((awards[1].id, awards[2].id))
    awards[1].refresh_from_db()
    awards[2].refresh_from_db()
    assert count == 2
    assert awards[1].potential_total_value_of_award == 4000
    assert awards[2].potential_total_value_of_award == 5000


@pytest.mark.skip(reason="deletion feature not yet implemented")
@pytest.mark.django_db
def test_deleted_transactions():
    """Test that award values are updated correctly when a txn is deleted."""
    # writing these tests revealed that we're not updating awards fields
    # when transactions are deleted. since the Transaction model's delete()
    # method may not fire during a bulk deletion, we may want to use a signal
    # rather than override delete()
