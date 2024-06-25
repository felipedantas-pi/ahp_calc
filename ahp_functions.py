import numpy as np
import pandas as pd

def create_comparison_matrix(factors):
    """Cria a matriz de comparação pareada."""
    n = len(factors)
    matrix = pd.DataFrame(index=factors, columns=factors, data=1.0)
    return matrix

def normalize_matrix(matrix):
    """Normaliza a matriz de comparação."""
    column_sums = matrix.sum(axis=0)
    normalized_matrix = matrix / column_sums
    return normalized_matrix

def calculate_priority_vector(normalized_matrix):
    """Calcula o vetor de prioridades."""
    return normalized_matrix.mean(axis=1)

def calculate_lambda_max(matrix, priority_vector):
    """Calcula Lambda Máximo."""
    weighted_sum_vector = matrix.dot(priority_vector)
    lambda_max = np.mean(weighted_sum_vector / priority_vector)
    return lambda_max

def calculate_consistency_index(lambda_max, num_factors):
    """Calcula o Índice de Consistência (IC)."""
    return (lambda_max - num_factors) / (num_factors - 1)

def calculate_consistency_ratio(consistency_index, num_factors):
    """Calcula a Razão de Consistência (RC)."""
    random_index = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
    }
    ri = random_index.get(num_factors, 1.49)  # Default to 1.49 if num_factors > 10
    return consistency_index / ri
