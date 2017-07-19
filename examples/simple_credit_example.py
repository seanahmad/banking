import pandas as pd
from credit.prepayment import PrepaymentModel
from rates.models import InterestRateModel
from credit.forecast import vintage_settings
from credit.forecast import get_budget
from credit.vintages import CreditVintage
from credit.vintages import CreditVintageCollection
from common.presentation import tabulate_print


if __name__ == '__main__':

    prod = 'tarjeta de credito'
    initial_date = '01-31-2017'
    budget = get_budget(product_name = prod, sdate = initial_date)
    fore = len(budget)*12

    prep_array = PrepaymentModel.psa(nper = fore,
                                     ceil = 0.03,
                                     stable_period = 12)

    index_array = InterestRateModel.zero(nper = fore,
                                         fecha_inicial = initial_date)

    collection = CreditVintageCollection(per_score = False)
    for sdate, m_disbur in budget.iteritems():

        settings = vintage_settings(product_name = prod,
                                    sdate = sdate,
                                    disburment = m_disbur,
                                    fore_length = fore,
                                    prepay_array = prep_array,
                                    index_array = index_array)

        my_vintage = CreditVintage(settings = settings)

        print("#########################################")
        print("# THE ORIGINAL VINTAGE")
        print("#########################################")
        tabulate_print(my_vintage.get_balance(per_score = False))
        print('\n', '\n')

        #collection = collection.add(my_vintage)

    #tabulate_print(collection.get_balance())

