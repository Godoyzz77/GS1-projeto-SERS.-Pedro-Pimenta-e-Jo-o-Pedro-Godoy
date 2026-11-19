# Indicadores e integração

Cada valor exibido é uma projeção do cenário. O cadastro do Ponto do Tear é simulado. Fontes publicadas descrevem equipamentos, preços de referência, irradiação e tarifa. A instalação no local permanece uma hipótese. O diagrama destaca o medidor que uma implantação futura poderia utilizar.

| Indicador | Cálculo e entradas principais | Referência / LED / solar no mês médio | Onde aparece e como aferir em operação |
|---|---|---|---|
| Consumo final, kWh/mês | Quantidade × potência de entrada × horas × dias ÷ 1.000. Base e B incluem a perda do reator | 165,47 / 66,19 / 165,47 | Cartão “Consumo final” e tabela. Registrar diariamente o submedidor do circuito e comparar meses de mesmo uso |
| Compra da rede, kWh/mês | Soma por minuto de carga menos solar usada. Entradas de carga, curva solar e desempenho | 165,47 / 66,19 / 75,21 | Cartão “Energia da rede”, barras e perfil diário. Cruzar medidor do circuito e leituras simultâneas da produção e dos fluxos no mesmo ponto |
| Redução da parcela variável da conta, R$/mês | (Compra da referência − compra da alternativa) × (TUSD + TE) ÷ 1.000, com tarifas em R$/MWh | 0,00 / 78,37 / 71,24 | Cartão “Redução da conta” e tabela. Conferir fatura, classe, tarifa e dias de leitura. Separar variações das demais cargas |
| Participação solar local, % | 100 × solar usada no circuito ÷ consumo final. Excedente fora do numerador | 0,00 / 0,00 / 54,54 | Cartão “Participação solar” e tabela. Sincronizar dados do microinversor e do submedidor. Somar só a energia efetivamente atendida no instante |
| Economia por eficiência, kWh/mês | Consumo final da referência − consumo final da alternativa | 0,00 / 99,28 / 0,00 | Tabela “Economia de consumo”. Comparar circuitos ou períodos equivalentes, com a mesma luz útil e horário |
| Horário de atendimento e qualidade da luz | 06h–23h mantido nos cenários. Luz útil exige verificação com luxímetro e equipe local | 17 h/dia nos três cenários; lux pendente de ensaio | Ficha do ponto e condição de implantação. Verificar rampa, instruções e coletor antes e depois nos mesmos pontos |

### Origem de um número da tela

Em “B · Geração solar”, o programa calcula a geração e a carga em 1.440 passos de um dia típico. Soma o menor valor de cada par para obter a energia solar usada. Ao multiplicar pelos dias de funcionamento e dividir por 12, encontra 90,25 kWh/mês médio. A divisão dessa energia pelo consumo mensal, com dados sem arredondar, produz os 54,54% do cartão. Os kWh excedentes não entram nesse cálculo.

### Integrar ao Neighborhood Action Dashboard

A tela inicial já utiliza a ficha do cadastro original FZC-001 e contém um acesso direto à seção **Energia**. A navegação interna, os filtros de cenário e de período e o acesso a **Método e fontes** funcionam no HTML entregue. Esta é uma implementação local do painel do projeto, construída sobre o recorte real do arquivo do grupo. O grupo não forneceu o código ou URL de outro painel publicado.

- Para integrar a um site existente, copie o HTML completo para uma rota ou pasta de SERS e acrescente uma ligação para `index.html#energia`. A página é autossuficiente e lê um espelho do JSON de cálculo que foi incorporado na geração do arquivo.
- Se o projeto tiver frontend próprio, utilize `dados/resultados.json`. A raiz traz `ponto`, `tarifa`, `resultados`, `premissas`, `fontes`, `sensibilidade`, `dias` e `horas`. Vincule a ficha por `ponto.id` ao cadastro maior, mantendo o status do serviço original.
- Cada alternativa (`base`, `led`, `solar`) contém `mes`, `ano`, `dia`, `participacao`, `reducao`, `capex` e `retorno`. Nos objetos de período, `consumo`, `rede`, `geracao`, `solar` e `excedente` estão em kWh. `conta`, `manutencao`, `operacao`, `economia_conta` e `economia_liquida` estão em R$. `participacao` e `reducao` já estão em %, `capex` em R$ e `retorno` em anos. Um denominador zero ou retorno indefinido gera JSON null. O perfil `dia` possui 24 intervalos com hora inicial e fluxos em kWh. `kw` indica a potência da carga ligada.
- Depois de editar premissas e executar o cálculo, substitua o HTML/JSON na aplicação que o hospeda. Confirme que o mesmo identificador, período e alternativa aparecem nas duas aplicações. A integração com eventual site remoto da equipe requer acesso ao repositório dele.
