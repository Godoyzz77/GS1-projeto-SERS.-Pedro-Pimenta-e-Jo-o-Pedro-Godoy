"use strict";
const modelo = JSON.parse(document.querySelector("#dados").textContent);
const porId = (id) => document.getElementById(id);
const f = (n, casas = 2) => n === null ? "n/a" : n.toLocaleString("pt-BR",{minimumFractionDigits:casas,maximumFractionDigits:casas});
const grana = (n) => "R$ " + f(n);
const entradas = Object.fromEntries(modelo.premissas.map(linha => [linha.id, Number(linha.valor)]));
const nomes = {base:"Referência", led:"A · LED", solar:"B · Solar"};
function el(tag, texto, classe) {
  const n = document.createElement(tag);
  if (texto !== undefined) n.textContent = texto;
  if (classe) n.className = classe;
  return n;
}
function tabela(alvo, colunas, linhas, destaque = -1) {
  const head = document.createElement("thead");
  const tr = document.createElement("tr");
  colunas.forEach((valor, i) => {
    const celula = el("th",valor, i === destaque ? "ativo-col" : "");
    celula.scope="col"; tr.append(celula);
  });
  head.append(tr);
  const corpo = document.createElement("tbody");
  linhas.forEach(linha => {
    const r = document.createElement("tr");
    linha.forEach((valor,i) => r.append(el("td",valor, i === destaque ? "ativo-col" : "")));
    corpo.append(r);
  });
  porId(alvo).replaceChildren(head,corpo);
}
function barras(periodo) {
  const area = porId("barras"); area.replaceChildren();
  const max = Math.max(...Object.values(modelo.resultados).map(x => x[periodo].consumo),1);
  const unidade = periodo === "mes" ? "kWh/mês" : "kWh/ano";
  porId("unidade-fluxo").textContent = unidade;
  Object.entries(modelo.resultados).forEach(([id,r]) => {
    const a = r[periodo], linha = el("div", undefined,"barrow");
    const rotulo = el("div", undefined,"barlabel");
    rotulo.append(el("span",nomes[id]),el("strong",f(a.consumo) + " kWh"));
    const trilha = el("div",undefined,"track");
    ["rede","solar"].forEach(chave => {
      const b = el("i",undefined,chave === "rede" ? "rede" : "fv");
      b.style.width = Math.max(0, Math.min(100,100*a[chave]/max))+"%";
      trilha.append(b);
    });
    linha.setAttribute("aria-label",nomes[id]+", rede "+f(a.rede)+" e solar "+f(a.solar)+" "+unidade);
    linha.append(rotulo,trilha); area.append(linha);
  });
}
function perfil(dia) {
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns,"svg");
  svg.setAttribute("viewBox","0 0 800 162"); svg.setAttribute("role","img");
  svg.setAttribute("aria-label","Energia da rede e solar por hora. Dados completos na tabela a seguir.");
  const max = Math.max(0.001,...dia.map(h=>h.consumo));
  function desenho(tag, attrs, txt) {
    const componente = document.createElementNS(ns,tag);
    Object.entries(attrs).forEach(([k,v]) => componente.setAttribute(k,v));
    if(txt !== undefined) componente.textContent=txt;
    svg.append(componente);
  }
  [0,0.5,1].forEach(frac=>{
    const y=127-93*frac;
    desenho("line",{x1:48,x2:789,y1:y,y2:y,stroke:"#d5dfd2"});
    desenho("text",{x:43,y:y+4,"text-anchor":"end","font-size":11,fill:"#496256"},f(max*frac));
  });
  dia.forEach(h=>{
    const x=51+h.hora*30.7, rede=93*h.rede/max, solar=93*h.solar/max;
    desenho("rect",{x,y:127-rede,width:23,height:rede,fill:"#286b54"});
    desenho("rect",{x,y:127-rede-solar,width:23,height:solar,fill:"#e7b540"});
    if(h.hora%3===0) desenho("text",{x:x+11,y:148,"text-anchor":"middle","font-size":11,fill:"#496256"},String(h.hora).padStart(2,"0")+"h");
  });
  porId("perfil").replaceChildren(svg);
  tabela("horas",["Hora","Carga (kWh)","Rede (kWh)","Solar usada (kWh)","Geração (kWh)","Excedente (kWh)"],dia.map(h=>[String(h.hora).padStart(2,"0")+"h",...["consumo","rede","solar","geracao","excedente"].map(k=>f(h[k],3))]));
}
function atualizar() {
  const id=porId("escolha").value, per=porId("periodo").value;
  const r=modelo.resultados[id], a=r[per], un=per==="mes"?"mês médio":"ano";
  const blocos = [
    ["Consumo final",f(a.consumo),"kWh / "+un],["Energia da rede",f(a.rede),"kWh / "+un],
    ["Redução da conta",grana(a.economia_conta),"por "+un],["Participação solar",f(r.participacao)+"%","da carga atendida"]
  ];
  porId("kpis").replaceChildren(...blocos.map(([nome,valor,unidade])=>{
    const item=el("div",undefined,"kpi");item.append(el("span",nome),el("strong",valor),el("small",unidade));return item;
  }));
  const leitura={
    base:f(entradas.tubos_base,0)+" tubos fluorescentes e seus reatores compõem a referência simulada. A rede atende toda a iluminação durante o atendimento cadastrado.",
    led:"A troca dos tubos reduz o consumo projetado em "+f(r.reducao,1)+"%. Antes da ampliação, compare a luz na rampa, na circulação e no rótulo do coletor.",
    solar:"A geração projetada é de "+f(a.geracao)+" kWh no período. O circuito usa "+f(a.solar)+" kWh e o excedente de "+f(a.excedente)+" kWh fica sem crédito no modelo. A rede complementa a iluminação."
  };
  porId("titulo-caso").textContent=r.nome;porId("leitura").textContent=leitura[id];
  porId("custo").textContent="Investimento adicional de "+grana(r.capex)+". Operação com manutenção de "+grana(r.ano.operacao)+" por ano.";
  const metricas=[["Consumo final (kWh)","consumo"],["Compra da rede (kWh)","rede"],["Geração solar (kWh)","geracao"],["Solar usada (kWh)","solar"],["Excedente (kWh)","excedente"],["Economia de consumo (kWh)","economia_consumo"],["Parcela variável (R$)","conta"],["Economia da conta (R$)","economia_conta"],["Operação com manutenção (R$)","operacao"]];
  const alternativas=Object.values(modelo.resultados);
  const linhas=metricas.map(([lab,k])=>[lab,...alternativas.map(x=>f(x[per][k]))]);
  linhas.push(["Participação solar (%)",...alternativas.map(x=>f(x.participacao))],["Investimento inicial (R$)",...alternativas.map(x=>f(x.capex))]);
  tabela("comparacao",["Indicador · "+un,...Object.values(nomes)],linhas,Object.keys(nomes).indexOf(id)+1);
  barras(per); perfil(r.dia);
}
function iniciar() {
  porId("bairro").textContent=modelo.ponto.bairro;porId("horario").textContent=modelo.ponto.horario;porId("status").textContent=modelo.ponto.id+" · "+modelo.ponto.status;
  tabela("premissas",["Premissa","Valor","Unidade","Origem","Fundamento"],modelo.premissas.map(x=>[x.descricao,String(x.valor).replace(".",","),x.unidade,x.origem+" · "+x.fonte,x.justificativa]));
  tabela("sens",["Teste","Rede (kWh/mês)","Investimento (R$)","Economia líquida (R$/ano)","Retorno (anos)"],modelo.sensibilidade.map(x=>[x.nome,f(x.rede),f(x.capex),f(x.liquida),f(x.retorno)]));
  modelo.fontes.forEach(s=>{
    const d=el("div",undefined,"source"); d.append(el("strong",s.id+" · "+s.autor),el("p",s.documento),el("small",s.nota));
    if(s.localizador.startsWith("https://")) {const link=el("a","Consultar fonte ↗");link.href=s.localizador;link.target="_blank";link.rel="noopener";d.append(link);}
    else d.append(el("small",s.localizador)); porId("fontes").append(d);
  });
  function navegar() {
    const id=["inicio","energia","metodo"].includes(location.hash.slice(1)) ? location.hash.slice(1) : "inicio";
    document.querySelectorAll(".view").forEach(v=>v.classList.toggle("aberta",v.id===id));
    document.querySelectorAll("nav a").forEach(a=>{if(a.hash==="#"+id)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});
    window.scrollTo(0,0);
  }
  porId("escolha").addEventListener("change",atualizar);porId("periodo").addEventListener("change",atualizar);window.addEventListener("hashchange",navegar);
  atualizar();navegar();
}
iniciar();
