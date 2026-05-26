<h1 align="center">
  <br>
  👕 Tech Wear
  <br>
</h1>

<p align="center">
  <b>E-commerce de roupas esportivas com busca visual inteligente por IA</b><br>
  Projeto A3 — Análise e Projeto de Sistemas · USJT
</p>

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/YOLO-00FFFF?style=flat&logo=yolo&logoColor=black" />
  <img src="https://img.shields.io/badge/CLIP-412991?style=flat&logo=openai&logoColor=white" />
</p>

---

## 📋 Sobre o Projeto

O **Tech Wear** é uma plataforma completa de e-commerce especializada em vestuário esportivo. O sistema integra um frontend web responsivo a um backend de inteligência artificial, permitindo ao usuário encontrar produtos por **busca visual** — basta fotografar qualquer peça de roupa para receber recomendações de produtos similares do catálogo.

### ✨ Destaques

- 🔍 **WearIA** — busca visual com YOLO + CLIP + extração de cor (KMeans)
- 🛒 Catálogo com filtros por categoria, esporte, preço e busca textual
- 💳 Fluxo completo de compra: carrinho → frete → pagamento → nota fiscal
- 📦 Cálculo de frete baseado na tabela ANTT com decomposição de impostos (ICMS, PIS, COFINS)
- 📊 Dashboard gerencial com previsão de vendas por regressão linear e controle de estoque
- 🌙 Tema claro/escuro com persistência
- 🔐 Autenticação de usuários e painel administrativo

---

## 🗂️ Estrutura do Projeto

```
Projeto USJT/
│
├── index.html            # Página inicial (hero + destaques)
├── markets.html          # Catálogo de produtos com filtros
├── wallet.html           # Carrinho de compras
├── frete.html            # Cálculo de frete por CEP
├── pagamento.html        # Seleção de método de pagamento
├── nota-fiscal.html      # Nota fiscal eletrônica
├── login.html            # Autenticação e registro
├── admin.html            # Painel administrativo (CRUD de produtos)
├── settings.html         # Perfil e configurações do usuário
├── dashboard.html        # Dashboard com KPIs e previsão de vendas
├── wearia.html           # Busca visual inteligente (WearIA)
│
├── css/                  # Estilos CSS globais e por página
├── js/
│   ├── produtos.js       # API global window.TechWear (localStorage)
│   ├── wearia.js         # Integração com o backend de IA
│   └── firebase-config.js
│
└── backend/              # API Python (FastAPI)
    ├── main.py           # Entrada da aplicação
    ├── routes/
    │   └── image_search.py   # Endpoints REST
    ├── services/
    │   ├── yolo_service.py   # Detecção de roupas (YOLOv8)
    │   ├── clip_service.py   # Embeddings visuais (CLIP)
    │   ├── color_service.py  # Cor dominante (KMeans)
    │   └── recommendation_service.py  # Ranking híbrido
    ├── models/
    │   └── product.py    # Schemas Pydantic
    └── requirements.txt
```

---

## 🚀 Como Rodar

### Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- Navegador moderno (Chrome, Firefox ou Edge)

---

### 1. Frontend (sem instalação)

Abra qualquer `.html` diretamente no navegador **ou** sirva com um servidor local:

```bash
# Python (qualquer versão)
python -m http.server 3000
```

Acesse: `http://localhost:3000/index.html`

---

### 2. Backend — WearIA (busca visual por IA)

> **Necessário apenas para usar a busca visual.**

#### Criar ambiente virtual e instalar dependências

```bash
cd backend

# Windows
python -m venv ../.venv
..\.venv\Scripts\activate

# Linux / macOS
python -m venv ../.venv
source ../.venv/bin/activate

# Instalar pacotes
pip install -r requirements.txt
```

#### Iniciar o servidor FastAPI

```bash
# Na raiz do projeto (com venv ativado)
uvicorn backend.main:app --reload --port 8000
```

API disponível em: `http://localhost:8000`  
Documentação interativa: `http://localhost:8000/docs`

---

## 🔌 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Health check |
| `POST` | `/api/search-by-image` | Busca produtos por imagem (multipart) |
| `POST` | `/api/index-products` | Indexa catálogo do frontend com embeddings |

---

## 🧮 Modelos Matemáticos Utilizados

| Módulo | Modelo | Fórmula |
|--------|--------|---------|
| **Frete** | Equação 1.º grau multiplicativa | `Frete = d × R$ 3,8866/km` |
| **Frete** | Fórmula de tempo (cinemática) | `t = (d × k_rota) ÷ (v × f_horário)` |
| **Frete** | Score de prioridade | `Sp = urgência × 0,6 + densidade × 0,4` |
| **Dashboard** | Regressão linear (MQO) | `ŷ = m·x + b` |
| **Dashboard** | Coeficiente R² | `R² = 1 − SS_res/SS_tot` |
| **Estoque** | Velocidade de venda | `t_ruptura = estoque ÷ (vel_30 ÷ 30)` |
| **WearIA** | Ranking híbrido | `score = 0,7 × sim_CLIP + 0,3 × sim_cor` |

---

## 🛠️ Tecnologias

### Frontend
| Tecnologia | Uso |
|---|---|
| HTML5 + CSS3 | Estrutura e estilização responsiva |
| JavaScript ES5/ES6 | Lógica, DOM, fetch API e localStorage |
| Material Symbols Outlined | Ícones vetoriais |
| Instrument Sans (Google Fonts) | Tipografia |
| Chart.js | Gráficos do dashboard |

### Backend
| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.13 | Linguagem principal |
| FastAPI | 0.115 | Framework da API REST |
| Uvicorn | 0.30 | Servidor ASGI |
| YOLOv8 (Ultralytics) | 8.2 | Detecção de roupas em imagens |
| CLIP (Hugging Face) | clip-vit-base-patch32 | Embeddings visuais e semânticos |
| scikit-learn | 1.5 | KMeans para extração de cor dominante |
| PyTorch | 2.4 | Framework de deep learning |
| Pillow | 10.4 | Manipulação de imagens |

---

## 💾 Persistência de Dados (LocalStorage)

| Chave | Conteúdo |
|---|---|
| `tw_produtos` | Catálogo de produtos (array) |
| `tw_carrinho` | Itens no carrinho |
| `tw_usuarios` | Usuários cadastrados |
| `tw_sessao` | Usuário logado |
| `tw_pedidos` | Histórico de pedidos |
| `theme` | Tema da interface (`dark` / `light`) |

---

## 📄 Documentação

A documentação técnica completa em formato **ABNT** está disponível em:  
📎 [`Documentacao_TechWear_ABNT.docx`](./Documentacao_TechWear_ABNT.docx)

---

## 👥 Participantes

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ArthurMedinaDev">
        <img src="https://github.com/ArthurMedinaDev.png" width="100px;" alt="Arthur"/><br>
        <sub><b>Arthur Medina</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/carloshenriquess23">
        <img src="https://github.com/carloshenriquess23.png" width="100px;" alt="Carlos"/><br>
        <sub><b>Carlos Henrique</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Lucas14almeida">
        <img src="https://github.com/Lucas14almeida.png" width="100px;" alt="Lucas"/><br>
        <sub><b>Lucas Almeida</b></sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/ThiagoCruz00">
        <img src="https://github.com/ThiagoCruz00.png" width="100px;" alt="Thiago"/><br>
        <sub><b>Thiago Cruz</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/tteuwm">
        <img src="https://github.com/tteuwm.png" width="100px;" alt="Matheus"/><br>
        <sub><b>Matheus</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/victorcajaiba1">
        <img src="https://github.com/victorcajaiba1.png" width="100px;" alt="Victor"/><br>
        <sub><b>Victor Cajaiba</b></sub>
      </a>
    </td>
  </tr>
</table>

Desenvolvido como Projeto A3 para a disciplina de **Matemática Computacional Aplicada** da **Universidade São Judas Tadeu (USJT)**.

---

<p align="center">
  Feito com ❤️ pela equipe Tech Wear · 2026
</p>
