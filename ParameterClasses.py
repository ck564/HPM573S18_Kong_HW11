from enum import Enum
import InputData as Data
import numpy as np
import scr.MarkovClasses as MarkovCls


class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEATH = 3
    BACKGROUND_DEATH = 4


class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    ANTICOAG = 1


class ParametersFixed:
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.NONE:
            self._prob_matrix = Data.TRANS_MATRIX
            if Data.ADD_BACKGROUND_MORT:
                add_background_mortality(self._prob_matrix)
        else:
            self._prob_matrix = calculate_prob_matrix_anticoag()

        # calculate annual treatment cost
        if self._therapy == Therapies.ANTICOAG:
            self._annual_drug_cost = Data.DRUG_COST
        else:
            self._annual_drug_cost = 0

        # calcualte adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT_RATE * Data.DELTA_T

        # annual state costs and utilities
        self._annualStateCosts = Data.COST_STATE
        self._annualStateUtilities = Data.HEALTH_UTILITY

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_annual_drug_cost(self):
        return self._annual_drug_cost

    def get_annual_state_costs(self, state):
        if state == HealthStats.DEATH or state == HealthStats.BACKGROUND_DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utilities(self, state):
        if state == HealthStats.DEATH or state == HealthStats.BACKGROUND_DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]


def add_background_mortality(prob_matrix):
    # find transition rate matrix
    rate_matrix = MarkovCls.discrete_to_continuous(prob_matrix, 1)
    # add mortality rates
    for s in HealthStats:
        # add background rates to non-death states
        if s not in [HealthStats.DEATH, HealthStats.BACKGROUND_DEATH]:
            rate_matrix[s.value][HealthStats.BACKGROUND_DEATH.value] \
                = -np.log(1-Data.ANNUAL_PROB_BACKGROUND_MORT)

    # convert back to transition probability matrix
    prob_matrix[:], p = MarkovCls.continuous_to_discrete(rate_matrix, Data.DELTA_T)


def calculate_prob_matrix_anticoag():
    """ :returns transition probability matrix under anticoagulation use"""

    # create an empty matrix populated with zeroes
    prob_matrix = []
    for s in HealthStats:
        prob_matrix.append([0] * len(HealthStats))
    # # for all health states
    # for s in HealthStats:
    #     # if the current state is post-stroke
    #     if s == HealthStats.POST_STROKE:
    #         # post-stoke to stroke
    #         prob_matrix[s.value][HealthStats.STROKE.value]\
    #             = Data.RR_STROKE*Data.TRANS_MATRIX[s.value][HealthStats.STROKE.value]
    #         # post-stroke to death
    #         prob_matrix[s.value][HealthStats.DEATH.value] \
    #             = Data.RR_STROKE * Data .RR_BLEEDING * Data.TRANS_MATRIX[s.value][HealthStats.DEATH.value]
    #         # staying in post-stroke
    #         prob_matrix[s.value][s.value]\
    #             = 1 - prob_matrix[s.value][HealthStats.STROKE.value] - prob_matrix[s.value][HealthStats.DEATH.value]
    #     else:
    #         prob_matrix[s.value] = Data.TRANS_MATRIX[s.value]

    for s in HealthStats:
        if s == HealthStats.POST_STROKE:
            prob_matrix[s.value][HealthStats.STROKE.value] \
                = 0.75 * Data.RATE_MATRIX[s.value][HealthStats.STROKE]

            prob_matrix[s.value][HealthStats.BACKGROUND_DEATH.value] \
                = 1.05 * Data.RATE_MATRIX[s.value][HealthStats.BACKGROUND_DEATH]
        else:
            prob_matrix[s.value] = Data.TRANS_MATRIX[s.value]

    return prob_matrix
