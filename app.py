import streamlit as st
import pandas as pd
from ahp_functions import (
    create_comparison_matrix, normalize_matrix, calculate_priority_vector,
    calculate_lambda_max, calculate_consistency_index, calculate_consistency_ratio
)

# --- Configuração da página --- #
st.set_page_config(
    page_title='AHP CALC',
    layout='wide'
)

st.title("Método AHP")

st.markdown(
    """
O método AHP proposto por Saaty é um processo robusto na análise multicritério.
Este app, tem como proposta ser um ferramenta acessível para o cálculo 
das Matrizes de comparação pareada e normalizada, bem como os cálculos 
dos vetores, Lambda máximo, Índice de Consistência, IC e RC.
"""
)

st.header("1. Montagem da matriz de comparação pareada")

# Inicializar o estado da sessão para armazenar fatores e valores da matriz
if 'factors' not in st.session_state:
    st.session_state.factors = []

if 'matrix_values' not in st.session_state:
    st.session_state.matrix_values = {}

# Entrada para a quantidade de fatores
num_factors  = st.number_input("Quantidade de fatores", min_value=2, step=1, value=len(st.session_state.factors) or 2)

# Entradas para os nomes dos fatores
factors = st.session_state.factors
columns = st.columns(num_factors)
for i in range(num_factors):
    with columns[i]:
        factor_name = st.text_input(f"Fator {i + 1}", value=factors[i] if i < len(factors) else "", key=f"factor_{i}")
        if i < len(factors):
            factors[i] = factor_name
        else:
            factors.append(factor_name)

# Atualizar o estado da sessão com os fatores
st.session_state.factors = factors

# Gerar a matriz se todos os fatores forem fornecidos
if len(factors) == num_factors and all(factors):
    st.subheader("1.1 Definindo peso dos fatores")

    matrix = create_comparison_matrix(factors)

    # Entradas para peso dos fatores (células acima da diagonal principal)
    for i in range(num_factors):
        if num_factors - i - 1 > 0:
            columns = st.columns(num_factors - i - 1)
            for j in range(i+1, num_factors):
                with columns[j-i-1]:
                    key = f"{i}-{j}"
                    value = st.session_state.matrix_values.get(key, 1.0)
                    cell_value = st.number_input(f"{factors[i]} vs {factors[j]}", min_value=0.01, step=0.01, value=value, key=key)
                    matrix.iloc[i, j] = cell_value
                    matrix.iloc[j, i] = 1 / cell_value
                    
                    # Atualizar o estado da sessão com os valores da matriz
                    st.session_state.matrix_values[key] = cell_value

    st.subheader("1.2 Matriz de Comparação Pareada")
    st.dataframe(matrix.style.format(precision=3))
    
    st.subheader("1.3 Somatório das colunas")
    column_sums = matrix.sum(axis=0)
    st.write(column_sums.round(3))

    st.subheader("1.4 Matriz Normalizada")
    normalized_matrix = normalize_matrix(matrix)
    st.dataframe(normalized_matrix.style.format(precision=3))

    st.subheader("1.5 Vetor de Prioridades")
    priority_vector = calculate_priority_vector(normalized_matrix)
    st.write(priority_vector.round(3))

    st.subheader("1.6 Cálculo de Consistência")
    lambda_max = calculate_lambda_max(matrix, priority_vector)
    st.write(f"Lambda Máximo: {lambda_max:.3f}")

    consistency_index = calculate_consistency_index(lambda_max, num_factors)
    st.write(f"Índice de Consistência (IC): {consistency_index:.3f}")

    consistency_ratio = calculate_consistency_ratio(consistency_index, num_factors)
    st.write(f"Razão de Consistência (RC): {consistency_ratio:.3f}")

    if consistency_ratio < 0.1:
        st.success("A matriz de comparação é consistente.")
    else:
        st.warning("A matriz de comparação não é consistente. Considere revisar os pesos.")
else:
    st.write("Por favor, preencha todos os nomes dos fatores.")
    
# Botão para resetar a sessão
if st.button("Resetar"):
    st.session_state.factors = []
    st.session_state.matrix_values = {}
    st.rerun()
