# 1. Importações necessárias
import requests
import fitz  # PyMuPDF
from openai import OpenAI

def handler(pd: "pipedream"):
    # --- ETAPA 1: PEGAR DADOS DO FORMULÁRIO E DOS ARQUIVOS ---
    trigger_event = pd.steps["trigger"]["event"]
    body = trigger_event.get("body", {})
    
    # Pegando os dados de texto
    duracao_texto = body.get("duracao", "0")
    dataInicio = body.get("dataInicio", "Não informado")
    nomeObra = body.get("nomeObra", "Não informado")
    topografia = body.get("topografia", "Não informado")
    infraestrutura = body.get("infraestrutura", "Não informado")
    print(topografia, infraestrutura)
    
    info_orcamento = body.get("orcamento")
    url_orcamento = info_orcamento.get("url")
    info_fisico = body.get("fisico")
    if info_fisico == "undefined" or not info_fisico:
        url_fisico = "Nenhum documento encontrado"
        texto_fisico = "Nenhum documento encontrado"
    else:
        # Only try to get the URL if info_fisico is a dictionary
        if isinstance(info_fisico, dict):
            url_fisico = info_fisico.get("url")
            response_fisico = requests.get(url_fisico)
            if response_fisico.ok:
                with fitz.open(stream=response_fisico.content, filetype="pdf") as doc:
                    texto_fisico = "".join(pagina.get_text() for pagina in doc)
        else:
            url_fisico = "Nenhum documento encontrado"
            texto_fisico = "Nenhum documento encontrado"
    
    print("Urls:", url_fisico, url_orcamento)

    

    # Verificação de segurança para o arquivo obrigatório
    if not url_orcamento:
        return pd.respond({
            "status": 400,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": {"success": False, "mensagem": "O arquivo da Planilha de Orçamento é obrigatório."}
        })

    # --- ETAPA 2: LER O CONTEÚDO DOS PDFS ---
    response_orcamento = requests.get(url_orcamento)
    response_orcamento.raise_for_status()
    with fitz.open(stream=response_orcamento.content, filetype="pdf") as doc:
        texto_orcamento = "".join(pagina.get_text() for pagina in doc)

    print("textos:",texto_fisico, texto_orcamento)
    
    
    
    # --- ETAPA 3: RESUMIR DOCUMENTOS COM A IA ---
    # CORREÇÃO 3: Lembre-se de usar o método seguro de contas conectadas no futuro!
    # client = OpenAI(api_key=pd.inputs["openai"]["$auth"]["api_key"])
    client = OpenAI(api_key="")

    

    # --- ETAPA 4: GERAR O CRONOGRAMA FINAL ---
    print("Montando o prompt final e gerando o cronograma JSON...")
    # CORREÇÃO 5: Usando F-String para inserir as variáveis no prompt principal
    prompt_main = f"""

    [CONTEXTO E PERSONA]

    Você é um assistente de IA especialista em engenharia civil e planejamento de obras, com foco em criar dados estruturados para software de gerenciamento de projetos.

    [TAREFA PRINCIPAL]
    Sua tarefa é analisar as informações de uma obra fornecidas abaixo e gerar um cronograma em formato de um array JSON, que será usado para alimentar um gráfico de Gantt interativo. Você deve calcular as datas de início e término de cada atividade com base nas durações, na data de início geral e nas dependências lógicas entre as tarefas.
    
    [DADOS DE ENTRADA]
      - Nome da Obra: {nomeObra}
      - Data de Início Geral: {dataInicio}
      - Duração de Referência: {duracao_texto} dias
      - Topografia do Terreno: {topografia}
      - Infraestrutura Existente no Local (lista do que o usuário marcou que JÁ TEM): {infraestrutura}
      - Dados da Planilha de Orçamento (fonte primária de atividades):
      {texto_orcamento}
      - Dados do Cronograma Físico (fonte secundária, opcional):
      {texto_fisico}
    [INTERPRETAÇÃO DE DADOS ESPECÍFICOS]
        Antes de gerar o cronograma, você DEVE aplicar as seguintes regras de engenharia:
        1.  **Regra de Topografia:**
            - Se a `Topografia do Terreno` for 'plano', você deve assumir que não são necessárias grandes atividades de terraplanagem no início do cronograma.
            - Se a `Topografia do Terreno` for 'aclive', 'declive', ou 'irregular', você DEVE incluir uma fase inicial de "Terraplanagem" no cronograma, com atividades como "Corte Mecanizado", "Aterro e Compactação", etc. A duração e a necessidade dessas tarefas devem ser inferidas a partir da planilha de orçamento, se presentes, ou estimadas com bom senso.
        
        2.  **Regra de Infraestrutura:**
            - A lista completa de infraestruturas básicas possíveis é: ['agua', 'esgoto', 'energia', 'pavimentacao'].
            - A entrada `Infraestrutura Existente` mostra o que JÁ EXISTE no local.
            - Para cada item da lista completa que **NÃO ESTIVER** presente na lista de `Infraestrutura Existente`, você **DEVE** adicionar uma tarefa correspondente na fase de "Serviços Preliminares" do cronograma.
            - **Exemplo 1:** Se `Infraestrutura Existente` for `['agua', 'esgoto']`, o cronograma deve incluir tarefas para "Executar ligação de energia elétrica" e "Preparar acesso / Pavimentação".
            - **Exemplo 2:** Se `Infraestrutura Existente` for `['agua', 'esgoto', 'energia', 'pavimentacao']`, nenhuma dessas tarefas de infraestrutura precisa ser adicionada.

    [REGRAS E ESPECIFICAÇÕES DE SAÍDA]
    1.  **FORMATO OBRIGATÓRIO:** Sua única saída deve ser um array JSON válido. Não inclua o JSON dentro de blocos de código markdown (como ```json ... ```). Não adicione NENHUM texto, explicação, introdução ou observação antes ou depois do array JSON.
    
    2.  **ESTRUTURA DOS OBJETOS:** Cada objeto dentro do array representa uma tarefa e deve conter EXATAMENTE as seguintes chaves:
        - `id`: Uma string única para a tarefa (ex: "task1", "task2", "atividade_limpeza").
        - `name`: O nome da atividade (ex: "Limpeza inicial do terreno").
        - `start`: A data de início calculada da tarefa no formato "AAAA-MM-DD".
        - `end`: A data de término calculada da tarefa no formato "AAAA-MM-DD".
        - `progress`: O progresso da tarefa em porcentagem. Use o valor 0 como padrão para todas.
        - `dependencies`: O 'id' da tarefa da qual esta depende. Se for a primeira tarefa, use uma string vazia (""). Se uma tarefa depende de múltiplas outras, separe os IDs por vírgula (ex: "task1,task2").

    [EXEMPLO DE SAÍDA ESPERADA]

    Se a entrada fosse simples, a saída deveria se parecer com isto:
    [
      {{
        "id": "task1",
        "name": "Serviços Preliminares",
        "start": "2025-01-10",
        "end": "2025-01-20",
        "progress": 0,
        "dependencies": ""

      }},
      {{
        "id": "task2",
        "name": "Fundação",
        "start": "2025-01-21",
        "end": "2025-02-15",
        "progress": 0,
        "dependencies": "task1"

      }}

    ]

    """ 

  
    
    response_ia_final = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{prompt_main} "},
            {"role": "user", "content": f"Faça o que o system pede."}
         ]
    )
    resultado_json_str = response_ia_final.choices[0].message.content

    # --- ETAPA 5: ENVIAR RESPOSTA FINAL ---
    return pd.respond({
        "status": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": {
            "success": True,
            "mensagem": "Cronograma JSON gerado com sucesso!",
            "cronograma": resultado_json_str
        }
    })