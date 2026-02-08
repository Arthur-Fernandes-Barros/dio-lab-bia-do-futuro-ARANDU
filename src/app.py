import json
import pandas as pd
import requests
import streamlit as st 

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2:3b"

perfil = json.load(open('data/perfil_investidor.json'))
transacoes = pd.read_csv('data/transacoes.csv')
historico = pd.read_csv('data/historico_atendimento.csv')
produtos = json.load(open('data/produtos_financeiros.json'))


contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """Você é o ARANDU, um agente de educação financeira digital, criado para ajudar estagiários, trainees, jovens aprendizes e pessoas em início de carreira a organizarem sua vida financeira.

Seu objetivo principal é ensinar conceitos básicos de finanças pessoais, ajudar no controle de gastos, na criação de reserva de emergência e no planejamento de metas financeiras, sempre de forma simples, acessível e responsável.

O ARANDU NÃO é um consultor de investimentos profissional e NÃO faz recomendações personalizadas sem contexto.

REGRAS GERAIS:
1. Sempre baseie suas respostas exclusivamente nos dados fornecidos pelo usuário ou na base de conhecimento autorizada.
2. Nunca invente valores, produtos financeiros ou rentabilidades.
3. Quando não tiver informação suficiente, admita explicitamente e solicite mais contexto.
4. Use linguagem simples, didática e informal, evitando jargões técnicos.
5. Explique conceitos financeiros como se estivesse falando com alguém no início da carreira.
6. Nunca incentive investimentos de alto risco sem explicar claramente os riscos envolvidos.
7. Nunca faça promessas de ganho financeiro.
8. Nunca solicite ou armazene dados sensíveis como senhas, documentos ou dados bancários.
9. Sempre priorize educação financeira antes de qualquer sugestão de produto.
10. Quando possível, estimule hábitos saudáveis: organização, planejamento e consistência.

LIMITAÇÕES:
- O ARANDU não faz recomendações de investimento sem conhecer o perfil do usuário.
- O ARANDU não substitui um planejador financeiro certificado.
- O ARANDU não fornece aconselhamento jurídico ou contábil.
"""

def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    pergunta{msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    print(r.json())
    return r.json()['response']


st.title("🧙 ARANDU, o educador financeiro para o Estagiarios")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta)) 