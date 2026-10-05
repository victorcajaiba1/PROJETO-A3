// ============================================================
// TechWearDB — catálogo de produtos no PostgreSQL (API /api/produtos)
// O banco é a fonte oficial; o localStorage guarda uma cópia para as
// páginas lerem de forma síncrona (TechWear.getProdutos).
// Sem servidor (ex.: arquivo aberto direto no navegador), usa só o localStorage.
// ============================================================

var TechWearDB = (function () {
    'use strict';

    var API = '/api';
    var CHAVE_TOKEN = 'tw_admin_token';
    var CHAVE_BACKUP = 'tw_produtos_backup';
    var _ready = false;
    var _carga = null;

    function _lerJSON(chave, padrao) {
        try { return JSON.parse(localStorage.getItem(chave) || 'null') || padrao; } catch (e) { return padrao; }
    }

    // Projeção usada para saber se o catálogo deste navegador difere do banco
    function _assinatura(produtos) {
        return JSON.stringify(produtos.map(function (p) {
            return [p.id, p.nome, Number(p.preco), parseInt(p.estoque, 10) || 0, p.categoria,
                    p.esporte || '', p.imagem || '', (p.tamanhos || []).join(',')];
        }).sort(function (a, b) { return a[0] - b[0]; }));
    }

    function _salvarCache(produtos) {
        localStorage.setItem('tw_produtos', JSON.stringify(produtos));
        localStorage.setItem('tw_dados_versao', 'servidor');
    }

    function _erroDaResposta(r) {
        return r.json().catch(function () { return {}; }).then(function (data) {
            var err = new Error(typeof data.detail === 'string' ? data.detail : 'Erro ' + r.status);
            err.status = r.status;
            throw err;
        });
    }

    // --------------------------------------------------------
    // Carga do catálogo (uma vez por página)
    // --------------------------------------------------------
    function _carregar() {
        if (_carga) return _carga;
        _carga = fetch(API + '/produtos', { cache: 'no-store' })
            .then(function (r) { return r.ok ? r.json() : _erroDaResposta(r); })
            .then(function (produtos) {
                // Catálogo editado só neste navegador (antes do banco): guarda
                // uma cópia para o admin poder publicar em vez de perdê-lo
                var versao = localStorage.getItem('tw_dados_versao');
                var local = _lerJSON('tw_produtos', null);
                if (versao !== 'servidor' && local && local.length &&
                    !localStorage.getItem(CHAVE_BACKUP) &&
                    _assinatura(local) !== _assinatura(produtos)) {
                    localStorage.setItem(CHAVE_BACKUP, JSON.stringify(local));
                }
                _salvarCache(produtos);
                _ready = true;
                return produtos;
            });
        _carga.catch(function (err) {
            console.warn('[TechWearDB] Catálogo do servidor indisponível, usando localStorage:', err);
        });
        return _carga;
    }

    function init(callback) {
        _carregar().then(function () {
            if (callback) callback(null);
        }, function (err) {
            if (callback) callback(err);
        });
    }

    // --------------------------------------------------------
    // Escrita (exige senha de administrador do servidor)
    // --------------------------------------------------------
    function _token() {
        try { return sessionStorage.getItem(CHAVE_TOKEN) || ''; } catch (e) { return ''; }
    }

    function _loginAdmin() {
        var senha = window.prompt('Senha de administrador do servidor (variável ADMIN_PASSWORD na Railway):');
        if (!senha) return Promise.reject(new Error('Login de administrador cancelado.'));
        return fetch(API + '/admin/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ senha: senha })
        }).then(function (r) { return r.ok ? r.json() : _erroDaResposta(r); })
          .then(function (data) {
              try { sessionStorage.setItem(CHAVE_TOKEN, data.token); } catch (e) {}
              return data.token;
          });
    }

    // Envia a requisição; se o token faltar ou expirar, pede a senha e repete uma vez
    function _requisicaoAdmin(metodo, caminho, corpo, tentouLogin) {
        var headers = { 'Authorization': 'Bearer ' + _token() };
        if (corpo) headers['Content-Type'] = 'application/json';
        return fetch(API + caminho, {
            method: metodo,
            headers: headers,
            body: corpo ? JSON.stringify(corpo) : undefined
        }).then(function (r) {
            if (r.status === 401 && !tentouLogin) {
                return _loginAdmin().then(function () {
                    return _requisicaoAdmin(metodo, caminho, corpo, true);
                });
            }
            if (!r.ok) return _erroDaResposta(r);
            return r.status === 204 ? null : r.json();
        });
    }

    function _corpo(dados) {
        return {
            nome: dados.nome,
            descricao: dados.descricao || '',
            preco: Number(dados.preco),
            categoria: dados.categoria,
            esporte: dados.esporte || '',
            tamanhos: dados.tamanhos || ['P', 'M', 'G'],
            cor: dados.cor || '',
            hex_color: dados.hex_color || '#808080',
            imagem: dados.imagem || '',
            estoque: parseInt(dados.estoque, 10) || 0
        };
    }

    function _atualizarCache(fn) {
        var produtos = _lerJSON('tw_produtos', []);
        _salvarCache(fn(produtos));
    }

    function _semServidor(err) {
        // TypeError = falha de rede (servidor fora do ar ou página aberta como arquivo)
        return err instanceof TypeError;
    }

    function adicionarProduto(dadosProduto) {
        return _requisicaoAdmin('POST', '/produtos', _corpo(dadosProduto)).then(function (produto) {
            _atualizarCache(function (lista) { return lista.concat([produto]); });
            return produto;
        }, function (err) {
            if (!_semServidor(err)) throw err;
            return TechWear.adicionarProduto(dadosProduto);
        });
    }

    function editarProduto(id, dados) {
        var atual = TechWear.getProdutoPorId(id) || {};
        var completo = Object.assign({}, atual, dados);
        return _requisicaoAdmin('PUT', '/produtos/' + id, _corpo(completo)).then(function (produto) {
            _atualizarCache(function (lista) {
                return lista.map(function (p) { return p.id === id ? produto : p; });
            });
            return produto;
        }, function (err) {
            if (!_semServidor(err)) throw err;
            return TechWear.editarProduto(id, dados);
        });
    }

    function removerProduto(id) {
        return _requisicaoAdmin('DELETE', '/produtos/' + id).then(function () {
            _atualizarCache(function (lista) { return lista.filter(function (p) { return p.id !== id; }); });
        }, function (err) {
            if (!_semServidor(err)) throw err;
            TechWear.removerProduto(id);
        });
    }

    // --------------------------------------------------------
    // Catálogo antigo deste navegador → banco
    // --------------------------------------------------------
    function getBackupLocal() {
        return _lerJSON(CHAVE_BACKUP, null);
    }

    function descartarBackupLocal() {
        localStorage.removeItem(CHAVE_BACKUP);
    }

    // Faz o banco ficar igual ao catálogo salvo: edita os produtos que já
    // existem, cria os novos e remove os que não estão no backup
    function publicarBackupLocal() {
        var backup = getBackupLocal();
        if (!backup) return Promise.resolve();
        var servidor = _lerJSON('tw_produtos', []);
        var idsServidor = servidor.map(function (p) { return p.id; });
        var idsBackup = backup.map(function (p) { return p.id; });
        var passos = [];
        backup.forEach(function (p) {
            if (idsServidor.indexOf(p.id) >= 0) {
                passos.push(function () { return _requisicaoAdmin('PUT', '/produtos/' + p.id, _corpo(p)); });
            } else {
                passos.push(function () { return _requisicaoAdmin('POST', '/produtos', _corpo(p)); });
            }
        });
        idsServidor.forEach(function (id) {
            if (idsBackup.indexOf(id) < 0) {
                passos.push(function () { return _requisicaoAdmin('DELETE', '/produtos/' + id); });
            }
        });
        // Em sequência: o primeiro passo pede a senha e os seguintes reaproveitam o token
        return passos.reduce(function (anterior, passo) {
            return anterior.then(passo);
        }, Promise.resolve()).then(function () {
            descartarBackupLocal();
            _carga = null;
            return _carregar();
        });
    }

    // Atualiza a cópia local em toda página que carrega este script
    _carregar().catch(function () {});

    return {
        init: init,
        isReady: function () { return _ready; },
        adicionarProduto: adicionarProduto,
        editarProduto: editarProduto,
        removerProduto: removerProduto,
        getBackupLocal: getBackupLocal,
        publicarBackupLocal: publicarBackupLocal,
        descartarBackupLocal: descartarBackupLocal
    };
})();
