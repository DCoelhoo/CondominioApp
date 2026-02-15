from controllers.config_manager import carregar_config
from controllers.data_manager import guardar_dados

def lancar_quota_mensal(moradores, ano: int, mes: int):
    config = carregar_config()
    quota_base = float(config.get("quota_base", 0.0))
    extra_garagem = float(config.get("extra_garagem", 0.0))

    data_lancamento = f"{ano}-{mes:02d}-01"
    descricao = f"Quota {mes:02d}/{ano}"

    adicionadas = 0
    ignoradas = 0

    for m in moradores:
        m.setdefault("tem_garagem", False)
        m.setdefault("transacoes", [])
        m.setdefault("saldo", 0.0)

        # evita duplicar (por morador)
        if any(t.get("descricao") == descricao for t in m["transacoes"]):
            ignoradas += 1
            continue

        valor = quota_base + (extra_garagem if m["tem_garagem"] else 0.0)
        valor = -abs(valor)  # despesa

        m["transacoes"].append({
            "data": data_lancamento,
            "tipo": "despesa",
            "valor": valor,
            "descricao": descricao
        })

        m["saldo"] += valor
        adicionadas += 1

    guardar_dados(moradores)
    return adicionadas, ignoradas
