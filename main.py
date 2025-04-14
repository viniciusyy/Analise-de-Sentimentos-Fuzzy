import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import re

# ============================================
# Bancos de Palavras
# ============================================
positive_words = [
    "ótimo", "excelente", "incrível", "fantástico", "maravilhoso",
    "feliz", "surpreendente", "bonito", "gostei"
]
negative_words = [
    "péssimo", "horrível", "terrível", "desagradável", "decepcionante",
    "triste", "frustrante"
]
intensifiers = [
    "muito", "bastante", "extremamente", "incrivelmente",
    "realmente", "completamente"
]
negations = ["não", "jamais", "nenhum", "nem", "nada"]

# ============================================
# Funções para Pré-processamento e Cálculo de Frequências
# ============================================
def process_text(text):
    """
    Converte o texto para minúsculas, remove pontuações e separa em palavras.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return words

def calculate_frequencies(text):
    """
    Calcula as frequências normalizadas para palavras positivas (FP),
    negativas (FN), intensificadores (I) e negações (N) com base no
    total de palavras-chave encontradas no texto.
    """
    words = process_text(text)
    
    count_positive = sum(word in positive_words for word in words)
    count_negative = sum(word in negative_words for word in words)
    count_intensifier = sum(word in intensifiers for word in words)
    count_negation = sum(word in negations for word in words)
    
    total_keywords = count_positive + count_negative + count_intensifier + count_negation
    if total_keywords == 0:
        return 0, 0, 0, 0  # Evita divisão por zero
    
    FP = count_positive / total_keywords
    FN = count_negative / total_keywords
    I = count_intensifier / total_keywords
    N = count_negation / total_keywords
    
    return FP, FN, I, N

# ============================================
# Definição das Variáveis Fuzzy com scikit-fuzzy
# ============================================
x_FP = np.arange(0, 1.01, 0.01)
x_FN = np.arange(0, 1.01, 0.01)
x_I  = np.arange(0, 1.01, 0.01)
x_N  = np.arange(0, 1.01, 0.01)
x_PS = np.arange(0, 1.01, 0.01)  # Polaridade do Sentimento

FP_var = ctrl.Antecedent(x_FP, 'FP')
FN_var = ctrl.Antecedent(x_FN, 'FN')
I_var  = ctrl.Antecedent(x_I, 'I')
N_var  = ctrl.Antecedent(x_N, 'N')
PS_var = ctrl.Consequent(x_PS, 'PS')

# Para cada variável de entrada, usamos trapézio para "low" e "high"
for var in (FP_var, FN_var, I_var, N_var):
    var['low'] = fuzz.trapmf(var.universe, [0, 0, 0.15, 0.3])
    var['medium'] = fuzz.trimf(var.universe, [0.2, 0.4, 0.6])
    var['high'] = fuzz.trapmf(var.universe, [0.4, 0.7, 1, 1])

# Para a saída, definimos as funções de pertinência
PS_var['negative'] = fuzz.trapmf(x_PS, [0, 0, 0.15, 0.3])
PS_var['neutral']  = fuzz.trimf(x_PS, [0.2, 0.4, 0.6])
PS_var['positive'] = fuzz.trapmf(x_PS, [0.4, 0.7, 1, 1])

# ============================================
# Definição das Regras Fuzzy (atualizadas)
# ============================================
# Regra 1: Se FP é alta e I é alta e N é baixa → SENTIMENTO POSITIVE
rule1 = ctrl.Rule(FP_var['high'] & I_var['high'] & N_var['low'], PS_var['positive'])
# Regra 2: Se FP é alta e I é alta e N é alta → SENTIMENTO NEGATIVE (inversão)
rule2 = ctrl.Rule(FP_var['high'] & I_var['high'] & N_var['high'], PS_var['negative'])
# Regra 3: Se FN é alta e N é baixa → SENTIMENTO NEGATIVE
rule3 = ctrl.Rule(FN_var['high'] & N_var['low'], PS_var['negative'])
# Regra 4: Se FN é alta e N é alta → SENTIMENTO POSITIVE (inversão, se aplicável)
rule4 = ctrl.Rule(FN_var['high'] & N_var['high'], PS_var['positive'])
# Regra 5: Se FP e FN estão na faixa média → SENTIMENTO NEUTRAL
rule5 = ctrl.Rule(FP_var['medium'] & FN_var['medium'], PS_var['neutral'])
# Regra 6: Se FP é alta e N é alta e I é baixa (inversão sem intensificador) → SENTIMENTO NEGATIVE
rule6 = ctrl.Rule(FP_var['high'] & N_var['high'] & I_var['low'], PS_var['negative'])
# NOVA Regra 7: Se FP é alta e FN é baixa e I é baixa e N é baixa → SENTIMENTO POSITIVE
rule7 = ctrl.Rule(FP_var['high'] & FN_var['low'] & I_var['low'] & N_var['low'], PS_var['positive'])

# Criação do sistema de controle fuzzy com as regras definidas
sentiment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])

# ============================================
# Função de Análise Fuzzy (usando scikit-fuzzy)
# ============================================
def fuzzy_sentiment_scikit(text):
    """
    Realiza a análise de sentimentos de um texto utilizando o sistema fuzzy.
    Calcula as frequências FP, FN, I e N, cria uma nova instância do simulador,
    realiza a inferência fuzzy e classifica o sentimento.
    
    Se nenhuma regra for acionada, assume um valor padrão de 0.5 (neutral).
    """
    FP_val, FN_val, I_val, N_val = calculate_frequencies(text)
    simulation = ctrl.ControlSystemSimulation(sentiment_ctrl)
    simulation.input['FP'] = FP_val
    simulation.input['FN'] = FN_val
    simulation.input['I'] = I_val
    simulation.input['N'] = N_val
    
    simulation.compute()
    try:
        score = simulation.output['PS']
    except KeyError:
        score = 0.5  # Valor padrão se nenhum resultado for definido
    
    if score < 0.35:
        sentiment = 'NEGATIVE'
    elif score < 0.65:
        sentiment = 'NEUTRAL'
    else:
        sentiment = 'POSITIVE'
    
    print("Texto analisado: ", text)
    print("Frequência de palavras positivas (FP): {:.2f}".format(FP_val))
    print("Frequência de palavras negativas (FN): {:.2f}".format(FN_val))
    print("Frequência de intensificadores (I): {:.2f}".format(I_val))
    print("Frequência de negações (N): {:.2f}".format(N_val))
    print("Score fuzzy (PS): {:.2f}".format(score))
    print("Classificação do sentimento: {}\n".format(sentiment))
    
    return sentiment

# ============================================
# Demonstração com Exemplos
# ============================================
if __name__ == '__main__':
    # Exemplo 1: Comentário positivo sem inversão de sentido
    texto1 = "O livro é incrível e maravilhoso"
    fuzzy_sentiment_scikit(texto1)
    
    # Exemplo 2: Comentário com inversão (esperado: NEGATIVE)
    texto2 = "Não gostei deste filme"
    fuzzy_sentiment_scikit(texto2)
    
    # Exemplo 3: Frase neutra
    texto3 = "Nada de bom aconteceu"
    fuzzy_sentiment_scikit(texto3)

    texto4= "Completamente feliz com o resultado"
    fuzzy_sentiment_scikit(texto4)

    texto5 = "O atendimento foi péssimo e frustrante"
    fuzzy_sentiment_scikit(texto5)

    texto6 = "Nem gostei, nem me apaixonei pelo livro"
    fuzzy_sentiment_scikit(texto6)

    texto7 = "Esse restaurante é fantástico e o atendimento é excelente"
    fuzzy_sentiment_scikit(texto7)
    

