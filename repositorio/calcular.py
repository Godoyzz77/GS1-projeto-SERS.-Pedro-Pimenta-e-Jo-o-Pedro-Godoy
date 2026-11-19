"""Recalcula o cenário SERS e monta o painel. Só utiliza a biblioteca padrão."""
import csv
import json
import math
from pathlib import Path

PASTA = Path(__file__).resolve().parent
DADOS = PASTA / "dados"


def ler_csv(nome):
    with (DADOS / nome).open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def validar(p, ponto):
    if any(not math.isfinite(v) or v < 0 for v in p.values()):
        raise ValueError("Use números finitos e não negativos nas premissas.")
    for chave in ("tubos_base", "tubos_led", "n_modulos", "dias_ano"):
        if not p[chave].is_integer():
            raise ValueError(f"{chave} deve ser um inteiro.")
    if not 0 < p["dias_ano"] <= 365 or not 0 <= p["desempenho"] <= 1:
        raise ValueError("Confira os dias anuais de operação e o fator de desempenho.")
    for inicio, fim in (("hora_abre", "hora_fecha"), ("hora_sol_inicio", "hora_sol_fim")):
        if not 0 <= p[inicio] < p[fim] <= 24:
            raise ValueError("O início deve anteceder o fim no dia modelado.")
    horario = f'{int(p["hora_abre"]):02d}:00–{int(p["hora_fecha"]):02d}:00'
    if not p["hora_abre"].is_integer() or not p["hora_fecha"].is_integer() or horario != ponto["horario"]:
        raise ValueError("Confira o horário em horas inteiras com o cadastro do Ponto do Tear.")


def simular_dia(carga_kw, geracao_dia, p):
    """Integra um dia médio em minutos; a área do triângulo solar é a energia diária."""
    sol_inicio, sol_fim = p["hora_sol_inicio"], p["hora_sol_fim"]
    meio = (sol_inicio + sol_fim) / 2
    meia_largura = (sol_fim - sol_inicio) / 2
    pico_kw = geracao_dia / meia_largura
    horas = [dict(hora=h, consumo=0.0, geracao=0.0, solar=0.0, rede=0.0, excedente=0.0) for h in range(24)]
    for minuto in range(24 * 60):
        t = (minuto + 0.5) / 60
        consumo = carga_kw / 60 if p["hora_abre"] <= t < p["hora_fecha"] else 0
        fv = pico_kw * max(0, 1 - abs(t - meio) / meia_largura) / 60
        uso_solar = min(consumo, fv)
        hora = horas[minuto // 60]
        hora["consumo"] += consumo
        hora["geracao"] += fv
        hora["solar"] += uso_solar
        hora["rede"] += consumo - uso_solar
        hora["excedente"] += fv - uso_solar
    return horas


def calcular(p):
    tarifa = (p["tusd"] + p["te"]) / 1000
    potencia_base = p["tubos_base"] * (p["pot_base"] + p["perda_reator"]) / 1000
    potencia_led = p["tubos_led"] * p["pot_led"] / 1000
    kwp = p["n_modulos"] * p["w_modulo"] / 1000
    geracao_dia = kwp * p["hsp"] * p["desempenho"]
    capex_led = p["tubos_led"] * (p["preco_led"] + p["mao_led"]) + p["lote_led"]
    capex_fv = p["kit_fv"] + p["inst_fv"] + p["acess_fv"]
    modelos = [
        ("base", "Situação de referência", potencia_base, 0, 0, p["reserva_base"]),
        ("led", "Troca por LED", potencia_led, 0, capex_led, p["reserva_led"]),
        ("solar", "Geração solar", potencia_base, geracao_dia, capex_fv, p["reserva_base"] + p["reserva_fv"]),
    ]
    resultados = {}
    for chave, nome, potencia, geracao, investimento, manutencao in modelos:
        perfil = simular_dia(potencia, geracao, p)
        anual = {}
        for fluxo in ("consumo", "geracao", "solar", "rede", "excedente"):
            diaria = sum(h[fluxo] for h in perfil)
            anual[fluxo] = diaria * p["dias_ano"]
        # Nos dias de fechamento só o gerador continua ativo; toda a produção fica fora do circuito.
        fv_fechado = (365 - p["dias_ano"]) * geracao
        anual["geracao"] += fv_fechado
        anual["excedente"] += fv_fechado
        anual["conta"] = anual["rede"] * tarifa
        anual["manutencao"] = manutencao
        anual["operacao"] = anual["conta"] + manutencao
        base = resultados["base"]["ano"] if "base" in resultados else anual
        for metrica, original in (("economia_consumo", "consumo"), ("rede_evitada", "rede"), ("economia_conta", "conta"), ("economia_liquida", "operacao")):
            anual[metrica] = base[original] - anual[original]
        mensal = {campo: valor / 12 for campo, valor in anual.items()}
        participacao = 100 * anual["solar"] / anual["consumo"] if anual["consumo"] else None
        reducao = 100 * anual["economia_consumo"] / base["consumo"] if base["consumo"] else None
        retorno = investimento / anual["economia_liquida"] if investimento and anual["economia_liquida"] > 0 else None
        resultados[chave] = dict(nome=nome, kw=potencia, ano=anual, mes=mensal, dia=perfil,
                                  participacao=participacao, reducao=reducao, capex=investimento, retorno=retorno)
    return resultados


def br(valor, casas=2):
    if valor is None:
        return "n/a"
    return format(valor, f",.{casas}f").translate(str.maketrans(".,", ",."))


def tabela(resultados):
    linhas = ["| Indicador | Referência | A · LED | B · Solar |", "|---|---:|---:|---:|"]
    for titulo, grupo, chave in [
        ("Consumo final (kWh/mês médio)", "mes", "consumo"), ("Energia da rede (kWh/mês médio)", "mes", "rede"),
        ("Geração fotovoltaica (kWh/mês médio)", "mes", "geracao"), ("Solar usada no circuito (kWh/mês médio)", "mes", "solar"),
        ("Excedente fora do circuito (kWh/mês médio)", "mes", "excedente"), ("Parcela variável (R$/mês médio)", "mes", "conta"),
        ("Redução da conta variável (R$/mês médio)", "mes", "economia_conta"), ("Consumo (kWh/ano)", "ano", "consumo"),
        ("Redução de consumo (%)", "", "reducao"), ("Participação solar no circuito (%)", "", "participacao"),
        ("Investimento incremental (R$)", "", "capex"), ("Manutenção provisionada (R$/ano)", "ano", "manutencao"),
        ("Operação, energia + manutenção (R$/ano)", "ano", "operacao"), ("Economia operacional líquida (R$/ano)", "ano", "economia_liquida"),
        ("Retorno simples (anos)", "", "retorno")]:
        valores = [br((r[grupo] if grupo else r)[chave]) for r in resultados.values()]
        linhas.append("| " + " | ".join([titulo] + valores) + " |")
    return "\n".join(linhas)


def atualizar_readme(texto):
    inicio, fim = "<!-- resultados:inicio -->", "<!-- resultados:fim -->"
    caminho = PASTA / "README.md"
    atual = caminho.read_text(encoding="utf-8")
    antes, resto = atual.split(inicio)
    _, depois = resto.split(fim)
    caminho.write_text(antes + inicio + "\n\n" + texto + "\n\n" + fim + depois, encoding="utf-8")


def main():
    entradas = ler_csv("premissas.csv")
    p = {linha["id"]: float(linha["valor"]) for linha in entradas}
    if len(p) != len(entradas):
        raise ValueError("Cada premissa deve ter um ID único.")
    ponto = json.loads((DADOS / "ponto_tear.json").read_text(encoding="utf-8"))
    validar(p, ponto)
    resultados = calcular(p)
    cenarios = []
    for nome, valores in [
        ("Piloto com 12 LEDs", {"tubos_led": 12.0}),
        ("Solar com desempenho 0,65", {"desempenho": 0.65}),
        ("Solar com desempenho 0,85", {"desempenho": 0.85})]:
        alternativo = calcular({**p, **valores})
        item = alternativo["led" if "tubos_led" in valores else "solar"]
        cenarios.append(dict(nome=nome, rede=item["mes"]["rede"], liquida=item["ano"]["economia_liquida"],
                            capex=item["capex"], retorno=item["retorno"]))
    pacote = dict(ponto=ponto, tarifa=(p["tusd"] + p["te"]) / 1000, resultados=resultados,
                  premissas=entradas, fontes=ler_csv("fontes.csv"), sensibilidade=cenarios,
                  dias=p["dias_ano"], horas=p["hora_fecha"] - p["hora_abre"])
    bruto = json.dumps(pacote, ensure_ascii=False, indent=2, allow_nan=False)
    (DADOS / "resultados.json").write_text(bruto + "\n", encoding="utf-8")
    atualizar_readme(tabela(resultados))
    leitura = lambda nome: (PASTA / nome).read_text(encoding="utf-8")
    quadro = leitura("web/pagina.html").replace("{{CSS}}", leitura("web/estilo.css"))
    quadro = quadro.replace("{{DADOS}}", bruto.replace("<", "\\u003c")).replace("{{DIAGRAMA}}", leitura("docs/diagrama.svg")).replace("{{JS}}", leitura("web/painel.js"))
    (PASTA / "index.html").write_text(quadro, encoding="utf-8")
    print("Atualizados: dados/resultados.json, indicadores do README.md e index.html.")


if __name__ == "__main__":
    main()
