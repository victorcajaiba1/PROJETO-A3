(function() {
    'use strict';

    // ========================================
    // Dados dos Produtos
    // ========================================
    var PRODUTOS_PADRAO = [
        {
            id: 1,
            nome: 'Camiseta Essential Branca',
            descricao: 'Camiseta de algodão penteado com toque macio e caimento reto, básica para treino e dia a dia.',
            preco: 79.90,
            categoria: 'camisetas',
            tamanhos: ['P', 'M', 'G', 'GG', 'XG'],
            cor: 'Branco',
            hex_color: '#eeefef',
            imagem: 'img/produtos/camiseta-essential-branca.jpg',
            estoque: 48,
            esporte: 'academia'
        },
        {
            id: 2,
            nome: 'Camiseta Dry-Fit Preta',
            descricao: 'Tecido dry-fit que afasta o suor da pele e seca rápido. Estampa circular discreta no peito.',
            preco: 89.90,
            categoria: 'camisetas',
            tamanhos: ['P', 'M', 'G', 'GG', 'XG'],
            cor: 'Preto',
            hex_color: '#111111',
            imagem: 'img/produtos/camiseta-dry-fit-preta.jpg',
            estoque: 40,
            esporte: 'academia'
        },
        {
            id: 3,
            nome: 'Camiseta Performance Vermelha',
            descricao: 'Malha leve com proteção UV 50+ e costuras planas para corridas longas sem atrito.',
            preco: 99.90,
            categoria: 'camisetas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Vermelho',
            hex_color: '#cc011e',
            imagem: 'img/produtos/camiseta-performance-vermelha.jpg',
            estoque: 32,
            esporte: 'corrida'
        },
        {
            id: 4,
            nome: 'Camiseta Run Amarela',
            descricao: 'Cor de alta visibilidade para treinos ao ar livre, com tecido respirável e secagem rápida.',
            preco: 94.90,
            categoria: 'camisetas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Amarelo',
            hex_color: '#eee373',
            imagem: 'img/produtos/camiseta-run-amarela.jpg',
            estoque: 26,
            esporte: 'corrida'
        },
        {
            id: 5,
            nome: 'Regata Basquete Creme',
            descricao: 'Regata de basquete em mesh com acabamento em ribana e número aplicado nas costas.',
            preco: 149.90,
            categoria: 'camisetas',
            tamanhos: ['M', 'G', 'GG', 'XG'],
            cor: 'Bege',
            hex_color: '#d9cfae',
            imagem: 'img/produtos/regata-basquete-creme.jpg',
            estoque: 18,
            esporte: 'basquete'
        },
        {
            id: 6,
            nome: 'Regata Basquete Marinho',
            descricao: 'Regata de quadra em mesh leve com recortes laterais para ventilação.',
            preco: 149.90,
            categoria: 'camisetas',
            tamanhos: ['M', 'G', 'GG', 'XG'],
            cor: 'Azul Marinho',
            hex_color: '#1b2440',
            imagem: 'img/produtos/regata-basquete-marinho.jpg',
            estoque: 20,
            esporte: 'basquete'
        },
        {
            id: 7,
            nome: 'Camiseta Fitness Verde',
            descricao: 'Modelagem feminina levemente ajustada, tecido com elastano para liberdade de movimento.',
            preco: 89.90,
            categoria: 'camisetas',
            tamanhos: ['PP', 'P', 'M', 'G'],
            cor: 'Verde',
            hex_color: '#5f7a72',
            imagem: 'img/produtos/camiseta-fitness-verde.jpg',
            estoque: 30,
            esporte: 'academia'
        },
        {
            id: 8,
            nome: 'Camiseta Training Azul',
            descricao: 'Cropped de treino com recortes em mesh e tecido de compressão leve.',
            preco: 99.90,
            categoria: 'camisetas',
            tamanhos: ['PP', 'P', 'M', 'G'],
            cor: 'Azul',
            hex_color: '#4b5ba6',
            imagem: 'img/produtos/camiseta-training-azul.jpg',
            estoque: 22,
            esporte: 'academia'
        },
        {
            id: 9,
            nome: 'Legging Compressão Preta',
            descricao: 'Legging de cintura alta com compressão média, não fica transparente no agachamento.',
            preco: 159.90,
            categoria: 'calcas',
            tamanhos: ['PP', 'P', 'M', 'G', 'GG'],
            cor: 'Preto',
            hex_color: '#111111',
            imagem: 'img/produtos/legging-compressao-preta.jpg',
            estoque: 35,
            esporte: 'academia'
        },
        {
            id: 10,
            nome: 'Calça Moletom Cinza',
            descricao: 'Moletom flanelado por dentro, cós com cordão e bolsos laterais. Conforto para o pós-treino.',
            preco: 169.90,
            categoria: 'calcas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Cinza',
            hex_color: '#c2c3c5',
            imagem: 'img/produtos/calca-moletom-cinza.jpg',
            estoque: 28,
            esporte: 'academia'
        },
        {
            id: 11,
            nome: 'Calça Jogger Turquesa',
            descricao: 'Jogger leve com punho na barra e cós elástico, ideal para aquecimento e trote.',
            preco: 179.90,
            categoria: 'calcas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Azul',
            hex_color: '#40a7c1',
            imagem: 'img/produtos/calca-jogger-turquesa.jpg',
            estoque: 16,
            esporte: 'corrida'
        },
        {
            id: 12,
            nome: 'Calça Jogger Cáqui',
            descricao: 'Sarja com elastano, punho na barra e bolsos funcionais. Vai do treino à rua.',
            preco: 189.90,
            categoria: 'calcas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Bege',
            hex_color: '#a08c6c',
            imagem: 'img/produtos/calca-jogger-caqui.jpg',
            estoque: 24,
            esporte: 'corrida'
        },
        {
            id: 13,
            nome: 'Calça Track Listrada',
            descricao: 'Calça de agasalho com listras laterais contrastantes e zíper no tornozelo.',
            preco: 199.90,
            categoria: 'calcas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Preto',
            hex_color: '#121417',
            imagem: 'img/produtos/calca-track-listrada.jpg',
            estoque: 20,
            esporte: 'corrida'
        },
        {
            id: 14,
            nome: 'Calça Jogger Roxa',
            descricao: 'Moletom leve com bolsos e punho elástico, cor vibrante para o treino.',
            preco: 179.90,
            categoria: 'calcas',
            tamanhos: ['P', 'M', 'G'],
            cor: 'Roxo',
            hex_color: '#492854',
            imagem: 'img/produtos/calca-jogger-roxa.jpg',
            estoque: 14,
            esporte: 'academia'
        },
        {
            id: 15,
            nome: 'Jaqueta Corta-Vento Tricolor',
            descricao: 'Corta-vento repelente à água com capuz embutido e blocos de cor preto, branco e amarelo.',
            preco: 299.90,
            categoria: 'jaquetas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Preto',
            hex_color: '#1a1b1b',
            imagem: 'img/produtos/jaqueta-corta-vento-tricolor.jpg',
            estoque: 15,
            esporte: 'corrida'
        },
        {
            id: 16,
            nome: 'Jaqueta Bomber Marinho',
            descricao: 'Bomber acolchoada com gola forrada em pelúcia e punhos canelados.',
            preco: 349.90,
            categoria: 'jaquetas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Azul Marinho',
            hex_color: '#2e3d57',
            imagem: 'img/produtos/jaqueta-bomber-marinho.jpg',
            estoque: 12,
            esporte: 'todos'
        },
        {
            id: 17,
            nome: 'Jaqueta Track Vermelha',
            descricao: 'Jaqueta de agasalho com zíper frontal e listras brancas nas mangas.',
            preco: 279.90,
            categoria: 'jaquetas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Vermelho',
            hex_color: '#c82d2d',
            imagem: 'img/produtos/jaqueta-track-vermelha.jpg',
            estoque: 18,
            esporte: 'corrida'
        },
        {
            id: 18,
            nome: 'Jaqueta Puffer Amarela',
            descricao: 'Puffer volumosa com enchimento térmico leve, gola alta e acabamento brilhante.',
            preco: 449.90,
            categoria: 'jaquetas',
            tamanhos: ['P', 'M', 'G'],
            cor: 'Amarelo',
            hex_color: '#f2c12e',
            imagem: 'img/produtos/jaqueta-puffer-amarela.jpg',
            estoque: 10,
            esporte: 'todos'
        },
        {
            id: 19,
            nome: 'Jaqueta Puffer Laranja',
            descricao: 'Puffer com capuz e gomos largos, quente e leve para dias frios.',
            preco: 449.90,
            categoria: 'jaquetas',
            tamanhos: ['M', 'G', 'GG'],
            cor: 'Laranja',
            hex_color: '#d2691e',
            imagem: 'img/produtos/jaqueta-puffer-laranja.jpg',
            estoque: 9,
            esporte: 'todos'
        },
        {
            id: 20,
            nome: 'Jaqueta Puffer Off-White',
            descricao: 'Puffer oversized em tom off-white com gola alta e bolsos com zíper.',
            preco: 469.90,
            categoria: 'jaquetas',
            tamanhos: ['P', 'M', 'G'],
            cor: 'Branco',
            hex_color: '#e8e6dc',
            imagem: 'img/produtos/jaqueta-puffer-off-white.jpg',
            estoque: 8,
            esporte: 'todos'
        },
        {
            id: 21,
            nome: 'Jaqueta Retrô Lilás',
            descricao: 'Corta-vento estilo anos 90 em nylon com recortes coloridos e capuz.',
            preco: 319.90,
            categoria: 'jaquetas',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Lilás',
            hex_color: '#7f7fc4',
            imagem: 'img/produtos/jaqueta-retro-lilas.jpg',
            estoque: 11,
            esporte: 'corrida'
        },
        {
            id: 22,
            nome: 'Moletom Cinza Mescla',
            descricao: 'Moletom canguru com capuz forrado e bolso frontal, peso médio.',
            preco: 229.90,
            categoria: 'moletons',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Cinza',
            hex_color: '#d5dde0',
            imagem: 'img/produtos/moletom-cinza-mescla.jpg',
            estoque: 30,
            esporte: 'academia'
        },
        {
            id: 23,
            nome: 'Moletom Verde Floresta',
            descricao: 'Capuz com cordão, punhos canelados e bordado discreto no peito.',
            preco: 239.90,
            categoria: 'moletons',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Verde Militar',
            hex_color: '#1e4a42',
            imagem: 'img/produtos/moletom-verde-floresta.jpg',
            estoque: 22,
            esporte: 'todos'
        },
        {
            id: 24,
            nome: 'Moletom Rosa Oversized',
            descricao: 'Modelagem ampla e ombro caído em moletom felpado macio.',
            preco: 259.90,
            categoria: 'moletons',
            tamanhos: ['P', 'M', 'G'],
            cor: 'Rosa',
            hex_color: '#f7b8e0',
            imagem: 'img/produtos/moletom-rosa-oversized.jpg',
            estoque: 16,
            esporte: 'todos'
        },
        {
            id: 25,
            nome: 'Moletom Branco Basic',
            descricao: 'O moletom básico: capuz, bolso canguru e algodão encorpado.',
            preco: 219.90,
            categoria: 'moletons',
            tamanhos: ['P', 'M', 'G', 'GG', 'XG'],
            cor: 'Branco',
            hex_color: '#e6e6e6',
            imagem: 'img/produtos/moletom-branco-basic.jpg',
            estoque: 25,
            esporte: 'todos'
        },
        {
            id: 26,
            nome: 'Moletom Bege Areia',
            descricao: 'Tom neutro areia, capuz amplo e interior flanelado.',
            preco: 239.90,
            categoria: 'moletons',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Bege',
            hex_color: '#cdb3a5',
            imagem: 'img/produtos/moletom-bege-areia.jpg',
            estoque: 20,
            esporte: 'todos'
        },
        {
            id: 27,
            nome: 'Moletom Preto Essential',
            descricao: 'Moletom preto com capuz e bolso canguru, combina com tudo.',
            preco: 229.90,
            categoria: 'moletons',
            tamanhos: ['P', 'M', 'G', 'GG', 'XG'],
            cor: 'Preto',
            hex_color: '#181618',
            imagem: 'img/produtos/moletom-preto-essential.jpg',
            estoque: 34,
            esporte: 'todos'
        },
        {
            id: 28,
            nome: 'Shorts Basquete Amarelo',
            descricao: 'Shorts de basquete em mesh com cós elástico largo e comprimento até o joelho.',
            preco: 129.90,
            categoria: 'shorts',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Amarelo',
            hex_color: '#f2c200',
            imagem: 'img/produtos/shorts-basquete-amarelo.jpg',
            estoque: 24,
            esporte: 'basquete'
        },
        {
            id: 29,
            nome: 'Shorts Tactel Água',
            descricao: 'Tactel leve com forro interno e secagem rápida.',
            preco: 99.90,
            categoria: 'shorts',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Azul',
            hex_color: '#48d1d6',
            imagem: 'img/produtos/shorts-tactel-agua.jpg',
            estoque: 30,
            esporte: 'corrida'
        },
        {
            id: 30,
            nome: 'Shorts Academia Vermelho',
            descricao: 'Shorts de treino com tecido elástico em 4 direções para agachamento e levantamento.',
            preco: 109.90,
            categoria: 'shorts',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Vermelho',
            hex_color: '#c0262c',
            imagem: 'img/produtos/shorts-academia-vermelho.jpg',
            estoque: 28,
            esporte: 'academia'
        },
        {
            id: 31,
            nome: 'Shorts Corrida Laranja',
            descricao: 'Shorts de corrida com bermuda interna de compressão e bolso para chave.',
            preco: 119.90,
            categoria: 'shorts',
            tamanhos: ['PP', 'P', 'M', 'G'],
            cor: 'Laranja',
            hex_color: '#e8622c',
            imagem: 'img/produtos/shorts-corrida-laranja.jpg',
            estoque: 18,
            esporte: 'corrida'
        },
        {
            id: 32,
            nome: 'Shorts Fitness Grafite',
            descricao: 'Shorts soltinho com cós alto e laterais abertas para mais mobilidade.',
            preco: 109.90,
            categoria: 'shorts',
            tamanhos: ['PP', 'P', 'M', 'G'],
            cor: 'Cinza',
            hex_color: '#4b4250',
            imagem: 'img/produtos/shorts-fitness-grafite.jpg',
            estoque: 20,
            esporte: 'academia'
        },
        {
            id: 33,
            nome: 'Shorts Basquete Preto',
            descricao: 'Shorts de quadra em mesh duplo com faixa lateral contrastante.',
            preco: 129.90,
            categoria: 'shorts',
            tamanhos: ['P', 'M', 'G', 'GG'],
            cor: 'Preto',
            hex_color: '#1a1a1a',
            imagem: 'img/produtos/shorts-basquete-preto.jpg',
            estoque: 26,
            esporte: 'basquete'
        }
    ];

    // Versão do catálogo padrão. Ao subir a versão, quem já tem catálogo salvo
    // recebe o catálogo novo inteiro (e o carrinho é esvaziado, pois os ids mudam).
    var DADOS_VERSAO = '2.0';

    // ========================================
    // Gerenciamento de Produtos (localStorage)
    // ========================================
    function getProdutos() {
        var saved = localStorage.getItem('tw_produtos');
        var versao = localStorage.getItem('tw_dados_versao');
        // Catálogo vindo do banco (js/catalogo-db.js) é a fonte oficial: não mexer
        if (saved && (versao === DADOS_VERSAO || versao === 'servidor')) return JSON.parse(saved);
        if (saved) localStorage.removeItem('tw_carrinho');
        localStorage.setItem('tw_produtos', JSON.stringify(PRODUTOS_PADRAO));
        localStorage.setItem('tw_dados_versao', DADOS_VERSAO);
        return PRODUTOS_PADRAO;
    }

    function salvarProdutos(produtos) {
        localStorage.setItem('tw_produtos', JSON.stringify(produtos));
    }

    function getProdutoPorId(id) {
        var produtos = getProdutos();
        for (var i = 0; i < produtos.length; i++) {
            if (produtos[i].id === id) return produtos[i];
        }
        return null;
    }

    function adicionarProduto(produto) {
        var produtos = getProdutos();
        produto.id = produtos.length > 0 ? Math.max.apply(null, produtos.map(function(p) { return p.id; })) + 1 : 1;
        produtos.push(produto);
        salvarProdutos(produtos);
        return produto;
    }

    function editarProduto(id, dados) {
        var produtos = getProdutos();
        for (var i = 0; i < produtos.length; i++) {
            if (produtos[i].id === id) {
                for (var key in dados) {
                    if (dados.hasOwnProperty(key)) produtos[i][key] = dados[key];
                }
                salvarProdutos(produtos);
                return produtos[i];
            }
        }
        return null;
    }

    function removerProduto(id) {
        var produtos = getProdutos();
        produtos = produtos.filter(function(p) { return p.id !== id; });
        salvarProdutos(produtos);
    }

    // ========================================
    // Carrinho de Compras
    // ========================================
    function getCarrinho() {
        var saved = localStorage.getItem('tw_carrinho');
        return saved ? JSON.parse(saved) : [];
    }

    function salvarCarrinho(carrinho) {
        localStorage.setItem('tw_carrinho', JSON.stringify(carrinho));
        atualizarBadgeCarrinho();
    }

    // Quantidade de um produto ainda livre para adicionar (estoque − o que já está no carrinho)
    function getEstoqueDisponivel(produtoId, ignorarTamanho) {
        var produto = getProdutoPorId(produtoId);
        if (!produto) return 0;
        var noCarrinho = 0;
        getCarrinho().forEach(function(item) {
            if (item.produtoId === produtoId && item.tamanho !== ignorarTamanho) noCarrinho += item.quantidade;
        });
        return Math.max(0, (parseInt(produto.estoque, 10) || 0) - noCarrinho);
    }

    function adicionarAoCarrinho(produtoId, tamanho, quantidade) {
        quantidade = quantidade || 1;
        var disponivel = getEstoqueDisponivel(produtoId);
        if (disponivel <= 0) return { erro: 'Produto sem estoque disponível', disponivel: 0 };
        if (quantidade > disponivel) return { erro: 'Apenas ' + disponivel + ' unidade(s) disponível(is)', disponivel: disponivel };
        var carrinho = getCarrinho();
        var existente = null;
        for (var i = 0; i < carrinho.length; i++) {
            if (carrinho[i].produtoId === produtoId && carrinho[i].tamanho === tamanho) {
                existente = carrinho[i];
                break;
            }
        }
        if (existente) {
            existente.quantidade += quantidade;
        } else {
            carrinho.push({ produtoId: produtoId, tamanho: tamanho, quantidade: quantidade });
        }
        salvarCarrinho(carrinho);
        return { sucesso: true };
    }

    function removerDoCarrinho(produtoId, tamanho) {
        var carrinho = getCarrinho();
        carrinho = carrinho.filter(function(item) {
            return !(item.produtoId === produtoId && item.tamanho === tamanho);
        });
        salvarCarrinho(carrinho);
    }

    function alterarQuantidade(produtoId, tamanho, novaQtd) {
        if (novaQtd < 1) { removerDoCarrinho(produtoId, tamanho); return { sucesso: true }; }
        var disponivel = getEstoqueDisponivel(produtoId, tamanho);
        if (novaQtd > disponivel) return { erro: 'Apenas ' + disponivel + ' unidade(s) em estoque', disponivel: disponivel };
        var carrinho = getCarrinho();
        for (var i = 0; i < carrinho.length; i++) {
            if (carrinho[i].produtoId === produtoId && carrinho[i].tamanho === tamanho) {
                carrinho[i].quantidade = novaQtd;
                break;
            }
        }
        salvarCarrinho(carrinho);
        return { sucesso: true };
    }

    function limparCarrinho() {
        localStorage.removeItem('tw_carrinho');
        atualizarBadgeCarrinho();
    }

    function getTotalCarrinho() {
        var carrinho = getCarrinho();
        var total = 0;
        for (var i = 0; i < carrinho.length; i++) {
            var produto = getProdutoPorId(carrinho[i].produtoId);
            if (produto) total += produto.preco * carrinho[i].quantidade;
        }
        return total;
    }

    function getQtdCarrinho() {
        var carrinho = getCarrinho();
        var qtd = 0;
        for (var i = 0; i < carrinho.length; i++) qtd += carrinho[i].quantidade;
        return qtd;
    }

    function atualizarBadgeCarrinho() {
        var badges = document.querySelectorAll('.cart-badge');
        var qtd = getQtdCarrinho();
        badges.forEach(function(badge) {
            badge.textContent = qtd;
            badge.style.display = qtd > 0 ? 'flex' : 'none';
        });
    }

    // ========================================
    // Superuser fixo (sempre disponível)
    // ========================================
    var SUPERUSER = {
        id: 0,
        nome: 'Super Admin',
        email: 'admin@techwear.com',
        senha: btoa('admin123'),
        perfil: 'admin',
        criadoEm: '2026-01-01T00:00:00.000Z'
    };

    // ========================================
    // Usuários e Autenticação
    // ========================================
    function getUsuarios() {
        var saved = localStorage.getItem('tw_usuarios');
        var usuarios = saved ? JSON.parse(saved) : [];
        // Migração: garante que todos tenham perfil
        var temAdmin = usuarios.some(function(u) { return u.perfil === 'admin'; });
        var alterou = false;
        usuarios.forEach(function(u, i) {
            if (!u.perfil) {
                u.perfil = (!temAdmin && i === 0) ? 'admin' : 'cliente';
                if (!temAdmin && i === 0) temAdmin = true;
                alterou = true;
            }
        });
        if (alterou) localStorage.setItem('tw_usuarios', JSON.stringify(usuarios));
        return usuarios;
    }

    function registrarUsuario(nome, email, senha) {
        var usuarios = getUsuarios();
        for (var i = 0; i < usuarios.length; i++) {
            if (usuarios[i].email === email) return { erro: 'E-mail já cadastrado' };
        }
        var novoUsuario = {
            id: Date.now(),
            nome: nome,
            email: email,
            senha: btoa(senha), // encoding simples para protótipo
            perfil: usuarios.length === 0 ? 'admin' : 'cliente',
            criadoEm: new Date().toISOString()
        };
        usuarios.push(novoUsuario);
        localStorage.setItem('tw_usuarios', JSON.stringify(usuarios));
        return { sucesso: true, usuario: novoUsuario };
    }

    function loginUsuario(email, senha) {
        // Superuser fixo
        if (email === SUPERUSER.email && btoa(senha) === SUPERUSER.senha) {
            var sessaoSuper = { id: SUPERUSER.id, nome: SUPERUSER.nome, email: SUPERUSER.email, perfil: 'admin' };
            localStorage.setItem('tw_sessao', JSON.stringify(sessaoSuper));
            return { sucesso: true, usuario: sessaoSuper };
        }
        var usuarios = getUsuarios();
        for (var i = 0; i < usuarios.length; i++) {
            if (usuarios[i].email === email && usuarios[i].senha === btoa(senha)) {
                var sessao = { id: usuarios[i].id, nome: usuarios[i].nome, email: usuarios[i].email, perfil: usuarios[i].perfil || 'cliente' };
                localStorage.setItem('tw_sessao', JSON.stringify(sessao));
                return { sucesso: true, usuario: sessao };
            }
        }
        return { erro: 'E-mail ou senha incorretos' };
    }

    function isAdmin() {
        var sessao = getUsuarioLogado();
        return sessao !== null && sessao.perfil === 'admin';
    }

    function alterarPerfilUsuario(id, perfil) {
        var usuarios = getUsuarios();
        for (var i = 0; i < usuarios.length; i++) {
            if (usuarios[i].id === id) {
                usuarios[i].perfil = perfil;
                localStorage.setItem('tw_usuarios', JSON.stringify(usuarios));
                // Atualiza sessão se for o usuário logado
                var sessao = getUsuarioLogado();
                if (sessao && sessao.id === id) {
                    sessao.perfil = perfil;
                    localStorage.setItem('tw_sessao', JSON.stringify(sessao));
                }
                return true;
            }
        }
        return false;
    }

    function getUsuarioLogado() {
        var saved = localStorage.getItem('tw_sessao');
        return saved ? JSON.parse(saved) : null;
    }

    function logout() {
        localStorage.removeItem('tw_sessao');
        window.location.href = 'login.html';
    }

    // ========================================
    // Pedidos
    // ========================================
    function getPedidos() {
        var saved = localStorage.getItem('tw_pedidos');
        return saved ? JSON.parse(saved) : [];
    }

    // opcoes.total: valor final pago (produtos + frete − desconto + juros).
    // Sem ele, o total é só a soma dos produtos.
    function criarPedido(endereco, opcoes) {
        opcoes = opcoes || {};
        var carrinho = getCarrinho();
        if (carrinho.length === 0) return { erro: 'Carrinho vazio' };
        var usuario = getUsuarioLogado();
        var produtos = getProdutos();
        var itens = [];
        for (var i = 0; i < carrinho.length; i++) {
            var produto = null;
            for (var j = 0; j < produtos.length; j++) {
                if (produtos[j].id === carrinho[i].produtoId) { produto = produtos[j]; break; }
            }
            if (produto) {
                if ((parseInt(produto.estoque, 10) || 0) < carrinho[i].quantidade) {
                    return { erro: 'Estoque insuficiente para ' + produto.nome + ' (restam ' + (produto.estoque || 0) + ')' };
                }
                itens.push({
                    produtoId: produto.id,
                    nome: produto.nome,
                    preco: produto.preco,
                    tamanho: carrinho[i].tamanho,
                    quantidade: carrinho[i].quantidade,
                    subtotal: produto.preco * carrinho[i].quantidade
                });
            }
        }
        // Baixa no estoque
        itens.forEach(function(item) {
            for (var k = 0; k < produtos.length; k++) {
                if (produtos[k].id === item.produtoId) {
                    produtos[k].estoque = (parseInt(produtos[k].estoque, 10) || 0) - item.quantidade;
                    break;
                }
            }
        });
        salvarProdutos(produtos);

        var subtotal = getTotalCarrinho();
        var pedido = {
            id: Date.now(),
            usuarioId: usuario ? usuario.id : null,
            itens: itens,
            subtotal: subtotal,
            total: typeof opcoes.total === 'number' ? Math.round(opcoes.total * 100) / 100 : subtotal,
            endereco: endereco,
            status: 'Confirmado',
            data: new Date().toISOString()
        };
        var pedidos = getPedidos();
        pedidos.unshift(pedido);
        localStorage.setItem('tw_pedidos', JSON.stringify(pedidos));
        limparCarrinho();
        return { sucesso: true, pedido: pedido };
    }

    // ========================================
    // Formatar moeda
    // ========================================
    function formatarPreco(valor) {
        return 'R$ ' + valor.toFixed(2).replace('.', ',');
    }

    // ========================================
    // Expor API global
    // ========================================
    window.TechWear = {
        getProdutos: getProdutos,
        getProdutoPorId: getProdutoPorId,
        adicionarProduto: adicionarProduto,
        editarProduto: editarProduto,
        removerProduto: removerProduto,
        getCarrinho: getCarrinho,
        adicionarAoCarrinho: adicionarAoCarrinho,
        removerDoCarrinho: removerDoCarrinho,
        alterarQuantidade: alterarQuantidade,
        limparCarrinho: limparCarrinho,
        getTotalCarrinho: getTotalCarrinho,
        getQtdCarrinho: getQtdCarrinho,
        getEstoqueDisponivel: getEstoqueDisponivel,
        atualizarBadgeCarrinho: atualizarBadgeCarrinho,
        registrarUsuario: registrarUsuario,
        loginUsuario: loginUsuario,
        getUsuarioLogado: getUsuarioLogado,
        isAdmin: isAdmin,
        alterarPerfilUsuario: alterarPerfilUsuario,
        logout: logout,
        getPedidos: getPedidos,
        criarPedido: criarPedido,
        formatarPreco: formatarPreco
    };

    // Atualizar badge ao carregar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', atualizarBadgeCarrinho);
    } else {
        atualizarBadgeCarrinho();
    }
})();
