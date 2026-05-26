"""
Gerador de documentação ABNT para o sistema Tech Wear.
Execução: python gerar_documentacao.py
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime


# ─────────────────────────────────────────────────────────
# Utilitários
# ─────────────────────────────────────────────────────────

def set_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def heading(doc, text, level=1, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size=font_size, bold=bold)
    return p


def body(doc, text, indent_cm=0, space_after=6, justify=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(1.25)  # recuo ABNT
    if indent_cm:
        p.paragraph_format.left_indent = Cm(indent_cm)
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    set_font(run)
    return p


def bullet(doc, text, indent_cm=1.25):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(indent_cm)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    set_font(run)
    return p


def code_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(4)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    set_font(run, name="Courier New", size=10)
    return p


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    # Cabeçalho
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        set_font(run, bold=True, size=10)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Dados
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            set_font(run, size=10)
    if col_widths:
        for i, width in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(width)
    return table


def add_page_number(doc):
    """Adiciona número de página centralizado no rodapé."""
    section = doc.sections[0]
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


# ─────────────────────────────────────────────────────────
# Documento
# ─────────────────────────────────────────────────────────

def build_document():
    doc = Document()

    # Margens ABNT: superior 3 cm, inferior 2 cm, esquerda 3 cm, direita 2 cm
    section = doc.sections[0]
    section.top_margin = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2)

    add_page_number(doc)

    # ──────────────────────────────────────────
    # CAPA
    # ──────────────────────────────────────────
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("UNIVERSIDADE SÃO JUDAS TADEU")
    set_font(run, bold=True, size=14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Curso de Engenharia de Software / Ciência da Computação")
    set_font(run, size=12)

    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("TECH WEAR")
    set_font(run, bold=True, size=18)

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        "Documentação Técnica do Sistema de E-commerce de Roupas Esportivas\n"
        "com Busca Visual Inteligente (WearIA)"
    )
    set_font(run, size=14)

    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        "Projeto A3 — Disciplina: Análise e Projeto de Sistemas"
    )
    set_font(run, size=12)

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("São Paulo\n" + str(datetime.date.today().year))
    set_font(run, size=12)

    doc.add_page_break()

    # ──────────────────────────────────────────
    # RESUMO
    # ──────────────────────────────────────────
    heading(doc, "RESUMO", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    body(doc,
        "Este documento apresenta a documentação técnica completa do sistema Tech Wear, "
        "uma plataforma de e-commerce especializada em vestuário esportivo. O sistema integra "
        "um frontend web responsivo desenvolvido com HTML, CSS e JavaScript puro a um backend "
        "de inteligência artificial baseado em Python e FastAPI. O módulo de busca visual "
        "denominado WearIA utiliza as tecnologias YOLO (You Only Look Once) para detecção de "
        "peças de roupa em imagens, CLIP (Contrastive Language–Image Pre-Training) da OpenAI "
        "para geração de embeddings multimodais e algoritmo KMeans para extração de cor dominante, "
        "permitindo ao usuário encontrar produtos similares a partir de uma fotografia. "
        "São descritos os requisitos funcionais e não funcionais, a arquitetura do sistema, "
        "os módulos de software, as interfaces de usuário e as tecnologias empregadas."
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run("Palavras-chave: ")
    set_font(run, bold=True)
    run2 = p.add_run(
        "e-commerce; vestuário esportivo; busca visual; inteligência artificial; YOLO; CLIP; FastAPI; JavaScript."
    )
    set_font(run2)

    doc.add_page_break()

    # ──────────────────────────────────────────
    # SUMÁRIO
    # ──────────────────────────────────────────
    heading(doc, "SUMÁRIO", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    sumario = [
        ("1", "INTRODUÇÃO", "4"),
        ("1.1", "Objetivo do Sistema", "4"),
        ("1.2", "Escopo", "4"),
        ("2", "VISÃO GERAL DA ARQUITETURA", "5"),
        ("2.1", "Camada Frontend", "5"),
        ("2.2", "Camada Backend (IA)", "5"),
        ("2.3", "Comunicação entre Camadas", "6"),
        ("3", "MÓDULOS DO FRONTEND", "6"),
        ("3.1", "Página Inicial (index.html)", "6"),
        ("3.2", "Coleção de Produtos (markets.html)", "7"),
        ("3.3", "Carrinho de Compras (wallet.html)", "7"),
        ("3.4", "Processo de Compra", "7"),
        ("3.5", "Autenticação (login.html)", "8"),
        ("3.6", "Painel Administrativo (admin.html)", "8"),
        ("3.7", "Configurações do Usuário (settings.html)", "9"),
        ("3.8", "Dashboard (dashboard.html)", "9"),
        ("4", "MÓDULO WEARIA — BUSCA VISUAL INTELIGENTE", "10"),
        ("4.1", "Visão Geral do Fluxo", "10"),
        ("4.2", "Detecção de Roupa com YOLO", "10"),
        ("4.3", "Extração de Cor com KMeans", "11"),
        ("4.4", "Embeddings Visuais com CLIP", "11"),
        ("4.5", "Ranking Híbrido", "12"),
        ("5", "API REST (BACKEND FASTAPI)", "12"),
        ("5.1", "Endpoints", "12"),
        ("5.2", "Modelos de Dados (Pydantic)", "13"),
        ("6", "ESTRUTURA DE DADOS (FRONTEND)", "13"),
        ("6.1", "LocalStorage", "13"),
        ("6.2", "Modelo de Produto", "14"),
        ("7", "TECNOLOGIAS UTILIZADAS", "14"),
        ("7.1", "Frontend", "14"),
        ("7.2", "Backend", "15"),
        ("8", "REQUISITOS DO SISTEMA", "15"),
        ("8.1", "Requisitos Funcionais", "15"),
        ("8.2", "Requisitos Não Funcionais", "16"),
        ("9", "CONSIDERAÇÕES FINAIS", "16"),
        ("", "REFERÊNCIAS", "17"),
    ]

    for num, titulo, pag in sumario:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.first_line_indent = Cm(0)
        if num:
            run = p.add_run(f"{num}  {titulo}")
        else:
            run = p.add_run(titulo)
        set_font(run, size=12, bold=(len(num) <= 1))

    doc.add_page_break()

    # ──────────────────────────────────────────
    # 1. INTRODUÇÃO
    # ──────────────────────────────────────────
    heading(doc, "1  INTRODUÇÃO", font_size=12, bold=True)

    body(doc,
        "O crescimento exponencial do comércio eletrônico no Brasil exige que plataformas de "
        "e-commerce ofereçam experiências de compra cada vez mais intuitivas e personalizadas. "
        "O projeto Tech Wear surge nesse contexto como uma solução completa de loja virtual "
        "de roupas esportivas, diferenciando-se pela integração de um módulo de inteligência "
        "artificial denominado WearIA, que permite ao usuário encontrar produtos por similaridade "
        "visual a partir de uma fotografia."
    )

    heading(doc, "1.1  Objetivo do Sistema", font_size=12, bold=True, space_before=6)
    body(doc,
        "Desenvolver e documentar uma plataforma de e-commerce de vestuário esportivo que reúna "
        "as funcionalidades essenciais de uma loja virtual — catálogo, carrinho, pagamento, "
        "gestão de pedidos e perfil de usuário — acrescidas de busca visual inteligente por "
        "imagem, tornando a experiência de descoberta de produtos mais natural e eficiente."
    )

    heading(doc, "1.2  Escopo", font_size=12, bold=True, space_before=6)
    body(doc,
        "O sistema abrange os seguintes componentes: (a) frontend web responsivo acessível por "
        "navegador, sem dependência de frameworks JavaScript externos; (b) API REST em Python "
        "para processamento de imagens com modelos de aprendizado profundo; (c) persistência "
        "local via localStorage no navegador para dados de sessão, produtos e pedidos. "
        "O sistema não inclui banco de dados relacional ou servidor de autenticação externo "
        "nesta versão, sendo adequado para ambiente acadêmico de demonstração."
    )

    doc.add_page_break()

    # ──────────────────────────────────────────
    # 2. ARQUITETURA
    # ──────────────────────────────────────────
    heading(doc, "2  VISÃO GERAL DA ARQUITETURA", font_size=12, bold=True)

    body(doc,
        "O Tech Wear adota uma arquitetura de duas camadas bem definidas: o frontend web "
        "(cliente) e o backend de inteligência artificial (servidor). Ambas se comunicam "
        "exclusivamente por HTTP/REST, garantindo baixo acoplamento e facilidade de evolução "
        "independente de cada camada."
    )

    heading(doc, "2.1  Camada Frontend", font_size=12, bold=True, space_before=6)
    body(doc,
        "O frontend é composto por páginas HTML5 estáticas estilizadas com CSS3 e animadas "
        "com JavaScript puro (ES5 compatível). Toda a lógica de negócio do cliente — "
        "gerenciamento de produtos, carrinho, usuários e pedidos — é encapsulada em uma "
        "API global exposta no objeto window.TechWear, implementada no arquivo js/produtos.js. "
        "A persistência de dados é realizada via localStorage do navegador."
    )

    body(doc,
        "As páginas que compõem o frontend são:"
    )

    paginas = [
        ("index.html", "Página inicial com banner hero, galeria de destaques e acesso rápido ao catálogo"),
        ("markets.html", "Catálogo completo com filtros por categoria, esporte, ordenação e busca textual"),
        ("wallet.html", "Carrinho de compras com resumo de itens, cálculo de totais e botão de checkout"),
        ("pagamento.html", "Seleção de método de pagamento e confirmação do pedido"),
        ("frete.html", "Cálculo de frete por CEP e seleção de modalidade de entrega"),
        ("nota-fiscal.html", "Exibição da nota fiscal eletrônica após a finalização da compra"),
        ("login.html", "Autenticação e registro de usuários"),
        ("admin.html", "Painel administrativo para cadastro, edição e remoção de produtos"),
        ("settings.html", "Perfil e configurações do usuário logado"),
        ("dashboard.html", "Visão gerencial com métricas e relatórios de vendas"),
        ("wearia.html", "Módulo de busca visual inteligente por imagem"),
    ]

    add_table(doc,
        ["Página", "Descrição"],
        paginas,
        col_widths=[4.5, 11.5]
    )

    doc.add_paragraph()

    heading(doc, "2.2  Camada Backend (IA)", font_size=12, bold=True, space_before=6)
    body(doc,
        "O backend é implementado com o framework FastAPI (Python 3.13) e expõe uma API REST "
        "consumida exclusivamente pelo módulo WearIA do frontend. Ao receber uma imagem, "
        "o pipeline de processamento executa três etapas sequenciais: detecção da peça de "
        "roupa com YOLOv8, extração da cor dominante com KMeans e geração de embedding visual "
        "com o modelo CLIP da OpenAI. O resultado final é uma lista ordenada por similaridade "
        "composta dos produtos mais relevantes do catálogo."
    )

    heading(doc, "2.3  Comunicação entre Camadas", font_size=12, bold=True, space_before=6)
    body(doc,
        "A comunicação é feita via HTTP com codificação JSON. O frontend envia requisições "
        "para http://localhost:8000/api, endereço padrão do servidor FastAPI. O middleware "
        "CORS está configurado para aceitar qualquer origem, permitindo o acesso a partir "
        "do servidor de desenvolvimento local. Em produção, recomenda-se restringir as "
        "origens permitidas ao domínio da aplicação."
    )

    doc.add_page_break()

    # ──────────────────────────────────────────
    # 3. MÓDULOS DO FRONTEND
    # ──────────────────────────────────────────
    heading(doc, "3  MÓDULOS DO FRONTEND", font_size=12, bold=True)

    heading(doc, "3.1  Página Inicial (index.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "A página inicial é o ponto de entrada do sistema após o login. Apresenta um banner "
        "hero com chamada para ação, uma galeria de produtos em destaque renderizada "
        "dinamicamente a partir do catálogo armazenado no localStorage e atalhos de "
        "navegação para as principais seções da loja. A sidebar exibe o menu principal "
        "com ícones do Material Symbols Outlined."
    )

    heading(doc, "3.2  Coleção de Produtos (markets.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Exibe o catálogo completo de produtos com suporte a filtros combinados: categoria "
        "(camisetas, calças, jaquetas, moletons, shorts), modalidade esportiva (corrida, "
        "basquete, academia), ordenação (menor preço, maior preço, nome A–Z) e busca "
        "textual em tempo real. Cada produto é exibido em um card com imagem, nome, "
        "preço e botão de adição ao carrinho com seleção de tamanho."
    )

    heading(doc, "3.3  Carrinho de Compras (wallet.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Apresenta os itens adicionados ao carrinho com controles de quantidade, opção de "
        "remoção e cálculo automático de subtotal, frete e total. O fluxo de checkout "
        "encaminha o usuário para a página de frete, seguida da de pagamento."
    )

    heading(doc, "3.4  Processo de Compra", font_size=12, bold=True, space_before=6)
    body(doc,
        "O processo de compra é dividido em três etapas distintas, representadas por "
        "páginas separadas:"
    )

    bullet(doc, "frete.html — consulta de CEP via API ViaCEP e seleção de modalidade de entrega (PAC, SEDEX, Expresso);")
    bullet(doc, "pagamento.html — seleção de método de pagamento (cartão de crédito, PIX, boleto) com simulação de processamento;")
    bullet(doc, "nota-fiscal.html — exibição da nota fiscal eletrônica gerada automaticamente com os dados do pedido.")

    doc.add_paragraph()

    heading(doc, "3.5  Autenticação (login.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Oferece duas funcionalidades: login de usuários já cadastrados e registro de "
        "novos usuários. Os dados são armazenados no localStorage com a chave tw_usuarios. "
        "A senha é armazenada em texto puro nesta versão de demonstração; em produção "
        "deve ser substituída por hash seguro (ex.: bcrypt). A sessão ativa é controlada "
        "pela chave tw_sessao."
    )

    heading(doc, "3.6  Painel Administrativo (admin.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Restrito a usuários com perfil de administrador, permite o gerenciamento completo "
        "do catálogo de produtos. Funcionalidades disponíveis:"
    )
    bullet(doc, "Cadastro de novo produto com nome, descrição, preço, categoria, tamanhos disponíveis, esporte, cor (com color picker HEX) e imagem (upload com conversão para Base64);")
    bullet(doc, "Edição de produto existente em modal;")
    bullet(doc, "Remoção de produto com confirmação;")
    bullet(doc, "Sincronização do catálogo com o backend WearIA (endpoint /api/index-products).")

    doc.add_paragraph()

    heading(doc, "3.7  Configurações do Usuário (settings.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Permite ao usuário logado atualizar seus dados cadastrais (nome, e-mail, telefone, "
        "endereço) e alterar a senha. As informações são salvas no localStorage com a "
        "chave tw_perfil. A página também exibe o histórico de pedidos realizados."
    )

    heading(doc, "3.8  Dashboard (dashboard.html)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Painel gerencial com visão consolidada do negócio, incluindo indicadores de "
        "desempenho (total de pedidos, receita, produtos cadastrados e usuários ativos), "
        "gráfico de vendas por período e listagem dos pedidos mais recentes. Os dados "
        "são calculados em tempo real a partir do localStorage."
    )

    doc.add_page_break()

    # ──────────────────────────────────────────
    # 4. WEARIA
    # ──────────────────────────────────────────
    heading(doc, "4  MÓDULO WEARIA — BUSCA VISUAL INTELIGENTE", font_size=12, bold=True)

    body(doc,
        "O WearIA é o principal diferencial do Tech Wear. Permite ao usuário fotografar "
        "qualquer peça de roupa — seja do próprio guarda-roupa, de uma vitrine ou da "
        "internet — e receber recomendações dos produtos mais similares do catálogo, "
        "levando em conta tanto a aparência visual quanto a cor da peça."
    )

    heading(doc, "4.1  Visão Geral do Fluxo", font_size=12, bold=True, space_before=6)
    body(doc,
        "O processamento de uma busca visual segue o pipeline descrito a seguir:"
    )

    fluxo = [
        ("1", "Upload", "Usuário seleciona ou arrasta uma imagem no frontend (wearia.html)"),
        ("2", "Envio", "js/wearia.js envia a imagem via POST multipart para /api/search-by-image"),
        ("3", "Detecção (YOLO)", "YOLOv8 detecta a peça principal; se for pessoa, recorta o torso"),
        ("4", "Cor (KMeans)", "KMeans extrai a cor dominante do recorte em HEX"),
        ("5", "Embedding (CLIP)", "CLIP gera um vetor de 512 dimensões para o recorte"),
        ("6", "Ranking", "Similaridade cosseno (CLIP) + distância Euclidiana (cor) → score híbrido"),
        ("7", "Resposta", "Backend retorna JSON com cor detectada, categoria e lista de produtos"),
        ("8", "Exibição", "Frontend renderiza os resultados com filtros de esporte e categoria"),
    ]

    add_table(doc,
        ["Etapa", "Nome", "Descrição"],
        fluxo,
        col_widths=[1.5, 3.5, 11]
    )

    doc.add_paragraph()

    heading(doc, "4.2  Detecção de Roupa com YOLO", font_size=12, bold=True, space_before=6)
    body(doc,
        "O serviço YoloService (backend/services/yolo_service.py) carrega o modelo "
        "YOLOv8n (nano) pré-treinado no dataset COCO. Como o COCO não possui classes "
        "específicas para peças de roupa, a estratégia adotada é detectar a pessoa "
        "presente na imagem e extrair a região do torso (15% a 65% da altura do bounding box), "
        "que corresponde à área onde a roupa é mais visível. Caso nenhuma detecção com "
        "confiança superior a 0,3 seja encontrada, o serviço realiza um recorte central "
        "da imagem como estratégia de fallback, assumindo que a roupa ocupa o centro do "
        "enquadramento."
    )

    heading(doc, "4.3  Extração de Cor com KMeans", font_size=12, bold=True, space_before=6)
    body(doc,
        "O serviço color_service (backend/services/color_service.py) recebe o recorte "
        "gerado pelo YOLO e aplica o algoritmo KMeans com k=3 clusters sobre os pixels "
        "da imagem redimensionada para 100×100 pixels. O cluster com maior número de "
        "pixels é selecionado como a cor dominante, cujas componentes RGB são convertidas "
        "para o formato hexadecimal (ex.: #c0392b para vermelho). A similaridade entre "
        "duas cores é calculada pela distância Euclidiana no espaço RGB normalizado."
    )

    heading(doc, "4.4  Embeddings Visuais com CLIP", font_size=12, bold=True, space_before=6)
    body(doc,
        "O serviço ClipService (backend/services/clip_service.py) utiliza o modelo "
        "openai/clip-vit-base-patch32 carregado via biblioteca transformers da Hugging Face. "
        "CLIP é um modelo de aprendizado contrastivo treinado em 400 milhões de pares "
        "imagem-texto, capaz de gerar representações vetoriais (embeddings) de 512 "
        "dimensões que capturam o conteúdo semântico da imagem em um espaço compartilhado "
        "com texto. Os embeddings são normalizados (norma L2 = 1) para que a similaridade "
        "cosseno possa ser calculada diretamente pelo produto escalar."
    )
    body(doc,
        "Para produtos sem imagem, o serviço encode_text gera o embedding a partir do "
        "texto descritivo do produto (nome + categoria), aproveitando o espaço vetorial "
        "unificado do CLIP."
    )

    heading(doc, "4.5  Ranking Híbrido", font_size=12, bold=True, space_before=6)
    body(doc,
        "O serviço recommendation_service combina os dois sinais em um score único:"
    )

    body(doc,
        "score = 0,7 × similaridade_clip + 0,3 × similaridade_cor"
    )

    body(doc,
        "A similaridade CLIP é o produto escalar entre o embedding da imagem de consulta e "
        "o embedding de cada produto (valor entre 0 e 1). A similaridade de cor é calculada "
        "como 1 − distância_normalizada, onde a distância é a Euclidiana no espaço RGB "
        "normalizada pelo valor máximo possível (√(255²×3) ≈ 441,67). O peso de 70% para "
        "CLIP e 30% para cor foi definido empiricamente, priorizando a similaridade "
        "de aparência geral sobre a cor específica. Resultados com score abaixo de 0,60 "
        "são filtrados e exibidos no estado de 'nenhum resultado encontrado'."
    )

    doc.add_page_break()

    # ──────────────────────────────────────────
    # 5. API REST
    # ──────────────────────────────────────────
    heading(doc, "5  API REST (BACKEND FASTAPI)", font_size=12, bold=True)

    body(doc,
        "O backend expõe dois endpoints REST sob o prefixo /api, servidos na porta 8000 "
        "pelo servidor ASGI Uvicorn. A documentação interativa é gerada automaticamente "
        "pelo FastAPI e acessível em http://localhost:8000/docs."
    )

    heading(doc, "5.1  Endpoints", font_size=12, bold=True, space_before=6)

    endpoints = [
        ("GET", "/", "Health check — retorna status online e nome do serviço"),
        ("POST", "/api/search-by-image", "Recebe imagem (multipart/form-data) e retorna produtos similares"),
        ("POST", "/api/index-products", "Recebe lista de produtos JSON e gera/atualiza embeddings no catálogo"),
    ]

    add_table(doc,
        ["Método", "Rota", "Descrição"],
        endpoints,
        col_widths=[2, 5, 9]
    )

    doc.add_paragraph()

    body(doc, "Exemplo de resposta do endpoint /api/search-by-image:")
    doc.add_paragraph()

    for line in [
        '{',
        '  "detected_hex": "#c0392b",',
        '  "detected_category": "camiseta",',
        '  "products": [',
        '    {',
        '      "id": 3,',
        '      "name": "Camiseta Running Pro",',
        '      "hex_color": "#c0392b",',
        '      "category": "camisetas",',
        '      "price": 89.90,',
        '      "image_url": "...",',
        '      "score": 0.87',
        '    }',
        '  ]',
        '}',
    ]:
        code_block(doc, line)

    heading(doc, "5.2  Modelos de Dados (Pydantic)", font_size=12, bold=True, space_before=6)
    body(doc,
        "Os modelos de dados da API são definidos com Pydantic (backend/models/product.py), "
        "garantindo validação automática de tipos e serialização JSON."
    )

    modelos = [
        ("ProductBase", "id, name, hex_color, category, price, image_url"),
        ("ProductWithEmbedding", "Herda ProductBase + embedding: List[float]"),
        ("SearchResult", "id, name, hex_color, category, price, image_url, score"),
        ("SearchResponse", "detected_hex, detected_category, products: List[SearchResult]"),
    ]

    add_table(doc,
        ["Modelo", "Campos"],
        modelos,
        col_widths=[5, 11]
    )

    doc.add_paragraph()
    doc.add_page_break()

    # ──────────────────────────────────────────
    # 6. ESTRUTURA DE DADOS
    # ──────────────────────────────────────────
    heading(doc, "6  ESTRUTURA DE DADOS (FRONTEND)", font_size=12, bold=True)

    heading(doc, "6.1  LocalStorage", font_size=12, bold=True, space_before=6)
    body(doc,
        "Toda a persistência de dados do frontend é realizada no localStorage do navegador. "
        "As chaves utilizadas e seus respectivos conteúdos são descritos a seguir:"
    )

    ls_keys = [
        ("tw_produtos", "Array de objetos Produto — catálogo completo da loja"),
        ("tw_carrinho", "Array de {produtoId, tamanho, quantidade} — itens no carrinho"),
        ("tw_usuarios", "Array de usuários cadastrados {id, nome, email, senha}"),
        ("tw_sessao", "Objeto do usuário logado {id, nome, email} ou null"),
        ("tw_pedidos", "Array de pedidos realizados com itens, total e data"),
        ("tw_perfil", "Dados de perfil complementares do usuário logado"),
        ("theme", "Tema da interface: 'dark' (padrão) ou 'light'"),
    ]

    add_table(doc,
        ["Chave", "Conteúdo"],
        ls_keys,
        col_widths=[4, 12]
    )

    doc.add_paragraph()

    heading(doc, "6.2  Modelo de Produto", font_size=12, bold=True, space_before=6)
    body(doc,
        "O objeto Produto armazenado no localStorage possui a seguinte estrutura:"
    )

    campos = [
        ("id", "number", "Identificador único numérico auto-incrementado"),
        ("nome", "string", "Nome comercial do produto"),
        ("descricao", "string", "Descrição detalhada"),
        ("preco", "number", "Preço em reais (float)"),
        ("categoria", "string", "Uma de: camisetas, calcas, jaquetas, moletons, shorts"),
        ("tamanhos", "string[]", "Array de tamanhos: P, M, G, GG"),
        ("cor", "string", "Nome da cor em português (ex.: 'vermelho')"),
        ("hex_color", "string", "Código HEX da cor (ex.: '#c0392b')"),
        ("imagem", "string", "Imagem em Base64 (data:image/...)"),
        ("estoque", "number", "Quantidade em estoque"),
        ("esporte", "string", "Modalidade: corrida, basquete, academia ou vazio"),
    ]

    add_table(doc,
        ["Campo", "Tipo", "Descrição"],
        campos,
        col_widths=[3.5, 3, 9.5]
    )

    doc.add_paragraph()
    doc.add_page_break()

    # ──────────────────────────────────────────
    # 7. TECNOLOGIAS
    # ──────────────────────────────────────────
    heading(doc, "7  TECNOLOGIAS UTILIZADAS", font_size=12, bold=True)

    heading(doc, "7.1  Frontend", font_size=12, bold=True, space_before=6)

    tec_front = [
        ("HTML5", "Marcação semântica das páginas"),
        ("CSS3", "Estilização com variáveis CSS, Flexbox e Grid Layout"),
        ("JavaScript ES5/ES6", "Lógica de negócio, DOM, fetch API e localStorage"),
        ("Google Fonts — Instrument Sans", "Tipografia padrão do sistema"),
        ("Material Symbols Outlined", "Ícones vetoriais do Google"),
        ("Firebase (firebase-config.js)", "Configuração para integração opcional com Firebase"),
        ("EmailJS (emailjs-template.html)", "Template para envio de e-mails transacionais"),
    ]

    add_table(doc,
        ["Tecnologia", "Uso"],
        tec_front,
        col_widths=[5.5, 10.5]
    )

    doc.add_paragraph()

    heading(doc, "7.2  Backend", font_size=12, bold=True, space_before=6)

    tec_back = [
        ("Python 3.13", "Linguagem principal do backend"),
        ("FastAPI 0.115", "Framework web assíncrono para criação da API REST"),
        ("Uvicorn 0.30", "Servidor ASGI de alta performance"),
        ("Pydantic", "Validação de dados e serialização (integrado ao FastAPI)"),
        ("Pillow 10.4", "Manipulação de imagens (abertura, recorte, redimensionamento)"),
        ("NumPy 1.26", "Operações matriciais e vetoriais"),
        ("scikit-learn 1.5", "Algoritmo KMeans para extração de cor dominante"),
        ("PyTorch 2.4", "Framework de deep learning (execução dos modelos CLIP e YOLO)"),
        ("Transformers 4.44 (Hugging Face)", "Carregamento do modelo CLIP openai/clip-vit-base-patch32"),
        ("Ultralytics 8.2 (YOLOv8)", "Detecção de objetos em imagens"),
    ]

    add_table(doc,
        ["Tecnologia / Versão", "Uso"],
        tec_back,
        col_widths=[6, 10]
    )

    doc.add_paragraph()
    doc.add_page_break()

    # ──────────────────────────────────────────
    # 8. REQUISITOS
    # ──────────────────────────────────────────
    heading(doc, "8  REQUISITOS DO SISTEMA", font_size=12, bold=True)

    heading(doc, "8.1  Requisitos Funcionais", font_size=12, bold=True, space_before=6)

    rfs = [
        ("RF01", "O sistema deve exibir o catálogo de produtos com filtros por categoria, esporte, ordenação e busca textual."),
        ("RF02", "O sistema deve permitir ao usuário adicionar produtos ao carrinho, alterando tamanho e quantidade."),
        ("RF03", "O sistema deve calcular o frete por CEP e permitir a seleção da modalidade de entrega."),
        ("RF04", "O sistema deve processar o pagamento por cartão de crédito, PIX ou boleto (simulado)."),
        ("RF05", "O sistema deve gerar nota fiscal eletrônica após a confirmação do pedido."),
        ("RF06", "O sistema deve permitir o cadastro e autenticação de usuários."),
        ("RF07", "O administrador deve poder cadastrar, editar e remover produtos do catálogo."),
        ("RF08", "O sistema deve permitir busca de produtos por imagem (WearIA)."),
        ("RF09", "O módulo WearIA deve detectar a peça de roupa na imagem enviada."),
        ("RF10", "O módulo WearIA deve retornar produtos ordenados por similaridade visual e de cor."),
        ("RF11", "O sistema deve suportar tema claro e escuro com persistência entre sessões."),
        ("RF12", "O dashboard deve exibir métricas de vendas e histórico de pedidos."),
    ]

    add_table(doc,
        ["ID", "Descrição"],
        rfs,
        col_widths=[1.5, 14.5]
    )

    doc.add_paragraph()

    heading(doc, "8.2  Requisitos Não Funcionais", font_size=12, bold=True, space_before=6)

    rnfs = [
        ("RNF01", "Desempenho", "A resposta do endpoint de busca visual deve ocorrer em menos de 5 segundos em hardware com GPU."),
        ("RNF02", "Responsividade", "O frontend deve ser utilizável em telas com largura mínima de 320px."),
        ("RNF03", "Compatibilidade", "O sistema deve funcionar nos navegadores Chrome, Firefox e Edge em suas versões atuais."),
        ("RNF04", "Manutenibilidade", "O código deve seguir separação de responsabilidades (frontend/backend independentes)."),
        ("RNF05", "Segurança", "Em produção, senhas devem ser armazenadas com hash e a API deve validar origens via CORS restrito."),
        ("RNF06", "Portabilidade", "O backend deve executar em qualquer sistema operacional com Python 3.10+."),
    ]

    add_table(doc,
        ["ID", "Categoria", "Descrição"],
        rnfs,
        col_widths=[1.5, 3.5, 11]
    )

    doc.add_paragraph()
    doc.add_page_break()

    # ──────────────────────────────────────────
    # 9. CONSIDERAÇÕES FINAIS
    # ──────────────────────────────────────────
    heading(doc, "9  CONSIDERAÇÕES FINAIS", font_size=12, bold=True)

    body(doc,
        "O sistema Tech Wear demonstra a viabilidade de integrar técnicas modernas de "
        "visão computacional e aprendizado profundo em uma plataforma de e-commerce "
        "desenvolvida com tecnologias web padrão. A arquitetura adotada separa "
        "claramente as responsabilidades: o frontend gerencia a experiência do usuário "
        "e a persistência local, enquanto o backend executa tarefas computacionalmente "
        "intensivas de processamento de imagens."
    )

    body(doc,
        "O módulo WearIA representa o diferencial técnico do projeto, combinando três "
        "técnicas complementares — detecção de objetos (YOLO), representação semântica "
        "(CLIP) e análise de cor (KMeans) — em um pipeline coeso de busca por similaridade. "
        "A arquitetura modular facilita a evolução do sistema, permitindo, por exemplo, "
        "substituir o modelo YOLO por um treinado especificamente em datasets de moda "
        "para aumentar a precisão da detecção."
    )

    body(doc,
        "Como trabalhos futuros, sugerem-se: (a) migração da persistência de dados do "
        "localStorage para um banco de dados relacional com autenticação JWT; "
        "(b) treinamento de um modelo YOLO customizado no dataset DeepFashion para "
        "melhorar a detecção de peças específicas; (c) implantação em infraestrutura "
        "em nuvem com balanceamento de carga para suportar múltiplos usuários simultâneos; "
        "(d) implementação de cache de embeddings para reduzir o tempo de resposta "
        "da busca visual."
    )

    doc.add_page_break()

    # ──────────────────────────────────────────
    # REFERÊNCIAS
    # ──────────────────────────────────────────
    heading(doc, "REFERÊNCIAS", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    referencias = [
        ("FASTAPI. FastAPI — Modern, Fast, Web Framework for Building APIs with Python. "
         "Disponível em: <https://fastapi.tiangolo.com>. Acesso em: mai. 2026."),
        ("HUGGING FACE. CLIP: Learning Transferable Visual Models From Natural Language Supervision. "
         "Disponível em: <https://huggingface.co/openai/clip-vit-base-patch32>. Acesso em: mai. 2026."),
        ("JOCHER, Glenn et al. Ultralytics YOLOv8. Versão 8.2. "
         "Disponível em: <https://github.com/ultralytics/ultralytics>. Acesso em: mai. 2026."),
        ("PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. "
         "Journal of Machine Learning Research, v. 12, p. 2825–2830, 2011."),
        ("PYDANTIC. Pydantic Documentation. "
         "Disponível em: <https://docs.pydantic.dev>. Acesso em: mai. 2026."),
        ("RADFORD, Alec et al. Learning Transferable Visual Models From Natural Language Supervision. "
         "In: International Conference on Machine Learning (ICML), 2021."),
        ("PYTORCH. PyTorch — An Open Source Machine Learning Framework. "
         "Disponível em: <https://pytorch.org>. Acesso em: mai. 2026."),
        ("ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 6023: Informação e documentação — "
         "Referências — Elaboração. Rio de Janeiro: ABNT, 2018."),
        ("ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 14724: Informação e documentação — "
         "Trabalhos acadêmicos — Apresentação. Rio de Janeiro: ABNT, 2011."),
    ]

    for ref in referencias:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Cm(0)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.hanging_indent = Cm(0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(ref)
        set_font(run)

    # ──────────────────────────────────────────
    # Salvar
    # ──────────────────────────────────────────
    output_path = "Documentacao_TechWear_ABNT.docx"
    doc.save(output_path)
    print(f"Documento gerado com sucesso: {output_path}")


if __name__ == "__main__":
    build_document()
