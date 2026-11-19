"""Conferências independentes do modelo, do caso didático e dos arquivos gerados."""
import json
import math
import re
from decimal import Decimal

from calcular import DADOS, PASTA, calcular, ler_csv, tabela, validar


def perto(a, b, tolerancia=1e-7):
    if not math.isclose(a, b, rel_tol=1e-10, abs_tol=tolerancia):
        raise AssertionError(f"Valores diferentes: {a:.9f} e {b:.9f}")


def solar_continua(p, carga):
    """Integral exata da curva triangular, cortada pela janela de uso e pela carga."""
    inicio, fim = p["hora_sol_inicio"], p["hora_sol_fim"]
    meio = (inicio + fim) / 2
    energia = p["n_modulos"] * p["w_modulo"] / 1000 * p["hsp"] * p["desempenho"]
    pico = 2 * energia / (fim - inicio)
    if not pico:
        return 0.0
    fracao = min(1, carga / pico)
    limites = sorted({inicio, inicio + (meio - inicio) * fracao, meio,
                      fim - (fim - meio) * fracao, fim, p["hora_abre"], p["hora_fecha"]})
    total = 0.0
    for a, b in zip(limites, limites[1:]):
        if a >= p["hora_abre"] and b <= p["hora_fecha"]:
            def usada(t):
                return min(carga, max(0.0, pico * (1 - abs(t - meio)/(meio - inicio))))
            total += (b-a) * (usada(a) + usada(b)) / 2
    return total


def microteste(p):
    # Um dia contínuo de carga; a geração de 40 kWh tem pico inferior à carga da base.
    exemplo = {**p, "dias_ano": 365, "hora_abre": 0, "hora_fecha": 24, "hora_sol_inicio": 0,
               "hora_sol_fim": 24, "n_modulos": 1, "desempenho": 1, "hsp": 8, "w_modulo": 5000,
               "tubos_base": 1, "pot_base": 100 * 1000 / 24, "perda_reator": 0,
               "tubos_led": 1, "pot_led": 60 * 1000 / 24}
    r = calcular(exemplo)
    # Reescala o dia de teste para um mês didático com saldo 100 / 60 / 40.
    for chave, carga, rede, economia in (("base",100,100,0),("led",60,60,40),("solar",100,60,0)):
        for campo, valor in (("consumo",carga),("rede",rede),("economia_consumo",economia)):
            perto(r[chave]["ano"][campo] / 365, valor)


def main():
    dados = json.loads((DADOS / "resultados.json").read_text(encoding="utf-8"))
    linhas = ler_csv("premissas.csv")
    p = {l["id"]:float(l["valor"]) for l in linhas}
    validar(p, dados["ponto"])
    r = calcular(p)
    assert r == dados["resultados"], "Rode calcular.py, o JSON diverge das entradas."
    dec = {l["id"]:Decimal(l["valor"]) for l in linhas}
    horas = dec["hora_fecha"] - dec["hora_abre"]
    energia_tubo = (dec["pot_base"] + dec["perda_reator"]) * horas / 1000
    base = energia_tubo * dec["tubos_base"] * dec["dias_ano"]
    led = dec["pot_led"] * dec["tubos_led"] * horas * dec["dias_ano"] / 1000
    perto(float(base),r["base"]["ano"]["consumo"])
    perto(float(base-led),r["led"]["ano"]["economia_consumo"])
    tarifa = (dec["tusd"] + dec["te"]) / 1000
    perto(float((base-led)*tarifa/12), r["led"]["mes"]["economia_conta"])
    diario = solar_continua(p,r["solar"]["kw"])
    solar_modelo = r["solar"]["ano"]["solar"] / p["dias_ano"]
    perto(diario,solar_modelo,0.0001)
    for x in r.values():
        for periodo in ("mes","ano"):
            z=x[periodo]
            perto(z["rede"] + z["solar"], z["consumo"])
            perto(z["solar"] + z["excedente"], z["geracao"])
            assert min(z[k] for k in ("rede","consumo","solar","excedente","geracao")) >= -1e-9
        if x["participacao"] is not None:
            assert 0 <= x["participacao"] <= 100.000001
    microteste(p)
    zero = calcular({**p,"tubos_base":0,"tubos_led":0})
    assert zero["base"]["reducao"] is None and zero["solar"]["participacao"] is None
    alterado = calcular({**p,"pot_led":p["pot_led"] + 1})
    esperado = p["tubos_led"] * float(horas) * p["dias_ano"] / 1000
    perto(alterado["led"]["ano"]["consumo"] - r["led"]["ano"]["consumo"],esperado)
    html=(PASTA/"index.html").read_text(encoding="utf-8")
    jsdados = re.search(r'<script type="application/json" id="dados">(.*?)</script>', html, re.S)
    assert jsdados and json.loads(jsdados.group(1)) == dados
    assert tabela(r) in (PASTA/"README.md").read_text(encoding="utf-8")
    print("OK: entradas, cálculo decimal, balanços, microteste, base zero, sensibilidade, README e painel.")
    print(f"Diferença do solar entre integração contínua e por minuto: {abs(diario-solar_modelo):.8f} kWh/dia.")
    print("O teste de potência foi feito em memória; o cenário-base foi preservado.")


if __name__ == "__main__":
    main()
