import re

# Bancos de palavras (ajuste conforme necessário)
positive_words = ["ótimo", "excelente", "incrível", "fantástico", "maravilhoso", "feliz", "surpreendente", "bonito", "gostei"]
negative_words = ["péssimo", "horrível", "terrível", "desagradável", "decepcionante", "triste", "frustrante"]

intensifiers = ["muito", "bastante", "extremamente", "incrivelmente", "realmente", "completamente"]
negations = ["não", "jamais", "nenhum", "nem", "nada"]

# Função para pré-processar o texto
def process_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return words

# Nova estratégia de normalização: usar o total de palavras-chave encontradas
def calculate_frequencies(text):
    words = process_text(text)
    
    count_positive = sum(word in positive_words for word in words)
    count_negative = sum(word in negative_words for word in words)
    count_intensifier = sum(word in intensifiers for word in words)
    count_negation = sum(word in negations for word in words)
    
    total_keywords = count_positive + count_negative + count_intensifier + count_negation
    if total_keywords == 0:
        return 0, 0, 0, 0
    
    FP = count_positive / total_keywords
    FN = count_negative / total_keywords
    I = count_intensifier / total_keywords
    N = count_negation / total_keywords
    
    return FP, FN, I, N

# Funções para conjuntos “shoulder” e triangulares

def left_shoulder(x, b, c):
    """Função de pertinência para conjunto do tipo left shoulder (inicia em 0)."""
    if x <= b:
        return 1.0
    elif x < c:
        return (c - x) / (c - b)
    else:
        return 0.0

def right_shoulder(x, a, b):
    """Função de pertinência para conjunto do tipo right shoulder (termina em 1)."""
    if x >= b:
        return 1.0
    elif x > a:
        return (x - a) / (b - a)
    else:
        return 0.0

def triangle(x, a, b, c):
    """Função triangular padrão (para o conjunto intermediário)."""
    if x < a or x > c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 1.0
    else:
        return (c - x) / (c - b) if (c - b) != 0 else 1.0

# Função para obter os graus de pertinência para uma variável.
# Os intervalos abaixo foram escolhidos de forma a refletir melhor os valores obtidos:
#
# Para FP, FN, I e N:
#   - Baixa (B): left shoulder de 0 a (b=0.05) e diminui até 0 em c=0.2.
#   - Média (M): função triangular com intervalo [0.1, 0.25, 0.4].
#   - Alta (A): right shoulder iniciando em a=0.3, totalmente 1 a partir de b=0.5.
def get_memberships(value):
    memberships = {
        'B': left_shoulder(value, b=0.05, c=0.2),
        'M': triangle(value, a=0.1, b=0.25, c=0.4),
        'A': right_shoulder(value, a=0.3, b=0.5)
    }
    return memberships

# Nova definição das regras fuzzy para tratar negações corretamente
def fuzzy_inference(FP, FN, I, N):
    fp_mem = get_memberships(FP)
    fn_mem = get_memberships(FN)
    i_mem = get_memberships(I)
    n_mem = get_memberships(N)
    
    # Função para calcular o mínimo (grau de ativação) de uma regra:
    def rule_activation(*conditions):
        return min(conditions)
    
    rules = []
    
    # Regra 1: Se FP é alta e N é baixa (ausência de negação) → SENTIMENTO POSITIVO
    activation_r1 = rule_activation(fp_mem['A'], left_shoulder(N, b=0.05, c=0.2))
    rules.append((activation_r1, 0.8))
    
    # Regra 2: Se FP é alta e N é alta (negação presente) → SENTIMENTO NEGATIVO
    activation_r2 = rule_activation(fp_mem['A'], right_shoulder(N, a=0.3, b=0.5))
    rules.append((activation_r2, 0.2))
    
    # Regra 3: Se FN é alta e N é baixa → SENTIMENTO NEGATIVO
    activation_r3 = rule_activation(fn_mem['A'], left_shoulder(N, b=0.05, c=0.2))
    rules.append((activation_r3, 0.2))
    
    # Regra 4: Se FN é alta e N é alta → SENTIMENTO POSITIVO
    activation_r4 = rule_activation(fn_mem['A'], right_shoulder(N, a=0.3, b=0.5))
    rules.append((activation_r4, 0.8))
    
    # Regra 5: Se FP e FN estão na faixa média (independente de intensificadores ou negações) → SENTIMENTO NEUTRO
    activation_r5 = rule_activation(get_memberships(FP)['M'], get_memberships(FN)['M'])
    rules.append((activation_r5, 0.5))
    
    numerator = sum(act * out for act, out in rules)
    denominator = sum(act for act, _ in rules)
    
    if denominator == 0:
        final_score = 0.5
    else:
        final_score = numerator / denominator
    
    return final_score, rules

def classify_sentiment(score):
    if score < 0.35:
        return "NEGATIVO"
    elif score < 0.65:
        return "NEUTRO"
    else:
        return "POSITIVO"

def fuzzy_sentiment_analysis(text):
    FP, FN, I, N = calculate_frequencies(text)
    score, applied_rules = fuzzy_inference(FP, FN, I, N)
    sentiment = classify_sentiment(score)
    
    print("Texto analisado: ", text)
    print("Frequência de palavras positivas (FP): {:.2f}".format(FP))
    print("Frequência de palavras negativas (FN): {:.2f}".format(FN))
    print("Frequência de intensificadores (I): {:.2f}".format(I))
    print("Frequência de negações (N): {:.2f}".format(N))
    print("\nRegras Fuzzy aplicadas:")
    for idx, (activation, output) in enumerate(applied_rules, start=1):
        print("  Regra {}: grau de ativação = {:.2f}, saída = {:.2f}".format(idx, activation, output))
    print("\nScore final fuzzy: {:.2f}".format(score))
    print("Classificação do sentimento: {}\n".format(sentiment))
    return sentiment

# Demonstração com exemplos:
if __name__ == "__main__":
    # Comentário positivo sem negação:
    texto1 = "Este gato é muito bonito"
    fuzzy_sentiment_analysis(texto1)
    
    # Comentário com negação: "Não gostei deste filme"
    texto2 = "O dia está passando normalmente"
    fuzzy_sentiment_analysis(texto2)

    texto3 = "Esse produto é incrível e maravilhoso"
    fuzzy_sentiment_analysis(texto3)