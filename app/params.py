from os import environ
# from app import categories

PROVIDERS = {
    'kingspeak': {
        'CHPC_SERVER': 'kingspeak',
        'SBATCH_ACCOUNT': 'owner-guest',
        'SBATCH_PARTITION': 'kingspeak-guest'
    },
    'sensale': {
        'CHPC_SERVER': 'kingspeak',
        'SBATCH_ACCOUNT': 'sensale',
        'SBATCH_PARTITION': 'kingspeak'
    },
    'ember': {
        'CHPC_SERVER': 'ember',
        'SBATCH_ACCOUNT': 'sensale',
        'SBATCH_PARTITION': 'ember'
    },
    'ash': {
        'CHPC_SERVER': 'ash-guest',
        'SBATCH_ACCOUNT': 'smithp-guest',
        'SBATCH_PARTITION': 'ash-guest'
    },
    'tangent': {
        'CHPC_SERVER': 'tangent',
        'SBATCH_ACCOUNT': 'sensale',
        'SBATCH_PARTITION': 'tangent'
    }
}

# CATEGORIES = categories.CATEGORIES

CURRENT_PROVIDER = PROVIDERS['sensale']

CHPC_PWD = '5896397Wxb@'  # environ['CHPC_PWD']
CHPC_SERVER = CURRENT_PROVIDER['CHPC_SERVER']
CHPC_USER = 'u0930578'
CHPC_LOGIN = '%s@%s.chpc.utah.edu' % (CHPC_USER, CHPC_SERVER)

SBATCH_ACCOUNT = CURRENT_PROVIDER['SBATCH_ACCOUNT']
SBATCH_PARTITION = CURRENT_PROVIDER['SBATCH_PARTITION']

CHPC_WORK_DIR = '/scratch/kingspeak/serial/u0930578/meep-workdir'

# ==================
# layout of element
# ==================

RESOLUTION = 50

# ==================
# probabilities
# ==================

DEFECT_MAX_PERCENT = 27
DEFECT_MIN_PERCENT = 25

GENERATE_BY_MUTATION_PROBABILITY = 0.9

# ==================
# genetic algorithm
# ==================

MUTATION_PROBABILITY = 0.015
CROSSOVER_PROBABILITY = 0.7
