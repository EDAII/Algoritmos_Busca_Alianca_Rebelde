# Star Wars: Aliança Rebelde - Buscas na Rebelião

### Em meio ao caos da Guerra Galáctica, a informação é a arma mais poderosa da Aliança Rebelde. Como um(a) Analista de Inteligência, sua missão é mergulhar em dados Imperiais capturados e encontrar dados vitais para as operações da Aliança.

### Cada desafio do jogo é uma simulação de como os algoritmos de busca são aplicados para transformar dados brutos em vantagem estratégica, com uma narrativa imersiva inspirada no universo Star Wars. Prepare-se para testar sua lógica e sua capacidade de agir com precisão.

## BUSCAR PARA VENCER!

## Descrição do Jogo

"Aliança Rebelde - Buscas da Rebelião" é um jogo de puzzle e simulação onde o jogador assume o papel de um(a) Analista de Inteligência. Sua jornada o levará a desvendar segredos do Império, aplicando algoritmos de busca para localizar informações em sistemas de arquivos complexos. Com o apoio de seu droide de protocolo, você enfrentará missões críticas que exigem o domínio de diferentes técnicas de busca para garantir o sucesso da Rebelião.

## Público-Alvo

- Estudantes da disciplina de Algoritmos de Busca.

- Entusiastas de jogos de puzzle e simulação.

- Fãs do universo Star Wars que apreciam narrativas de espionagem e estratégia.

## Objetivos do Jogo

- Para o Jogador: Concluir com sucesso todas as missões ao utilizar a lógica de busca correta para cada tipo de problema.

- Educacional: Proporcionar uma compreensão prática e intuitiva da aplicação de diversos algoritmos de busca, como a busca sequencial e hashing.

## Missões do Jogo (Desafios de Algoritmos)

### MISSÃO 1: Inspeção no Hangar de Carga
#### Algoritmo: Busca Sequencial

- **Contexto:** Suspeita-se que um carregamento de detonadores térmicos foi escondido em um dos contêineres de um grande hangar. O Império misturou o contêiner em um catálogo massivo de carga.
- **Descrição:** A missão é dividida em fases, simulando a complexidade de uma busca sequencial em cenários reais:
  - **Fase 1**: Use a busca sequencial simples para encontrar um código de contêiner específico, que serve como sua primeira pista.
  - **Fase 2:** Utilize a informação do primeiro contêiner para encontrar um segundo, otimizando a busca com métodos de reorganização de dados.
  - **Fase 3:** Em um catálogo de mais de 400 contêineres, utilize uma tabela de índices fornecida para reduzir o espaço de busca e encontrar o item final de contrabando, provando a eficiência da busca sequencial indexada.

### MISSÃO 2: Localizando um Infiltrado
#### Algoritmo: Busca Binária

- **Contexto:** Há um agente Imperial infiltrado na Aliança. Os registros da inteligência estão armazenados em uma lista ordenada por ID, e apenas a eficiência da busca binária pode localizar rapidamente o alvo antes que o Império descubra a operação.
- **Descrição:** A missão é dividida em fases que representam cenários diferentes da busca binária:
  - **Fase 1**: Localize o infiltrado pelo ID exato usando a lógica de dividir para conquistar.
  - **Fase 2:** Descubra a primeira ocorrência de um ID duplicado em meio a registros repetidos, simulando a necessidade de precisão em listas não únicas.
  - **Fase 3:** Confirme rapidamente se existe algum agente dentro de um intervalo de IDs, utilizando duas buscas binárias (limites inferior e superior), para validar a presença de registros em faixas específicas.

### MISSÃO 3: Sintonizando a Frequência Secreta
#### Algoritmo: Busca por Interpolação

- **Contexto:** Uma transmissão da Aliança está escondida em meio a um espectro de canais uniformemente distribuídos. Para não chamar a atenção do Império, é preciso localizar o sinal com o mínimo de passos possível.
- **Descrição:** O desafio simula a busca por interpolação em um espectro de frequências:
  - **Fase Única:** O jogador deve utilizar a fórmula da interpolação para estimar a posição da frequência secreta no intervalo atual (low e high). A cada passo, os valores de pos, arr[low], arr[high] e arr[pos] são exibidos, e o jogador decide se deve mover os limites ou se encontrou o alvo.
  - O objetivo é demonstrar como a interpolação aproveita a distribuição uniforme para convergir mais rapidamente ao valor alvo do que a busca binária em alguns cenários.


### MISSÃO 4: Acesso Rápido aos Arquivos da Frota
#### Algoritmo: Hashing

- **Contexto:** A Aliança interceptou um catálogo da frota Imperial. Os arquivos estão organizados por um sistema de "hashing" para acesso rápido. Sua missão é reverter o processo para encontrar as especificações de uma nave de carga vital para a Aliança.
- **Descrição:** Este desafio simula o processo de acesso a dados via hashing:
  - **Fase 1:** O jogador deve calcular o hash de uma "chave" de nave e identificar o "bucket" correto na tabela de hash.
  - **Fase 2:** Ao encontrar o bucket, o jogador descobre que houve uma colisão. Ele deve usar a lógica de encadeamento para inspecionar os itens na lista até encontrar a nave-alvo, acessando assim os dados de forma precisa.

