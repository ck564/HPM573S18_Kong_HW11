import HW11P1 as R

POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 15     # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DELTA_T = 1/12      # years (length of time step, how frequently you look at the patient)
DISCOUNT_RATE = 0.03

# transition matrix
TRANS_MATRIX = [
    [0.75,  0.15,   0.0,    0.1],   # Well
    [0,     0.0,    1.0,    0.0],   # Stroke
    [0,     0.25,   0.55,   0.2],   # Post-Stroke
    [0.0,   0.0,    0.0,    1.0],   # Dead
    ]

# anticoagulation relative risk in reducing stroke incidence and stroke death while in “Post-Stroke”
RR_STROKE = 0.65
# anticoagulation relative risk in increasing mortality due to bleeding is 1.05.
RR_BLEEDING = 1.05

# annual cost of anticoagulation drug
DRUG_COST = 2000

# annual cost
COST_STATE = [
    0,      # Well
    0,      # Stroke
    200,    # Post-Stroke
    0       # Dead
]

# cost of stroke
COST_STROKE = 5000

# health utility
HEALTH_UTILITY = [
    1.0,     # Well
    0.2,     # Stroke
    0.9,     # Post-Stroke
    0.0      # Dead
]

RATE_MATRIX = [
    [0, R.d, 0, R.b],
    [0, 0, R.i, R.e],
    [0, R.g, 0, R.h],
    [0, 0, 0, 0]
]

RATE_MATRIX_TX = [
    [0, R.d, 0, R.b],
    [0, 0, R.i, R.e],
    [0, 0.75 * R.g, 0, 1.05 * R.h],
    [0, 0, 0, 0]
]

ANNUAL_PROB_BACKGROUND_MORT = 18 / 1000
ADD_BACKGROUND_MORT = True

print(RATE_MATRIX)
print(RATE_MATRIX_TX)
