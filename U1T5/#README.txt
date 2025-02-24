Análise de Mobilidade no Entorno da UFRN em Natal-RN
Este projeto analisa a mobilidade no entorno da Universidade Federal do Rio Grande do Norte (UFRN), utilizando métricas de centralidade em uma rede de ruas, com o objetivo de identificar pontos estratégicos para mobilidade, como possíveis locais para dock-stations de bicicletas compartilhadas.

Objetivos
Calcular e visualizar diferentes métricas de centralidade para analisar a conectividade e posição estratégica dos nós na rede.
Realizar uma análise da função de densidade de probabilidade (PDF) e da função de distribuição acumulada (CDF) dos graus dos nós.
Realizar uma análise multivariada das métricas de centralidade.
Identificar a estrutura de core/shell da rede, para analisar a robustez e a hierarquia dos nós.
Requisitos
Para executar o código, são necessárias as seguintes bibliotecas:

networkx
osmnx
matplotlib
seaborn
numpy
pandas
----------------------------------------------------------------------------------------------------------------------------------------------------------
Explicação das Análises
1. Cálculo e Visualização das Métricas de Centralidade
Para entender a importância e a conectividade dos nós na rede, foram calculadas quatro métricas de centralidade:

Degree Centrality: Mede a quantidade de conexões diretas de cada nó.
Closeness Centrality: Mede a distância média de um nó para todos os outros, identificando nós centrais.
Betweenness Centrality: Identifica nós que atuam como pontes em caminhos mais curtos entre outros nós, importantes para o fluxo de mobilidade.
Eigenvector Centrality: Mede a influência de um nó com base na conectividade dos seus vizinhos.
Essas métricas foram plotadas lado a lado para facilitar a comparação visual.

2. Análise PDF e CDF dos Graus dos Nós
Para analisar a distribuição dos graus na rede:

A PDF (Função de Densidade de Probabilidade) mostra a frequência dos diferentes graus de nós na rede, ajudando a identificar a presença de nós com muitos ou poucos conectores.
A CDF (Função de Distribuição Acumulada) exibe a probabilidade acumulada dos graus dos nós.
3. Análise Multivariada das Métricas de Centralidade
Para entender a relação entre as métricas de centralidade, foi realizada uma análise multivariada que exibe as correlações e distribuições das métricas. Isso ajuda a identificar como cada métrica se relaciona com as outras e a identificar possíveis padrões.

4. Identificação do Core/Shell da Rede
Utilizando o conceito de k-core, foi identificada a estrutura de core/shell da rede, onde nós mais conectados formam o núcleo e nós menos conectados formam as camadas externas. A estrutura de k-cores ajuda a identificar regiões densamente conectadas, o que pode ser útil para decidir locais estratégicos para infraestrutura.

Resultados e Interpretações
Métricas de Centralidade
Os nós com alta Degree Centrality representam áreas de grande conectividade, que são importantes para facilitar o fluxo na rede. Nós com alta Betweenness Centrality indicam locais estratégicos para direcionar o tráfego e são potenciais locais para alocar dock-stations de bicicletas, maximizando o alcance da mobilidade.

Distribuições PDF e CDF
A PDF e a CDF dos graus dos nós ajudam a entender se a rede possui muitos nós de baixa conectividade ou alguns nós que desempenham papéis centrais. Redes com nós de alta conectividade tendem a ter melhor suporte para fluxo de mobilidade.

Estrutura Core/Shell
A estrutura de core/shell revela os nós mais centrais da rede. Áreas no núcleo da rede podem ser mais resilientes e estratégicas para a colocação de infraestrutura, enquanto áreas na "casca" podem necessitar de intervenções para melhorar a conectividade.

Conclusão
Este projeto forneceu uma visão detalhada da rede de ruas no entorno da UFRN em Natal-RN, utilizando métricas de centralidade e análise de estrutura para identificar áreas com potencial para intervenções de mobilidade. As informações obtidas podem auxiliar na tomada de decisões para melhorar a mobilidade e a conectividade na região.


LINK DO VIDEO: https://www.loom.com/share/5663839237144f70bf3d784e4ba78cf4?sid=1bec22c2-0604-4410-819f-5bcd513f1e2b