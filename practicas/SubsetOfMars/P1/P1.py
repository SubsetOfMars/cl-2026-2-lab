# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: P1 (3.12.13)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Práctica 1 - Lingüística Computacional
#

# %% [markdown]
# # Fonética

# %%
from collections import defaultdict

import pandas as pd
import requests

# %%
IPA_URL = "https://raw.githubusercontent.com/open-dict-data/ipa-dict/master/data/{lang}.txt"

# %%
response = requests.get(IPA_URL.format(lang="es_MX"))

# %%
ipa_list = response.text.split("\n")

# %%
ipa_list[0].split("\t")


# %%
def download_ipa_corpus(iso_lang: str) -> str:
    """
    Descarga el archivo del diccionario IPA para el idioma dado.
    """
    print(f"Descargando {iso_lang}...", end=" ")
    response = requests.get(IPA_URL.format(lang=iso_lang))
    print(f"status={response.status_code}")
    
    if response.status_code != 200:
        print(f"Error al descargar el corpus para {iso_lang}")
        return ""
    
    return response.text


# %%
def parse_response(response: str) -> dict:
    """
    Convierte el texto crudo del diccionario IPA en un diccionario de Python.
    Formato esperado por línea: palabra[TAB]ipa
    """
    ipa_list = response.rstrip().split("\n")
    result = {}
    
    for item in ipa_list:
        if item == "":
            continue
        
        item_list = item.split("\t")
        
        if len(item_list) == 2:
            word, ipa = item_list
            result[word] = ipa
    
    return result


# %%
es_data = parse_response(download_ipa_corpus("es_MX"))


# %%
def get_ipa_transcriptions(word: str, dataset: dict) -> list[str]:
    """
    Busca una palabra en el diccionario y devuelve sus transcripciones IPA.
    Si no existe, devuelve lista vacía.
    """
    return dataset.get(word.lower(), "").split(", ") if dataset.get(word.lower(), "") else []


# %%
get_ipa_transcriptions("mayonesa", es_data)


# %%
def levenshtein(s1: str, s2: str) -> int:
    """
    Calcula la distancia de Levenshtein entre dos cadenas.
    """
    m = len(s1)
    n = len(s2)

    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                costo = 0
            else:
                costo = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + costo
            )

    return dp[m][n]


# %%
def encontrar_palabra_mas_cercana(palabra: str, dataset: dict) -> str:
    """
    Encuentra la palabra más cercana en el diccionario usando distancia de Levenshtein.
    """

    palabra_mas_cercana = None
    distancia_minima = float("inf")

    for palabra_dic in dataset.keys():
        distancia = levenshtein(palabra.lower(), palabra_dic.lower())

        if distancia < distancia_minima:
            distancia_minima = distancia
            palabra_mas_cercana = palabra_dic

    return palabra_mas_cercana


# %%
def obtener_ipa_aproximado(palabra: str, dataset: dict) -> dict:
    """
    Busca la transcripción IPA de una palabra.
    Si no existe en el diccionario, aproxima usando la palabra más cercana.
    """

    resultado_exacto = get_ipa_transcriptions(palabra, dataset)

    if resultado_exacto:
        return {
            "encontrada": True,
            "palabra_ingresada": palabra,
            "palabra_coincidente": palabra.lower(),
            "transcripciones": resultado_exacto
        }

    palabra_cercana = encontrar_palabra_mas_cercana(palabra, dataset)
    transcripcion_aprox = get_ipa_transcriptions(palabra_cercana, dataset)

    return {
        "encontrada": False,
        "palabra_ingresada": palabra,
        "palabra_coincidente": palabra_cercana,
        "transcripciones": transcripcion_aprox
    }


# %%
from pprint import pprint

# %%
print(obtener_ipa_aproximado("tomate", es_data))
print(obtener_ipa_aproximado("cassa", es_data))
print(obtener_ipa_aproximado("cucharacha", es_data))

# %% [markdown]
# # Morfología
