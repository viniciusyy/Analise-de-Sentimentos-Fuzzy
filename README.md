# Analise de Sentimentos Fuzzy

Este repositório contém uma implementação de um sistema de análise de sentimentos baseado em lógica fuzzy. O objetivo é determinar, a partir de um comentário (por exemplo, em redes sociais), se o sentimento expresso é **POSITIVO**, **NEGATIVO** ou **NEUTRO**. O sistema avalia variáveis como:

- **FP (Frequência de palavras-chave positivas):** Medida da presença e quantidade de palavras com conotação positiva.
- **FN (Frequência de palavras-chave negativas):** Medida da presença e quantidade de palavras com conotação negativa.
- **I (Intensificadores):** Palavras que reforçam ou aumentam o grau de emoção.
- **N (Negações):** Palavras que invertem ou anulam o sentido de termos positivos ou negativos.

O código utiliza funções de pertinência (usando funções triangulares e trapezoidais) para modelar os conjuntos fuzzy e aplica regras de inferência para determinar a polaridade do sentimento em um comentário.

---

## Descrição

O sistema realiza a análise fuzzy em diversas etapas:

1. **Pré-processamento do Texto:**  
   - Converte o texto para minúsculas.
   - Remove pontuações.
   - Realiza a tokenização do texto em palavras.

2. **Cálculo de Frequências:**  
   - As frequências de palavras positivas, negativas, intensificadores e negações são calculadas de forma normalizada com base no total de palavras-chave encontradas no comentário.

3. **Modelagem Fuzzy:**  
   - Cada variável (FP, FN, I, N) possui funções de pertinência definidas para três conjuntos (low, medium e high).
   - A variável de saída (Polaridade do Sentimento – PS) também possui funções de pertinência definidas para os conjuntos **negative**, **neutral** e **positive**.

4. **Inferência Fuzzy:**  
   - São definidas regras fuzzy que combinam as variáveis de entrada para inferir a polaridade do sentimento.  
   - Exemplos de regras incluem:  
     - Se FP for alta e a presença de intensificadores for alta (e não houver negação) → **POSITIVE**.  
     - Se FP for alta, mas houver também forte presença de negações sem intensificadores → **NEGATIVE**.  
     - Se FP e FN estiverem na faixa média, a saída tende para **NEUTRAL**.  
     - Uma regra adicional trata explicitamente do caso em que há exclusividade de termos positivos, classificando como **POSITIVE**.

---

## Integração com scikit-learn e scikit-fuzzy

Embora o **scikit-learn** seja uma biblioteca poderosa para tarefas de aprendizado de máquina, ele não possui suporte nativo para a implementação de lógica fuzzy. Para atender a essa necessidade, este projeto integra o **scikit-fuzzy**, uma biblioteca especializada na criação de sistemas de controle fuzzy. 

- **scikit-fuzzy:** Utilizado para definir as variáveis fuzzy, funções de pertinência e regras de inferência de forma modular e inspirada nas estruturas do scikit-learn.  
- **Complementaridade:** Enquanto o scikit-learn pode ser utilizado para tarefas de pré-processamento e outras análises estatísticas, o scikit-fuzzy cuida da parte fuzzy do sistema, possibilitando uma integração fluida entre técnicas tradicionais de machine learning e lógica fuzzy.

Essa abordagem permite uma aplicação flexível e extensível, onde futuras melhorias poderão incluir uma combinação de técnicas fuzzy com modelos baseados em scikit-learn.

---

## Requisitos

- **Python 3.x**
- **scikit-fuzzy**
- **numpy**

Para instalações adicionais ou tarefas de pré-processamento avançado, você pode também integrar o **scikit-learn** no seu fluxo de trabalho, embora a lógica fuzzy deste projeto seja implementada com o scikit-fuzzy.


