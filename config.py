

import random
import os
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fixed seed for reproducibility
SEED = 20261022

random.seed(SEED)
np.random.seed(SEED)

# Master data requirements
NUM_PLANTS = 3
NUM_LINES = 12
NUM_MACHINES = 100
NUM_SENSORS = 500

# Observation period
DAYS = 90

# Dataset generation mode
STARTER_MODE = True

STARTER_READINGS = 10000
FULL_READINGS = 1000000

# Database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "predictive_maintenance_db")
