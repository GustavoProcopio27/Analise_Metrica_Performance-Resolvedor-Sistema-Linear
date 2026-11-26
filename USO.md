## Declaração de Uso de LLM

Declaramos que houve uso de ferramentas de LLM para apoio de estudo, planejamento, criação/revisão de scripts externos de medição/análise e revisão textual/documentação. As ferramentas identificadas nos registros são ChatGPT e Gemini. **O código do resolvedor se manteve inalterado**


### Uso 1 - Seleção de métricas e discussão sobre Jacobi / otimizações
* **Ferramenta:** Gemini
* **Modelo:** `Auto` (escolhe o modelo que ele considera mais adequado, logo não é possível rastrear a um modelo específico)
* **Integrantes:** Pedro, Gustavo e Pablo
* **Onde foi utilizado:** Planejamento e Estudo
* **O que foi perguntado/solicitado:** Foi perguntado quais 3 métricas ele acharia que seria interessante coletar para basear o trabalho? Seria bom que fosse algumas mais faceis de explicar, e tbm de tratar as relações com os temas especificados para as perguntas junto a um anexo enviado que envolia uma amostragem de métricas que o grupo considerou coletar (como taxa de falha de TLB, erros de paginação, erros de cache, erros de desvio, IPC, CPI). Após resposta inicial foi discutido com a IA a respeito hipóteses para o método de Jacobi e para os níveis de otimização -O0, -O3 e -O3 -march=native.
* **Avaliação da resposta:**  resposta do gemini sugeriu que as metricas seguissem 2 critérios: facilidade de explicação, e conexão clara com as perguntas orais e metódo algoritmico, Dito isso as sugestões foram que entre as métricas apresentadas mantessemos instruções e ciclos derivando o IPC, branches e branch misses derivando a taxa de erro ou acerto de branch e cache-references e cache-misses, derivando a taxa de erro ou acerto na cache. A sugestão foi aceita, e as metricas definidas foram IPC, Taxa de Erro de Desvio e Taxa de Erro de Acesso a Cache. Além disso, a discussão sobre o metódo jacobi levou a um entendimento básico do que o código-fonte realiza e de quais mudanças a otimização na compilação aplica, levando a aprender sobre otimizações como a vetorização, desdobramento de loops, e como o hardware de predição de desvio (`branch preditor`) atua

### Uso 2 - Adequação textual da tabela markdown com a especificação dos computadores no README
* **Ferramenta:**ChatGPT
* **Modelo:** 6 Instant
* **Integrantes:** Pablo, Pedro
* **Onde foi utilizado:** Revisão e adequação textual artefatos afetados: `README.md`
* **O que foi perguntado/solicitado:** Foi anexado as especificações coletadas do computador(processador, sistema operacional, versões, memória) em forma de tabela markdown e pedido para adicionar a topologia dos núcleos físicos e cpus lógicas de forma que não ficasse desorganizado.
* **Avaliação da resposta:** Reorganização inicial foi recusada. Após requisitar uma segunda versão foi aceita.

### Uso 3 - Revisão de código e adequação do regex para multiplexação no script de processamento
* **Ferramenta:** ChatGPT
* **Modelo:** 6 Instant
* **Integrantes:** Gustavo
* **Onde foi utilizado:** Scripts externos - artefatos afetados: `process_data.py`
* **O que foi perguntado/solicitado:** Foi pedido para alterar o script de processamento script, adicionando linhas de busca regex para a captura da multiplexação das métricas
* **Avaliação da resposta:** O código completo gerado foi rejeitado, após múltiplas tentativas que não atenderam ao formato desejado. Contudo, a ideia de utilizar re.findall() obtida por ao ler o código de uma das tentativas foi aceita.

### Uso 4 - Cálculo de taxa de clock e erro no pattern regex no script de processamento de dados
* **Ferramenta:** Gemini Pro
* **Modelo:** 4 Hydrogen
* **Integrantes:** Gustavo, Pablo
* **Onde foi utilizado:** Scripts externos - artefatos afetados: `process_data.py`
* **O que foi perguntado/solicitado:** Foi perguntado se era possível estimar a taxa de clock por meio de um calculo com os campos `seconds user`, `seconds sys` e  `time elapsed`, uma vez que o evento `task-clock` não foi utilizado.
* **Avaliação da resposta:** A resposta foi positiva, confirmando que seria possível estimar a taxa de clock ao calcular 1/(`seconds user`+`seconds sys`). Ao revisar o trecho de `process_data.py`, a IA identificou que a extração de sys_mode_time procurava por `seconds time elapsed` em vez de `seconds sys`, erro derivado da cópia da linha superior no código para poupar a reescrita. Esse erro foi corrigido

### Uso 5 - Entendimento da discrepância de acessos a cache entre máquinas (L2 vs. L3)
* **Ferramenta:** Gemini Pro
* **Modelo:** 4 Hydrogen 
* **Integrantes:** Gustavo, Pedro, Pablo
* **Onde foi utilizado:** Estudo e documentação - artefatos afetados: `README.md` e `relatorio.pdf`.
* **O que foi perguntado/solicitado:** Foi discutido sobre as limitações de comparabilidade dos eventos de cache e diferenças entre as PMUs das duas arquiteturas, após notar uma discrepância entre o número de acessos na cache no computador novo e no computador antigo(a exemplo, 30.530.030 acessos em O0 no pc novo na primeira medição e 1.006.977 em O0 na primeira medição, uma diferença de 30x)
* **Avaliação da resposta:** Após uma busca realizada em conjunto ao Gemini e observação sugerida no código do kernel Linux e no código dos eventos com perf stat -vv, chegou-se a conclusão que o **PC novo monitora a cache de nível L2** e o **PC antigo monitora a cache de nível L3** nos eventos cache-references e cache-misses, e por isso foi feita uma adaptação textual no README e no relatório.

### Uso 6 - Organização das especificações de hardware e coleta de turbo/temperatura
* **Ferramenta:** ChatGPT
* **Modelo:** 6 Instant  
* **Integrantes:** Pedro
* **Onde foi utilizado:** Revisão e documentação - artefatos afetados: `README.md`.
* **O que foi perguntado/solicitado:** Foi enviado as informações coletadas com comandos buscando as especificações do computador(como `hostnamectl`, `lscpu`, `dmidecode -t memory`, `uname -r`, `arch`) e solicitado que ele buscasse o conteúdo de certos campos e organizasse em uma tabela *Markdown* facilitando assim o trabalho de documentação. Ademais foi perguntado como adquirir informações como o carga e temperatura na máquina.
* **Avaliação da resposta:** O texto em markdown foi aceito e validadopara conferir se ele não modificou nenhuma informação e e testamos os comandos de coleta de temperatura/carga no ambiente antes de usar.

### Uso 7 - Script de monitoramento de carga/temperatura
* **Ferramenta:** ChatGPT
* **Modelo:** 6 Instant
* **Integrantes:** Pablo
* **Onde foi utilizado:** Scripts externos - artefatos afetados: `coleta_jacobi_simples_vibed`
* **O que foi perguntado/solicitado:** Foi requisitado a criação de um script, para registrar uma amostragem matrizes de tamanho 1000, 3000, 5000, com as 3 otimizações, e registrar a carga sob execução, temperatura para se obter uma comparação de como estavam as condições. 
* **Avaliação da resposta:** O script inicial foi recusado, após um pedido para modificação, simplificação e aproximação do código aos scripts escritos pelos membros do grupo, seguido de uma revisão do código foi aceito. 

### Uso 8 - Ánalise da carga e da temperatura
* **Ferramenta:** ChatGPT
* **Modelo:** 6 Instant
* **Integrantes:** Pablo, Pedro
* **Onde foi utilizado:** Scripts externos - artefatos afetados: `coleta_jacobi_simples_vibed`
* **O que foi perguntado/solicitado:**  Foram enviados logs do monitoramento de temperatura e carga e requirido que informações como a temperatura média durante a execução, media de carga durante a execução, considerando os niveis de otimização e tamanho de entrada 
* **Avaliação da resposta:** Aceito com ressalvas, que levaram a organização dos dados em `DataFrames`com `pandas` em código próprio para validar os valores

### Uso 9 - Revisão textual e ánalise gráfica: 
* **Ferramenta:** Gemini Pro
* **Modelo:** 4 Hydrogen 
* **Integrantes:** Pablo, Pedro, Gustavo
* **Onde foi utilizado:** Revisão textual e documentação
* **O que foi perguntado/solicitado:** Foi enviado estruturas bases de texto, hipotéses e ánalises dos gráficos e requisitado uma revisão textual e requisitado melhoras e aprofundamento nas afirmações
* **Avaliação da resposta:** As sugestões foram em grande aceitas, de modo a melhorar a escrita do documento e a clareza. Além disso também foi adicionado trechos textuais também se referindo a ánalise estatística das visualizações de boxplot.

### Uso 10 - Auxílio em comando no Linux
* **Ferramenta:** Gemini Pro
* **Modelo:** 4 Hydrogen 
* **Integrantes:** Pablo, Pedro
* **Onde foi utilizado:** Revisão textual e documentação
* **O que foi perguntado/solicitado:** Foi consultado como exibir tamanhos de arquivos em MB com ls, informações utilizadas para validação do tamanho das matrizes `Ax000.bin` em relação a cache dos computadores
* **Avaliação da resposta:** A resposta apresentou opções como ls -l –-block-size=M, ls -l -–block-size=MB
e ls -lh,
