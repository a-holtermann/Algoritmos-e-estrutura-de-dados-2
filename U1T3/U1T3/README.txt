Assortatividade em Rede de Medicamentos e Princípios Ativos
Este projeto tem como objetivo estudar a assortatividade em redes de medicamentos e princípios ativos, analisando a co-ocorrência e a relação entre diferentes características dos medicamentos, como categoria regulatória, complexidade e empresa.

Descrição do Projeto
Este código foi desenvolvido para criar três tipos de redes baseadas em medicamentos e princípios ativos usando a biblioteca NetworkX. O conjunto de dados foi extraído do site de dados abertos do governo brasileiro, contendo informações sobre medicamentos registrados no Brasil.

As três redes geradas são:

Rede de Co-ocorrência de Princípios Ativos entre Medicamentos
Grafo Bipartido de Medicamentos e Princípios Ativos
Co-ocorrência por Empresa ou Classe Terapêutica
Cada uma das redes é analisada em termos de assortatividade, uma métrica que mede o quanto os nós de uma rede estão conectados de forma similar em relação a uma propriedade.

Estrutura do Código
Leitura e Limpeza dos Dados

Os dados são carregados a partir de um arquivo CSV e tratados para garantir a limpeza e organização da informação, principalmente no campo de princípio ativo.
Criação das Redes

Rede 01: Conecta medicamentos que compartilham pelo menos um princípio ativo.
Rede 02: Grafo bipartido que conecta medicamentos aos seus princípios ativos.
Rede 03: Conecta medicamentos da mesma empresa ou classe terapêutica.
Cálculo da Assortatividade

Para cada rede, é calculada a assortatividade em relação à categoria regulatória, empresa e complexidade.
Visualização das Redes

As redes geradas são visualizadas usando matplotlib.
Respostas às Perguntas
1. Medicamentos da mesma categoria regulatória tendem a compartilhar mais princípios ativos?
Sim, a Rede 01 foi criada para investigar essa hipótese. Nesta rede, dois medicamentos são conectados se compartilham ao menos um princípio ativo. A assortatividade calculada para essa rede com base na categoria regulatória indicará se os medicamentos da mesma categoria estão mais conectados entre si. Se o valor de assortatividade for positivo, isso sugere que os medicamentos da mesma categoria compartilham mais princípios ativos.

2. Medicamentos da mesma empresa tendem a compartilhar mais princípios ativos?
A Rede 03 foi criada para analisar a co-ocorrência de medicamentos que pertencem à mesma empresa. Medicamentos da mesma empresa são conectados se compartilharem ao menos um princípio ativo. A assortatividade com base na empresa foi calculada, e um valor positivo indica que medicamentos da mesma empresa compartilham mais princípios ativos.

3. Medicamentos com mais princípios ativos tendem a se conectar com medicamentos de similar complexidade?
A Rede 02 (grafo bipartido) foi criada para analisar a relação entre medicamentos e seus princípios ativos. Calculamos a assortatividade com base no grau dos nós para verificar se medicamentos com muitos princípios ativos (maior complexidade) tendem a se conectar com outros medicamentos complexos. Um valor de assortatividade positivo sugeriria que medicamentos complexos se conectam mais com outros medicamentos complexos.