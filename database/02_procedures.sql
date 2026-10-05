-- ============================================================
-- Tech Wear — Procedures e triggers
-- reservar_estoque e alterar_preco: iguais aos slides da apresentação.
-- ============================================================

SET client_min_messages = warning;
BEGIN;

-- Reduz o saldo apenas se o produto está ativo e há quantidade suficiente.
-- O UPDATE condicional impede saldo negativo em compras concorrentes.
CREATE OR REPLACE PROCEDURE reservar_estoque(
    p_produto bigint, p_qtd integer)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_qtd IS NULL OR p_qtd <= 0 THEN
        RAISE EXCEPTION 'Quantidade invalida';
    END IF;
    UPDATE produtos SET estoque = estoque - p_qtd
    WHERE id = p_produto AND ativo = true
      AND estoque >= p_qtd;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Produto indisponivel ou sem estoque';
    END IF;
END;
$$;

-- Executada apenas pela API administrativa.
CREATE OR REPLACE PROCEDURE alterar_preco(
    p_produto bigint, p_preco numeric)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_preco IS NULL OR p_preco <= 0 THEN
        RAISE EXCEPTION 'Preco invalido';
    END IF;
    UPDATE produtos SET preco = p_preco
    WHERE id = p_produto;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Produto nao encontrado';
    END IF;
END;
$$;

-- Devolve ao estoque os itens de um pedido cancelado.
CREATE OR REPLACE PROCEDURE cancelar_pedido(p_pedido bigint)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE pedidos SET status = 'cancelado', cancelado_em = now()
    WHERE id = p_pedido AND status IN ('aberto', 'aguardando_pagamento');
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Pedido inexistente ou ja pago/enviado';
    END IF;
    UPDATE produtos pr SET estoque = pr.estoque + i.qtd
    FROM (SELECT produto_id, SUM(quantidade) AS qtd
          FROM itens_pedido WHERE pedido_id = p_pedido
          GROUP BY produto_id) i
    WHERE pr.id = i.produto_id;
END;
$$;

-- Mantém pedidos.subtotal igual à soma dos itens.
CREATE OR REPLACE FUNCTION recalcular_subtotal_pedido() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_pedido bigint := COALESCE(NEW.pedido_id, OLD.pedido_id);
BEGIN
    UPDATE pedidos SET subtotal = COALESCE(
        (SELECT SUM(quantidade * preco_unitario)
         FROM itens_pedido WHERE pedido_id = v_pedido), 0)
    WHERE id = v_pedido;
    IF TG_OP = 'UPDATE' AND OLD.pedido_id <> NEW.pedido_id THEN
        UPDATE pedidos SET subtotal = COALESCE(
            (SELECT SUM(quantidade * preco_unitario)
             FROM itens_pedido WHERE pedido_id = OLD.pedido_id), 0)
        WHERE id = OLD.pedido_id;
    END IF;
    RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS tg_itens_subtotal ON itens_pedido;
CREATE TRIGGER tg_itens_subtotal
    AFTER INSERT OR UPDATE OR DELETE ON itens_pedido
    FOR EACH ROW EXECUTE FUNCTION recalcular_subtotal_pedido();

COMMIT;
