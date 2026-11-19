# Memória de cálculo e decisão

## Escopo do serviço

O recorte cobre a iluminação do atendimento de óleo usado no Ponto do Tear. O cadastro do integrador fornece o ponto, a rampa mencionada no relato e o horário. Oito tubos divididos entre quatro trechos, iluminação ligada durante as 17 horas e funcionamento nos 365 dias são hipóteses de estudo. “Atual” descreve uma **referência simulada**. A área exata, iluminância, distribuição de luminárias, perfil de usuários, frequência de visitas e ligação B3 dependem de levantamento. O horário cadastrado indica atendimento; a luz artificial durante todo esse tempo é uma hipótese a conferir.

## Inventário do cenário central

| Equipamento | Quantidade | Potência por unidade | Horas/dia | Energia/dia | Mês médio | Ano |
|---|---:|---:|---:|---:|---:|---:|
| Tubos fluorescentes, base e B | 8 | 36 W [S2] | 17 | 4,896 kWh | 148,92 kWh | 1.787,04 kWh |
| Parcela de perda dos reatores, base e B | 8 equivalentes | 4 W [H] | 17 | 0,544 kWh | 16,55 kWh | 198,56 kWh |
| Circuito completo, base e B | — | 320 W no total | 17 | 5,440 kWh | 165,47 kWh | 1.985,60 kWh |
| LED de ligação direta, A | 8 | 16 W [S3] | 17 | 2,176 kWh | 66,19 kWh | 794,24 kWh |

As três primeiras linhas decompõem o mesmo circuito. Somar a linha de total aos seus dois componentes duplicaria o consumo. Cada kW descreve potência num instante. Um kWh é a energia utilizada por uma potência de um kW mantida por uma hora. O mês médio corresponde a 365 ÷ 12 dias; um mês de calendário específico pode ser diferente.

**Conta que se pode fazer à mão.** Um tubo de referência com a parcela do reator usa (36 + 4) × 17 ÷ 1.000 = 0,680 kWh/dia. Oito conjuntos usam 5,440 kWh/dia. No ano, 5,440 × 365 = 1.985,60 kWh. Na alternativa A, 8 × 16 × 17 × 365 ÷ 1.000 = 794,24 kWh. A diferença de 1.191,36 kWh/ano representa 60,00% da referência ou 99,28 kWh/mês médio.

## Como foi calculada a opção solar

O kit [S6] tem dois módulos de 590 Wp, totalizando 1,18 kWp, e microinversor de placa de potência superior a essa potência DC. O atlas paulista [S5] fornece 4,589 kWh/m²/dia de radiação global média para São Paulo. Dividir esse valor pela irradiância de referência de 1 kW/m² fornece 4,589 horas de sol pleno. São Paulo é um local de referência para o município fictício. A área de telhado, a inclinação, a orientação e as sombras reais ainda precisariam ser verificadas. Usa-se uma aproximação em plano horizontal e um fator de desempenho hipotético de 0,78 que agrupa perdas elétricas, térmicas e de conversão.

- **Energia solar produzida no dia médio** = 1,18 × 4,589 × 0,78 = 4,2237156 kWh/dia. É a energia estimada já após o fator de desempenho.
- **Distribuição no tempo**. Entre 06h e 18h a potência solar simulada cresce linearmente até o meio-dia e depois decresce até zero. A área desse triângulo reproduz a geração do dia. Potência de pico do dia médio = 2 × 4,2237156 ÷ 12 ≈ 0,704 kW. Às 12h, o circuito demanda 0,320 kW. A parte que excede a carga no intervalo não evita uma segunda compra de energia.
- **Coincidência**. Em cada minuto, a parcela usada é o menor valor entre carga e geração. Compra da rede = carga − solar usada. Excedente = geração − solar usada. Às 20h a geração é zero e a iluminação fica por conta da rede. O programa soma os minutos por hora, dia e ano.
- **Resultado no mês médio**. Geração de 128,47 kWh, dos quais 90,25 kWh atendem diretamente o circuito. Restam 38,22 kWh fora desse consumo. A rede fornece 75,21 kWh. A participação solar é 54,54% do consumo total do circuito. A divisão usa valores sem arredondamento.
- **Fronteira**. Não há bateria. O modelo não dá ao excedente receita ou crédito tarifário. Ele poderia atender outras cargas do imóvel ou ser injetado/limitado conforme o arranjo autorizado. Isso precisaria de estudo do prédio inteiro. A energia solar projetada não torna o ponto independente da rede, inclusive em interrupções.

O mesmo dia representativo é repetido ao longo do ano. Isso simplifica sazonalidade, chuva, sombras e simultaneidade. A curva por minuto resolve o balanço dentro do cenário; granularidade por minuto não significa qualidade de medição por minuto. Uma série horária local de carga e irradiação melhoraria a estimativa.

## Custos em reais de referência de 13/11/2026

A tarifa usada é (472,42 + 316,96) ÷ 1.000 = **R$ 0,78938/kWh**, TUSD + TE da modalidade convencional B3 da Enel SP [S4]. A hipótese é que o pátio integre uma instalação em baixa tensão nessa modalidade e a variação marginal de consumo afete a parcela volumétrica. O cálculo exclui tributos, bandeiras adicionais, demanda contratada, contribuição de iluminação pública, custo mínimo de disponibilidade e componentes fixos da fatura. Verificar a conta do prédio e se o mínimo interfere na economia antes de decidir.

| Componente | Base | A · LED | B · Solar | Fundamento |
|---|---:|---:|---:|---|
| Material principal | R$ 0,00 | 8 × R$ 32,99 = R$ 263,92 | 1 kit × R$ 2.759,00 | Ativos existentes na base. Referências comerciais S7 e S6, sujeitas a alteração |
| Instalação e serviços | R$ 0,00 | 8 × R$ 30,00 = R$ 240,00 | R$ 1.000,00 | Provisões H. Solicitar cotação de adaptação, instalação e regularização |
| Complementos e logística | R$ 0,00 | R$ 80,00 | R$ 500,00 | H. Retirada/destinação do lote A. Estrutura, proteção e transporte de B |
| Investimento total incremental | **R$ 0,00** | **R$ 583,92** | **R$ 4.259,00** | Soma acima, sem financiamento |
| Energia variável anual | R$ 1.567,39 | R$ 626,96 | R$ 712,47 | kWh da rede × tarifa |
| Manutenção e reposição rotineira anual | R$ 120,00 | R$ 60,00 | R$ 240,00 | Provisão H. B mantém a reserva dos tubos e acrescenta R$ 120,00 para o sistema solar |
| Operação anual total | R$ 1.687,39 | R$ 686,96 | R$ 952,47 | Energia + manutenção |

O investimento é pago uma vez. A economia anual na parcela variável da conta é R$ 940,44 (A) ou R$ 854,93 (B). Ao considerar a mudança de manutenção, a economia operacional líquida anual fica em R$ 1.000,44 ou R$ 734,93. Os retornos simples indicativos são 0,58 ano e 5,80 anos. Para esse indicador, supõe-se repetição do ano-modelo a preços constantes. Inflação, juros, degradação e reposições extraordinárias ficam fora dessa projeção. Em particular, a eventual troca antecipada do inversor pode aumentar o prazo real. O fornecedor do LED exibe discrepância de SKU entre o título e um campo secundário; confirmar a peça e o valor antes de adquirir.

## Escolha e condições em que muda

Para a gestão do Ponto do Tear, o objetivo considerado é conservar o atendimento com baixo investimento inicial e reduzir o custo de operação. No cenário central, o LED custa R$ 3.675,08 a menos para implantar e proporciona economia líquida anual superior. A proposta solar continua relevante quando a gestão prioriza geração local ou consegue aproveitar o excedente com outras cargas.

**Um teste que pode mudar a escolha.** O tubo de referência tem cerca de 36 × 90 = 3.240 lm por lâmpada pelas especificações nominais [S2]. O LED proposto tem 2.100 lm [S3]. O fabricante o indica como alternativa ao de 36 W. Distribuição de luz e geometria do local influenciam o que chega ao piso. Antes da compra, comparar iluminância média e mínima em uma malha de pontos na rampa, passagem e coletor, nos mesmos horários e condições de luz natural. Conferir ofuscamento, leitura das instruções e critérios aplicáveis com o responsável técnico. Se o piloto não preservar a luz útil, revisar o arranjo.

| Hipótese alternativa | Rede no mês médio | Investimento | Economia operacional líquida/ano | Retorno simples |
|---|---:|---:|---:|---:|
| A, necessidade de 12 LEDs | 99,28 kWh | R$ 835,88 | R$ 686,96 | 1,22 ano |
| B, desempenho solar 0,65 | 80,52 kWh | R$ 4.259,00 | R$ 684,63 | 6,22 anos |
| B, desempenho solar 0,85 | 73,03 kWh | R$ 4.259,00 | R$ 755,63 | 5,64 anos |

Com 12 LEDs, A ainda exige menos investimento e tem retorno mais curto. B no desempenho central passa a poupar mais por ano em operação (R$ 734,93 contra R$ 686,96). A quantidade de 12 constitui um teste de sensibilidade; também requer confirmação de espaço e iluminação. O teste mantém a reserva de manutenção de A fixa, por ser uma provisão do conjunto. Não se estimou redução de CO₂e sem caracterizar o fator de emissão. A participação solar e os kWh poupados são os indicadores ambientais quantificáveis.

## Rastrear e atualizar

As referências S1–S7 e suas datas de consulta estão em [fontes.csv](../dados/fontes.csv). Os quantitativos, potências, tarifas e hipóteses com origem rotulada estão em [premissas.csv](../dados/premissas.csv). O script atualiza os arquivos de resultados, a tabela central do README e o dashboard. Os exemplos deste memorial e as falas do roteiro registram o cenário de 13/11/2026. Atualize os textos narrativos se a equipe mudar entradas.
