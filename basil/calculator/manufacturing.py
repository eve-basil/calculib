import math

from functools import reduce
from operator import mul


def calc_mats(runs, quantity, me_bonuses):
    """
    Calculate material requirement for one material in a manufacturing job.

    :param runs: Number of runs in the job.
    :param quantity: Raw quantity of a material required for one run.
    :param me_bonuses: List of factors influencing material efficiency. This
           may include blueprint ME research (1% per level) and/or facility
           bonus used as a bonus of the job's build material requirements.
           Factors should be represented as a percent bonus (e.g. 5%
           reduction in material requirements appears in the list as 5 and a
           5% increase in material requirements appears as -5).
    :return: number of the material required for the job
    """
    if not isinstance(me_bonuses, list):
        me_bonuses = [me_bonuses]

    factors = [runs, quantity] + [1 - (float(x) / 100.0) for x in me_bonuses]
    return max(runs, math.ceil(reduce(mul, factors, 1)))


def calc_time(runs, time, te_bonuses):
    """
    Calculate time requirement for a manufacturing job.

    :param runs: Number of runs in the job.
    :param time: Raw time in seconds for one run.
    :param te_bonuses: List of factors influencing time efficiency. This
           may include blueprint TE research (1% per level) and/or skill,
           implant, and facility bonuses used as a bonus of the job's build
           material requirements. Factors should be represented as a percent
           bonus. (e.g. 5% reduction in material requirements appears in the
           list as 5.
    :return: number of seconds for the job
    """
    # The formula is the same
    return calc_mats(runs, time, te_bonuses)


def calc_install(runs, cost_index, system_index, tax_rate):
    """
    Calculate total install cost for a manufacturing job.

    :param runs: Number of runs in the job.
    :param cost_index: Cost Index for the item.
    :param system_index: Cost Index for the star system where construction
           would occur.
    :param tax_rate: Tax rate for the facility where construction would occur.
           Rate should be represented as a percent. (e.g. the 10% of cost
           index tax charged in NPC stations is given as 10)
    :return:
    """
    job_fee = runs * float(cost_index) * float(system_index)
    facility_tax = job_fee * float(tax_rate) / 100
    return job_fee + facility_tax
