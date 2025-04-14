# Analise de Sentimentos Fuzzy

Este repositório contém uma implementação de um sistema de análise de sentimentos baseado em lógica fuzzy. O objetivo é determinar, a partir de um comentário (por exemplo, em redes sociais), se o sentimento expresso é **POSITIVO**, **NEGATIVO** ou **NEUTRO**. O sistema avalia variáveis como:

- **FP (Frequência de palavras-chave positivas):** Medida da presença e quantidade de palavras com conotação positiva.
- **FN (Frequência de palavras-chave negativas):** Medida da presença e quantidade de palavras com conotação negativa.
- **I (Intensificadores):** Palavras que reforçam o grau de emoção.
- **N (Negações):** Palavras que invertem ou negam o sentido de termos positivos ou negativos.

O código utiliza funções de pertinência do tipo triangular e funções "shoulder" para tratar valores extremos, bem como regras fuzzy customizadas que aplicam a lógica de negação e intensificação para definir a polaridade do sentimento.

---

## Descrição

A análise fuzzy é realizada em diversas etapas:

1. **Pré-processamento do Texto:**  
   O texto é convertido para minúsculas, os sinais de pontuação são removidos e ele é tokenizado em palavras.

2. **Cálculo de Frequências:**  
   São calculadas as frequências normalizadas das palavras positivas, negativas, intensificadores e negações. Nesta implementação, a normalização é realizada com base no total de palavras-chave encontradas no texto.

3. **Avaliação das Funções de Pertinência:**  
   Cada variável (FP, FN, I, N) é associada a conjuntos fuzzy (Baixa, Média e Alta) utilizando funções de pertinência triangulares e funções “shoulder” para capturar corretamente os extremos (valores 0 ou 1).

4. **Inferência Fuzzy e Regras:**  
   São definidas pelo menos 5 regras fuzzy, por exemplo:
   - **Regra 1:** Se FP é alta e N é baixa → SENTIMENTO POSITIVO.
   - **Regra 2:** Se FP é alta e N é alta → SENTIMENTO NEGATIVO (inversão de polaridade).
   - **Regra 3:** Se FN é alta e N é baixa → SENTIMENTO NEGATIVO.
   - **Regra 4:** Se FN é alta e N é alta → SENTIMENTO POSITIVO (inversão de polaridade).
   - **Regra 5:** Se FP e FN estão na faixa média → SENTIMENTO NEUTRO.

5. **Classificação Final:**  
   Após a agregação dos resultados das regras fuzzy, obtém-se um *score* final (valor entre 0 e 1). Com base nesse score, o comentário é classificado:
   - **NEGATIVO:** Se o score for inferior a 0.35.
   - **NEUTRO:** Se o score estiver entre 0.35 e 0.65.
   - **POSITIVO:** Se o score for superior a 0.65.

---

## Funcionalidades

- **Text Preprocessing:** Conversão para minúsculas, remoção de pontuação e tokenização.
- **Cálculo de Variáveis Fuzzy:** Extração e normalização das frequências de palavras positivas, negativas, intensificadores e negações.
- **Funções de Pertinência Customizadas:** Uso de funções triangulares e "shoulder" para refletir melhor os valores extremos.
- **Inferência Fuzzy:** Aplicação de regras fuzzy para determinar a polaridade do sentimento.
- **Exemplos de Demonstração:** O script inclui exemplos para testar o sistema com diferentes frases.

---

## Requisitos

- **Python 3.x**


---


