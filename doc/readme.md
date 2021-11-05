# Plataforma de Dados

- [1. Introdução](#1-introdução)
- [1.1. Objetivos do trabalho](#1-1-objetivos-do-trabalho)
- [2. Fundamentação técnica](#2-fundamentação-técnica)
  - [2.1 Plataforma de dados](#2-1-plataforma-de-dados)
  - [2.2 Data Lake](#2-2-data-lake)
  - [2.3 Big Data](#2-3-big-data)
  - [2.4 ETL](#2-4-etl)
  - [2.5 Apache Airflow](#2-5-apache-airflow)
  - [2.6 Apache Spark](#2-6-apache-spark)
  - [2.7 Hadoop Distributed File System](#2-7-hadoop-distributed-file-system)
  - [2.8 Apache Hive](#2-8-apache-hive)
  - [2.9 Event Streaming](#2-9-event-streaming)
  - [2.10 Apache Kafka](#2-10-apache-kafka)
  - [2.11 Trino](#2-11-trino)
  - [2.12 Apache Parquet](#2-12-apache-parquet)
  - [2.13 Apache Avro](#2-13-apache-avro)
  - [2.14 Confluent Schema Registry](#2-14-confluent-schema-registry)
  - [2.15 Computação distribuída](#2-15-computação-distribuída)
  - [2.16 Spark Structured Streaming](#2-16-Spark-Structured-Streaming)
  - [2.17 Docker](#2-17-docker)
  - [2.18 Plataforma Clickstream](#2-18-plataforma-clickstream)
  - [2.19 Kubernetes](#2-19-kubernetes)
- [3. Desenvolvimento](#3-desenvolvimento)
  - [3.1 Arquitetura](#3-1-arquitetura)
  - [3.2 Gerenciamento de pipelines com DAGs](#3-2-gerenciamento-de-pipelines-com-dags)
  - [3.3 Armazenamento de dados](#3-3-armazenamento-de-dados)
  - [3.4 Definição de metadados](#3-4-definição-de-metadados)
  - [3.5 Ingestão de dados em tempo real](#3-5-ingestão-de-dados-em-tempo-real)
  - [3.6 Análise dos dados](#3-6-análise-dos-dados)
  - [3.7 Estudo de casos](#3-7-estudo-de-casos)
  - [3.7.1 ETL em lote](#3-7-1-etl-em-lote)
  - [3.7.2 ETL em tempo real](#3-7-2-etl-em-tempo-real)
- [4. Resultados](#4-resultados)
  - [4.1. ETL em lote](#4-1-etl-em-lote)
  - [4.2. ETL em tempo real (Clickstream)](#4-2-etl-em-tempo-real-clickstream)
  - [4.3. Painel Kubernetes](#4-3-painel-kubernetes)
- [5. Considerações finais](#5-considerações-finais)
- [5.1. Contribuições e Conclusões](#5-1-contribuições-e-conclusões)
- [5.2. Trabalhos futuros](#5-2-trabalhos-futuros)
- [Referências](#referências)

## 1 Introdução

Nos dias atuais é cada vez mais comum empresas coletarem quantidades imensas de dados, que são gerados por usuários, ferramentas de auditoria que geram logs ou soluções que envolvem IoT. Porém, para lidar com essa quantidade imensa de dados não é uma tarefa trivial. Dependendo da área de negócio, dados devem ser armazenados em lugares de alta disponibilidade, consistente e seguro.

Além da preocupação em armazenar os dados, é entendível que estes servirão para algum
propósito, como por exemplo, entregar uma experiência personalizada para usuários, analisar e monitorar técnicas anti-fraude entre outras coisas. Neste momento que a área de processamento massivo de dados entra em questão.

O processamento de quantidades massivas de dados lida com alguns aspectos não tão triviais, por exemplo, alta capacidade computacional, computação distribuída e tolerante a falhas, o que caracteriza lidar com técnicas e ferramentas, conhecidas hoje como Big Data.

Hoje no mercado existem ferramentas e serviços disponíveis capazes de proporcionar ambientes auto-gerenciáveis que disponibilizam uma plataforma com alta disponibilidade, segura, normalmente tolerante a falhas entre outros aspectos. Porém, tais soluções envolvem altos custos de gerenciamento e suporte e, que também limitam a capacidade do usuário em extender ou personalizar uma solução, permitindo somente integrar ferramentas gerenciadas pela própria provedora do serviço ou plataforma.

### 1-1 Objetivos do trabalho

O objetivo geral deste trabalho é desenvolver uma plataforma de dados que proporcione a escrita de scripts capazes de extrair, transformar e armazenar dados aproveitando de ferramentas open-source disponibilizadas pelo mercado de teconlogia.

Para a realização deste trabalho foram estabelecidos alguns objetivos específicos que envolvem a criação de uma plataforma de dados:

- Utilizando ferramentas open-source
- Focada na otimização de custos
- Extensível e personalizável
- Que proporcione ao usuário a construção de produtos de dados
- Capaz de fazer análises históricas
- Capaz de coletar dados em tempo real
- Capaz de fazer processamentos de dados em lote e em tempo real

## 2 Fundamentação técnica

Neste capítulo serão abordados os conceitos básicos que definem uma plataforma de dados e seus requisitos, e também algumas das tecnologias que compõe a plataforma contruída neste trabalho.

### 2-1 Plataforma de dados

Plataforma de Dados é um conjunto ferramental e de técnicas que busca extrair dados de diversas fontes, alimentar e enriquecer tais dados, que por fim são armazenados em uma outra base de dados. A finalidade principal de uma plataforma de dados é centralizar os dados de uma organização, de modo que esteja em conformidade com leis de proteção de dados, aplicando inteligência para alavancar a sua estratégia.

Comumente, plataformas de dados incluem ferramentas de extração e transformação de dados que por fim são armazenados em tecnologias de armazenamento de dados em larga escala, conhecidos como Data Lake.

Referência: https://blog.tail.digital/o-que-e-customer-data-platform-e-porque-voce-precisa-de-um/

### 2-2 Data Lake

Data Lake é um tipo de repositório de dados que armazena quantidades massivas de dados estruturados e não estruturados. Comumente armazena-se dados brutos, ou dados não tratados, que no momento em que são coletados não há uma finalidade para tal, e sim, definida posteriormente. Este dado pode ser utilizado por cientístas e analístas de dados ou aplicações que envolvem aprendizado de máquinas por diversas vezes e para diversos propósitos, o que facilita a sua reutilização.

Algumas das principais diferenças entre Data Lake e Data Warehouse, que é outro tipo de ferramenta de armazenamento de dados para Big Data, é que Data Lakes armazenam dados não estruturados que são estruturados posteriormente (conhecido como "schema on read"). Também não são acomplados à ferramentas de alto custo computacional para otimização de leitura e controle de acesso concorrente à dados, o que minimiza gastos com hardware e software e flexibiliza a capacidade de armazenamento de dados.

Referência: https://www.redhat.com/en/topics/data-storage/what-is-a-data-lake

### 2-3 Big Data

Big Data refere-se à manipulação ou gerenciamento de uma larga quantidade de dados ou de dados muito complexos. Big Data tornou-se conhecido pelos "3 Vs" de variedade, velocidade e volume. Volume refere-se à quantidade massiva de dados, variedade à ampla gama de formatos não padronizados, volume refere-se à necessidade de processar com rapidez e eficiência.

O principal objetivo de Big Data é ofecer informações em tempo real que podem ser usadas para alavancar a estratégia da organização. O processamento de informações em tempo real é o principal objetivo das organizações que buscam agregar valor aos seus clientes de forma consistente e contínua, o que se encaixa em um dos pilares de computação de ponta.

Referência: https://www.redhat.com/en/topics/big-data

### 2-4 ETL

ETL, ou extrair (Extract), transformar (Transform) e armazenar (Load) é um processo que extrai, transforma e armazena dados de multiplas fontes para um data warehouse ou outro repositório unificado de dados.

No processo de extração, o dado é copiado de uma fonte e movido para outro local intermediário, conhecido como staging area. O dado pode ser extraído de um fonte de dados estruturado ou não estruturado, por exemplo, banco de dados transacionais SQL ou não SQL, sistemas ERP, e-mails, API REST e outros.

No processo de transformação o dado bruto pode, normalmente é, transformado em um formato útil que posteriomente é utilizado para análises. O processo de transformação pode envolver filtros, limpezas, duplicações, validações, cálculos, traduções, agregações, anonimizações para governança de dados entre outras coisas. Essa etapa de transformação normalmente ocorre em um ambiente computacional diferente da fonte, para assim, limitando o impacto do desempenho nos sistemas de origem e reduz a probabilidade de corrupção de dados.

No processo de armazenamento, o último passo, o dado é movido da staging area para um data warehouse, por exemplo. Normalmente, inicialmente envolve o armazenamento de todo o dado, seguindo por carregamentos de alterações de dados incrementais periodicos. Também pode haver a necessidade, menos comum, do reprocessamento do dados o que acaba envolvendo o carregamento total dos dados novamente.

Algumas ferramentas conhecidas na comunidade de engenharia de dados são Airflow, Luigi, Argo, Kubeflow e outros, aos quais abordam cada passo do processo ETL de forma separada.

Referência: https://www.ibm.com/cloud/learn/etl

### 2-5 Apache Airflow

Apache Airflow é uma plataforma open-source para criar, agendar e monitorar programaticamente fluxos de trabalho. Airflow é uma ferramenta principalmente utilizada para fluxos de trabalho ETL seguindo o conceito de DAGs (Directed Acyclic Graphs). Assim, as tarefas atribuídas ao fluxos são executadas por workers seguindo uma dependência especificada.

A ferramenta Airflow permite a integração com diversas outras ferramentas que auxiliam no processo de ETL, como por exemplo, Apache Spark para transformação de dados de forma distribuída.

Referência: https://airflow.apache.org/docs/apache-airflow/stable/index.html

### 2-6 Apache Spark

Apache Spark é um mecanismo de análise unificado para processamento de dados em grande escala. Spark utiliza caching em memória, a grande diferença do seu concorrente Hadoop, e execução de consulta otimizada para consultas rápidas em dados de qualquer tamanho. Alguns componentes disponibilizados pelo Spark, como por exemplo Spark Streaming e Spark Core, possibilitam processamento de dados em lotes e stream.

Referência: http://spark.apache.org/

### 2-7 Hadoop Distributed File System

HDFS é um sistema de arquivos distribuído que lida com grandes conjuntos de dados executados em hardware comum. Ele é usado para dimensionar um único cluster Apache Hadoop para centenas(e até milhares) de nós. HDFS é um dos principais componentes do Apache Hadoop.

Com HDFS os dados podem ser particionados e armazenados em diferentes nós/servidores. O particionamento em diversos nós gera a replicação de dados, o que implica na redundância também. A redundância pode ser aumentada ou diminuída, conforme o caso de uso da aplicação. Portanto a redundância oferece múltiplos benefícios, o mais óbvio é a alta disponibilidade - um dos principais pilares de computação distribuída.

Referência: https://www.ibm.com/analytics/hadoop/hdfs

### 2-8 Apache Hive

Apache Hive é uma ferramenta de data warehouse que facilita a leitura, escrita e gerenciamento de grandes conjuntos de dados que residem em armazenamento distribuído e consultados usando a sintaxe SQL.

Hive disponibiliza algumas ferramentas como:

- Acesso a dados via instruções SQL, portanto permite tarefas de extração, transformação e armazenamento
- Mecanismo de armazenamento de dados estruturados em uma variedade de formatos
- Acesso à arquivos armazenados diretamente no Apache HDFS ou HBase
- Execução de consultas via Apache Spark ou MapReduce
- Componente para armazenamento de metadados, ou descritores de arquivos

Apache Hive foi projetado para maximizar a escalabilidade (escalar horizontalmente com mais máquinas adicionadas dinamicamente ao cluster Hadoop), desempenho, extensibilidade, tolerância a falhas e acoplamento fraco com seus formatos de entrada.

Referência: https://cwiki.apache.org/confluence/display/Hive/Home

### 2-9 Event Streaming

O event streaming é a prática de capturar dados em tempo real de fontes de eventos como bancos de dados, sensores, dispositivos móveis, serviços em nuvem e aplicativos de software na forma de fluxos de eventos; armazenar esses fluxos de eventos de forma duradoura para recuperação posterior; manipular, processar e reagir aos fluxos de eventos em tempo real e também retrospectivamente; e encaminhar os fluxos de eventos para diferentes tecnologias de destino, conforme necessário. O streaming de eventos, portanto, garante um fluxo contínuo e interpretação dos dados para que as informações certas estejam no lugar certo, na hora certa.

Algumas das principais ferramentas de event streaming no mercado nos dias de hoje são Apache Kafka, AWS Kinesis, ActiveMQ, RabbitMQ entre outros.

Referência: https://kafka.apache.org/documentation/

### 2-10 Apache Kafka

Apache Kafka é uma plataforma de streaming de eventos distribuídos de código aberto usada por milhares de empresas para pipelines de dados de alto desempenho, análise de streaming, integração de dados e aplicativos de missão crítica.

Kafka é comumente utilizado no processo ETL na etapa de extração via transmissão de eventos de diversas fontes para uma área intermediária, conhecida como staging area.

Referência: https://kafka.apache.org/

### 2-11 Trino

Trino é um mecanismo de consulta SQL distribuído projetado para consultar grandes conjuntos de dados distribuídos em uma ou mais fontes de dados heterogêneas. Trino é utilizado principalmente para trabalhar com terabytes or petabytes de dados armazenados em fontes diversas, como por exemplo, Apache HDFS, bancos de dados transacionais como MySQL, Oracle e também outras fontes de dados como Cassandra.

Trino foi projetado para manipular análises e data warehousing: análises de dados, agregrações de quantidades massivas de dados. Essas cargas de trabalho são sempre classificadas como Online Analytical Processing (OLAP).

Referências:

- https://trino.io/docs/current/overview.html
- https://trino.io/docs/current/overview/use-cases.html

### 2-12 Apache Parquet

Apache Parquet é um formato de armazenamento colunar disponível no ecossistema Hadoop, independentemente da escolha da estrutura de processamento de dados, modelo de dados ou linguagem de programação.

Apache Parquet permite armazenar arquivos contendo a definição do schema no próprio arquivo com alguns metadados. Além disso, é possível armazenar a declaração do particionamento de dados. Com o benefício de armazenamento colunar do Apache Parquet, os custos de armazenamento, leitura e processamentto dos dados reduzem significativamente, pois os dados são compactados e a leitura é feita apenas nas colunas necessárias para retornar uma consulta.

A figura abaixo ilustra a comparação na leitura de 1 TB de dados em um arquivo CSV e no formato Parquet.

![Apache Parquet vs CSV](./images/parquet_vs_csv.png)

Referências:

- https://parquet.apache.org/
- https://blog.openbridge.com/how-to-be-a-hero-with-powerful-parquet-google-and-amazon-f2ae0f35ee04

### 2-13 Apache Avro

Apache Avro é formato binário de armazenameno de arquivos e mensagens. Apache Avro resolves alguns dos principais problemas quando trata-se de evolução de schemas de dados estruturados. Avro armazena no próprio arquivo ou mensagem a definição dos schemas, então aplicações antigas conseguem ler schemas novos e, aplicações novas conseguem ler schemas antigos. Além disso Avro é armazenado em formato binário, o que o torna compacto e eficiente.

Referências:

- https://www.ibm.com/analytics/hadoop/avro
- https://catherine-shen.medium.com/why-you-should-use-avro-and-schema-registry-for-your-streaming-application-2f24dcf017c8

### 2-14 Confluent Schema Registry

Confluent Schema Registry é uma camada provedora de metadados. Disponibiliza uma API RESTFul para armazenar a definição de schemas no formato Avro, JSON ou Protobuf. Com Schema Registry torna-se capaz armazenar versões de cada schema, o que permite visualizar o histórico de versões dos schemas. Atua como um componente intermediário separado dos brokers do Apache Kafka, porém permite a comunicação com consumers para recuperar schemas e assim fazer a leitura de tópicos, como também se comunica com producers para validarem schemas e postarem mensagens em tópicos.

Referências:

- https://docs.confluent.io/platform/current/schema-registry/index.html

### 2-15 Computação distribuída

Computação distribuída é termo para referir-se a sistemas que possuem múltiplos componentes de softwares executando em múltiplos computadores, mas executando apenas um sistema. Sistemas distribuídos podem constituir-se de múltiplos computadores localizados geograficamente no mesmo local conectados por uma rede local ou podem estar geograficamente distribuídos conectados por um rede ampla. O objetivo da computação distribuída é fazer com que esse múltiplos computadores se comportem como apenas um. Alguns benefícios da computação distribuída inclue escalabilidade, podendo adicionar mais computadores a rede e também a redundância, ao qual se um computador parar de funcionar, o sistema continuará executando.

Referências:

- https://www.ibm.com/docs/ko/txseries/8.1.0?topic=overview-what-is-distributed-computing

### 2-16 Spark Structured Streaming

Spark Structured Streaming é um mecanismo de processamento em tempo real que utiliza Spark SQL para criar fluxos de processamento de dados da mesma maneira que fluxo de processamento em lote são criados. Spark Structured Streaming é responsável por adicionar todos os dados em um fluxo de streaming e adicionar ao final de uma DataFrame ou Dataset, que é componente do mecanismo Spark SQL.

Referências:

- https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

### 2-17 Docker

Docker é uma plataforma open-source que permite desenvolvedores virtualizar componentes e aplicações utilizando a técnica de containers e imagens. Docker permite empacotar diversas aplicações e suas respectivas configurações em um único artefato - a imagem, ao qual pode ser implantada e replicada diversas vezes minimizando o custo de manutenção.

Referências:

- https://docs.docker.com/get-started/overview/

### 2-18 Plataforma Clickstream

Plataforma Clickstream, ou software de Clickstream é um produto que coleta todo o fluxo da jornada online de usuários em uma plataforma ou websiite. Normalmente plataformas de Clickstream são focados em um único website e geralmente mostram o progresso dos usuários desde o momento em que ingressam no website até o momento que fecham a compra de um produto. Dados gerados por esse tipo de plataforma são comumente utilizados para análise do comportamento de usuários.

Referências:

- https://www.wordtracker.com/blog/keyword-research/what-is-clickstream-data

### 2-19 Kubernetes

Kubernetes é um sistema de código aberto para orquestração de containers na nuvem, da qual disponibiliza diversas funcionalidades para automatização de atividades envolvendo gerenciamento da infraestrutura de containers, como por exemplo, escalabilidade horizontal de recursos, orquestração de componentes de persistência de dados, balanceamento de carga, gerenciamento de segredos etc. Kubernetes baseia-se em 15 anos de experiência do Google gerenciando e executando aplicações em produção combinado com as melhores práticas do mercado.

Referências:

- https://kubernetes.io/

## 3 Desenvolvimento

Este capítulo aborda o processo de construção e desenvolvimento da plataforma de dados, tanto quanto o de definição da arquitetura da plataforma.

### 3-1 Arquitetura

A figura X mostra a arquitetura ao qual a plataforma de dados foi implementada. Na arquitetura, destaca-se 4 camadas - Airflow juntamente com Spark definindo a camada de processamento, ou seja, onde ocorre o gerenciamento de pipelines ETL em lote. Hadoop (HDFS) e Hive Metastore como camada de armazenamento ou Data Lake, tanto os dados/informações em sí, como também o catalogo de dados. Trino compõe a camada de análise, ao qual é possível executar instruções utilizando-se da síntaxe SQL para a exploração analítica dos dados. Por fim, a aplicação escrita em Javascript (Node.js), Apache Kafka e Spark Streaming compõem a camada de ingestão e processamento de dados em tempo real.

![Arquitetura](./images/architecture.jpg)

### 3-2 Gerenciamento de pipelines com DAGs

Para definir, executar e gerenciar tarefas previamente agendadas utilizou-se a ferramenta Apache Airflow. Tal ferramenta permite-nos escrever diferentes scripts na linguagem Python que denominam-se tarefas. Um conjunto de tarefas compõem o que chama-se na literatura de pipelines ETL, as DAGs. As DAGs permite-nos definir fluxos de execução complexos, não limitando-se apenas a execução de códigos locais, mas também a invocação de aplicação remotas e também a chamada de APIs externas entre outros tipos de soluções.

A figura X mostra a definição de uma DAG simples, ao qual a primeira tarefa é uma função Python que recebe dois números e retorna a soma deles. A segunda tarefa é outra função Python que apenas mostra o texto `ok` e retorna o mesmo.

![Definição de DAG](./images/simple_dag.png)

A figura X mostra de forma visual como as tarefas anteriormente definidas formam um grafo acíclico direcionado.

![Definição visual de DAG](./images/simple_dag_visual.png)

### 3-3 Armazenamento de dados

Para compor e alimentar o Data Lake, utilizou-se a ferramenta Apache Hadoop (HDFS). Para a inserção de dados no HDFS via tarefas definidas no Airflow, fez-se necessário a criação de um Hook - um script personalizado que se comunica internamente com uma API do HDFS. A figura X representa a definição do código Hook para a comunicação com a API do HDFS.

![Definição do Hook HDFS](./images/hdfs_hook.png)

Por fim, para inserir os dados no HDFS fez-se necessário apenas invocar o Hook e passar quais dados a serem inseridos. A figura X demonstra o exemplo da invocação do hook e a inserção de um dado no formato JSON e a figura X mostra o dado já persistido no HDFS.

![Invocação do Hook HDFS](./images/hdfs_hook_invocation.png)

![Dados persistido no HDFS](./images/persisted_data.png)

O pilar de distribuição de dados se dá pela forma ao qual o HDFS é implementado. A arquitetura é definida por dois componentes, sendo eles Namenode e Datanode.

Namenode caracteriza-se pela interface com o cliente ao qual quer manipular os dados e comporta-se como um orquestrador. Tal componente responsabiliza-se por receber as chamadas de leitura e escrita de dados e decidir em qual nó (Datanode) o dado será persistido ou será consultado para disponibilização. Namenode armazena somente metadados, como por exemplo, nomo e caminho de arquivos, número de blocos escritos, número de réplicas e outras informações relacionadas aos Datanodes.

Datanodes, como citado anteriormente, são orquestrados pelo Namenode, e sua função é persistir e disponibilizar bloco de dados ao qual é requisitado pelo Namenode. A figura X ilustra a arquitetura do HDFS.

![Arquitetura HDFS - Referência https://amitray.com/hadoop-architecture-in-big-data-yarn-hdfs-and-mapreduce/](./images/hdfs_architecture.jpg)

### 3-4 Definição de metadados

Para a estruturação e definição dos dados, ou seja, definição de databases, tabelas e suas respectivas colunas fez-se necessário a utilização da ferramenta Apache Hive juntamente com Apache Spark para a definição de scripts que recebem um caminho de arquivo em um formato conhecido, como por exemplo JSON, e o converte para outro formato conhecido, Apache Parquet, para posterior consulta via uma ferramenta de análise de dados.

A figura X mostra um trecho de código que recebe o caminho de um arquivo no formato JSON e o persiste novamente em outro caminho no formato Parquet. O script não somente persiste o dado em outro formato, mas também cria os metadados de definição do dados, como por exemplo, a estrutura da tabela. A criação dos metadados é feita internamente pela API do Apache Spark. As figuras X e X mostram respectivamente o dado persistido no HDFS e a definição da tabela criada.

![Persistência dos dados e metadados](./images/write_metadata.png)

![Dado no formato parquet](./images/persisted_metadata.png)

![Definição da tabela](./images/table_definition.png)

### 3-5 Ingestão de dados em tempo real

Uma plataforma de dados ao qual se faz processamento de dados em tempo real necessita de uma ponta ou camada para ingestão de dados em tempo real. Para prover a capacidade de ingerir dados em tempo real, criou-se uma aplicação escrita em Javascript utilizando-se a plataforma Node.js para prover uma API HTTP ao qual se passa o titulo da mensagem e o dado da mensagem no corpo da requisição HTTP.

A figura X apresenta a classe Javascript implementada para receber o titulo da mensagem, que condiz com o nome do tópico Kafka ao qual a mensagem será postada, e também o corpo da mensagem. É importante notar que, antes da postagem da mensagem no tópico Kafka é feito a codificação da mensagem para um formato conhecido, Apache Avro. Internamente, após a codificação da mensagem também é validado se o esquema da mensagem é um esquema válido registrado no repositório de esquemas, o então Confluent Schema Registry. Só então a mensagem é de fato postada no Kafka.

![Definição classe postagem mensagens no Kafka](./images/send_message_class.png)

### 3-6 Análise dos dados

Com o intuito de disponibilizar aos usuários a possibilidade de consultar os dados persistidos no Data Lake usando uma síntaxe conhecida, como por exemplo SQL, usou-se o componente Trino.

Para disponibilizar o ambiente provido do componente Trino, usou-se a ferramenta Docker para subir um container com a imagem do Trino e um arquivo de configuração para expor os dados armazenados como um catálogo de dados. A figura X e X, respectivamente demonstram a configuração do ambiente com Trino e do catálogo de dados.

![Container Trino](./images/trino_docker.png)

![Catálogo de dados Trino](./images/trino_catalog.png)

Por fim, para disponibilizar uma interface intuitiva para o usuário realizar consultas SQL, usou-se o componente SQL Pad ao qual interage com o catálogo de dados definido no Trino.

Para disponibilizar o ambiente provido do componente SQL Pad, também usou-se a ferramenta Docker para subir um container com a imagem contendo o SQL Pad. A figura X e X mostram respectivamente a definição do container do SQL e por fim o uso para realizar consultas SQL.

![Container SQL Pad](./images/sqlpad_docker.png)

![Interface SQL Pad](./images/sqlpad_query.png)

### 3-7 Estudo de casos

Nesta subseção serão apresentados estudo de casos envolvendo fluxos ETL em lote, tanto quanto, em tempo real.

### 3-7-1 ETL em lote

Como demonstração de um fluxo ETL em lote de ponta-a-ponta, implementou-se um fluxo completo de extração, transformação e persistência utilizando uma API escrita na linguagem Javascript, os scripts de extração e transformação com a biblioteca PySpark.

Com o objetivo de expor dados para extração, criou-se uma API ao qual gera um conjunto de dados aleatórios simulando um evento de clique, visualização ou submissão de um formulário por parte de um usuário.

![API geradora de dados aleatórios](./images/api_random_data_code.png)

A Figura X apresenta o código de implementação da API geradora de dados aleatórios, ao qual na chamada da API é passado o parâmetro nomeado como `date` e um limitador da quantidade de registros por chamada, nomeado como `count`.

Da linha 28 a 35 implementou-se o método responsável por gerar um objeto JavaScript contendo os campos username, page e event_name com valores aleatórios. O campo event_time é a conversão do parâmetro date para o formato de Timestamp.

Da linha 19 a 26 foi implementado o método responsável por gerar N objetos JavaScript utilizando o método anteriormente citado, onde N corresponde ao parâmetro count. Por fim, o método envia uma resposta de volta ao cliente invocador da API HTTP.

Para realizar a extração dos dados da API anteriormente citada, criou-se um script de DAG contendo 3 tarefas para definição do fluxo ETL. A Figura X apresenta a implementação do script.

![Script da DAG ETL](./images/study_case_dag.png)

Da linha 7 a 11 é definida a primeira tarefa nomeada como `insights_to_hdfs`. Na primera tarefa é utilizado um operador personalizado - StudyCaseOperator, responsável por fazer uma chamada a API geradora de dados aleatórios e persistir a resposta da chamada no Data Lake. É importante ressaltar que os dados da resposta são persistidos em uma camada de dados brutos, sem nenhuma transformação.

A segunda tarefa, implementada da linha 13 a 27 nomeada como insights_json_to_parquet, é responsável por transformar o dado bruto extraído da API no formato JSON para o formato colunar Parquet, como também a criação de uma tabela no catálogo de dados do Hive Metastore. Nessa tarefa é utilizada outro operador personalizado, responsável por submeter a execução de scripts para o cluster Spark.

A terceira e última tarefa, nomeada como group_insights definida da linha 29 a 41 é responsável por realizar transformações no dado já catalogado, aplicando transformações com intuito de extrair informações analíticas. Essa tarefa também utiliza o mesmo operador da tarefa anterior, que faz submissão de scripts para o cluster Spark. Na Figura X é apresentado a implementação do script de transformação.

![Script de agregação dos dados](./images/study_case_transform.png)

Na linha 4 a 8 é implementado o código para receber como argumentos a data ao qual o script irá extrair os dados.

Na linha 10 a 26 do script é iniciado uma instância da aplicação Spark como também a instrução SQL que aplica as transformações nos dados. Com intuito de simular a obtenção de alguma informação analítica do dado. O script aplica uma agregação dos dados de uma determinada data, especificada pelo cláusula `WHERE date = '%s'`. Agrupa pelo campo event_name e faz a contagem de cada tipo de evento.

Por fim, na linha 28 a 36 a instrução é de fato executada, e o resultado da transformação é persistido no Data Lake, porém em outra camada - de dados analíticos.

A Figura X apresenta a implementação da classe operador personalizado anteriormente citado, nomeado como StudyCaseOperator.

![Operador de extração de dados](./images/study_case_operator.png)

Na linha 4 a 16 é definido o construtor da classe operadora, ao qual são definidas variáveis iniciais contendo a data de execução do script, o contador de objetos e o endereço da API geradora de dados aleatórios.

Na linha 18 a 22 é definido o conjunto de códigos que realiza a chamada HTTP à API geradora de dados, passando como parâmetro a data e o contador de objetos definidos no construtor da classe. É utilizado o pacote requests nativo do Python.

Para a definição do código executor da classe operadora, na linha 24 a 31 é implementado o método execute que realiza a chamada HTTP a API e persiste o resultado da chamada no formato JSON na camada de dados brutos do HDFS.

Na Figura X é apresentado o script de transformação de dados no formato JSON para o formato Parquet, citado anteriormente na definição da segunda tarefa ETL.

![Script de conversão de JSON para Parquet](./images/json_to_parquet_operator.png)

Na linha 1 a 17 são definidas as variáveis contendo o caminho do arquivo JSON, o nome do banco de dados e tabela onde o dado Parquet será persistido, a data de execução do script e a instância da aplicação Spark.

Na linha 19 a 22 é iniciado a leitura do arquivo JSON, como também a adição de uma nova coluna contendo a data de execução do script, anteriormente definida. A partir da linha 23 a 30 é iniciado a persistência dos novos arquivos no formato Parquet, como também a especificação do nome do banco de dados, tabela e o caminho de onde os arquivos serão persistidos. Por fim, na linha 32 a aplicação Spark é finalizada.

Com o intuito de disponibilizar uma plataforma cloud native (nativa em nuvem) e atingir algumas das boas práticas de orquestração de containers do mercado, todos os componentes da arquitetura deste trabalho foram implantados utilizando a ferramenta Kubernetes. A Figura X apresenta o arquivo manifesto para fazer a implantação de um StatefulSet do componente Namenode HDFS.

![Arquivo manifesto do StatefulSet do componente Namenode HDFS](./images/namenode_statefulset.png)

### 3-7-2 ETL em tempo real

Como demonstração de um fluxo ETL em tempo real de ponta-a-ponta, implementou-se um fluxo de Clickstream utilizando a biblioteca PySpark. O objetivo do experimento foi enviar dados aleatórios para uma API HTTP, implementada na seção 3.5. A partir da API, os dados foram postados em um tópico Kafka ao qual, conectou-se uma aplicação Clickstream para receber os eventos e agrupa-los em uma janela de tempo definida de 5 segundos. A cada janela de tempo, os eventos foram agrupados e por fim contabilizado a quantidade de eventos de cada usuário na respectiva janela de tempo.

A seguir as Figuras X e Y apresentam o código da aplicação Clickstream separado em duas partes. O código da aplicação foi implementado utilizando a biblioteca PySpark juntamente com o framework Spark Structured Streaming.

![Script de iniciação da aplicação Clickstream](./images/clickstream_pt1.png)

![Script de processamento da aplicação Clickstream](./images/clickstream_pt2.png)

Na Figura X ao qual apresenta a primeira parte da aplicação, no trecho de código da linha 5 a 13 é definido a estrutura dos dados que são transmitidos no tópico Kafka utilizando a síntaxe de definição do formato Avro. Da linha 18 a 22 é instanciado a aplicação Spark que será executada. Da linha 24 a 30 é instanciado um objeto DataStreamReader ao qual são lidos e processados cada evento que é transmitido no tópico Kafka especificado na linha 29.

Na Figura X, no trecho de código apresentado da linha 32 a 40 é aplicado algumas transformações no evento recebido pelo DataStreamReader. Na linha 33 é removido caracteres mágicos e extraído a mensagem Avro convertida para JSON. Da linha 35 a 40 cada campo do objeto JSON é anexado a sua respectiva coluna contendo o nome do campo.

No trecho de código da linha 41 a 47 é aplicado a função de janelamento, onde cada janela contém eventos dentro de um período de 5 segundos. Tais eventos são agrupados pelas colunas event_name, page e username que por fim, é aplicado uma contagem da quantidade de eventos de cada grupo adicionando-se o campo start_date e start_time contendo respectivamente o ano-mês-dia e hora-minuto-segundo da janela.

Por fim, da linha 49 a 56 é criado uma instância do objeto DataStreamWriter, ao qual os dados processados anteriormente são preparados para serem persistidos no Data Lake, no formato Parquet e no caminho de arquivo especificado na linha 53.

Para a definição e criação da estrutura de dados dos eventos postados no tópico Kafka anteriormente citado, foi-se necessário criar um script capaz de criar a estrutura do dado no repositório de esquemas - Schema Registry. Na Figura X é apresentado o script de criação de esquemas no formato Avro.

![Script de criação de schema](./images/schema_creator.png)

No trecho de código da linha 5 a 23, é definido a estrutura do dado e o corpo da requisição de criação de esquema a ser enviado para a API do Schema Registry. Da linha 27 a 33 é realizado a chamada criação de esquema a API, passando como corpo da requisição a estrutura definida anteriormente.

Para fazer a postagem dos eventos na API HTTP citada na seção 3.5 utilizando o formato do dado anteriormente definido, criou-se um script apresentado na Figura X.

![Script de postagem de eventos na API](./images/spam_api_clickstream.png)

No trecho de código da linha 7 a 9 são definidos conjuntos de dados a serem sorteados por um número aleatório. Da linha 11 a 16 é definido o modelo do corpo da requisição a ser enviado a API citada na seção 3.5. Da linha 18 a 36 é definido um loop infinito, onde são sorteados aleatoriamente os dados anteriormente definidos. Com os dados sorteados, os campos do modelo do corpo da requisição são preenchidos e por fim, é feito a postagem da mensagem a API.

## 4 Resultados

Neste capítulo serão apresentados os resultados do desenvolvimento de uma plataforma para extração, transformação e disponibilização de dados dos estudo de casos anteriormente apresentados.

### 4-1 ETL em lote

Nesta seção serão apresentados os resultados obtidos a partir da criação de um fluxo ETL em lote implementado na seção 3.7.1.

A Figura X apresenta uma chamada HTTP feita na API geradora de dados aleatórios através do navegador. Na chamada são passados os parâmetros de data (date) e quantidade de objetos (count). A resposta retorna os dados necessários para realizar as transformações posteriores.

![Requisição HTTP na API geradora de dados](./images/api_random_data.png)

Na Figura X é apresentado a representação gráfica da DAG no Airflow implementada na seção 3.7.1. Na figura é possível visualizar a 3 tarefas que compõem o fluxo ETL e também que todas as tarefas foram executadas com sucesso, representado pela borda na cor verde como também o marcador success.

![Representação gráfica da DAG ETL](./images/airflow_run_dags.png)

Navegando pelo painel de tarefas do Airflow, é possível visualizar os logs das execuções de tais tarefas. Na Figura X é apresentado os logs da primeira tarefa, ao qual é possível visualizar a resposta retornada da chamada a API de geração de dados como também uma mensagem mencionando onde o arquivo resultado será persistido no Data Lake.

![Painel de logs do Airflow](./images/airflow_logs.png)

Na página web contendo o painel do Spark, é possível visualizar o histórico das aplicações executadas como também suas respectivas métricas, as aplicações em execução e também as instâncias executoras do Spark, os Workers. Na Figura X é apresentado o histórico de aplicações executadas a partir das invocações feita pelo Airflow.

![Aplicação web do Spark e histórico de execuções](./images/spark_ui_jobs.png)

Como resultado da primeira tarefa, os dados extraídos da API são persistidos no Data Lake, na camada de dados brutos. Nas Figuras X e X são apresentados as partições, ou seja, os dados da execução de cada dia em específico, como também o arquivo result.json contendo os dados extraídos por uma execução.

![Camada de dados brutos particionado pela data](./images/hdfs_raw_layer.png)

![Dado bruto persistido na camada de dados brutos](./images/hdfs_partition_raw_layer.png)

Na Figura X é apresentado os dados persistidos pela tarefa de transformação do dado bruto para o formato Parquet. É possível observar que os dados estão persistidos em outra camada, nomeada como trusted e também que o caminho do arquivo leva o nome da tabela Hive que foi criada "study_case.insights".

![Dado persistido no formato Apache Parquet](./images/hdfs_partition_trusted_layer.png)

Como resultado da execução da terceira tarefa, a de agregação dos dados, um novo arquivo Parquet é persistido no Data Lake. Na Figura X é possível observar que os dados são persistidos na mesma camada trusted, porém em outro caminho de arquivo ao qual leva o nome da tabela Hive que foi criada "study_case.grouped_insights".

![Dado persistido no formato Apache Parquet](./images/hdfs_trusted_grouped_insights.png)

Na Figura X e X são apresentados respectivamente instruções SQLs para consultar os dados persistidos nas tabelas criadas pela segunda e terceira tarefa. As tabelas levam o nome de insights e grouped_insights, ao qual a insights contém apenas os dados convertidos do formato JSON para Parquet. A tabela grouped_insights contém os dados agrupados pelos campos anteriormente citados na seção 3.7.1. As consultas foram feitas através da ferramenta SQL Pad.

![Consulta SQL na tabela insights](./images/sql_pad_insights_table.png)

![Consulta SQL na tabela grouped_insights](./images/sql_pad_grouped_insights_table.png)

### 4-2 ETL em tempo real (Clickstream)

Nesta seção serão apresentados os resultados obtidos a partir da criação de um fluxo ETL em tempo real implementado na seção 3.7.2, nomeada como Clickstream.

Na Figura X é apresentado a execução do script para criação do esquema no formato Avro dos eventos que são postados na API apresentada anteriormente na seção 3.5. Na figura é possível observar que o corpo completo do esquema é mostrado como saída da execução do script como também os identificadores no repositório de esquemas. O esquema criado foi nomeado como appclickstream.

![Resultado script de criação do esquema dos eventos Avro](./images/script_create_schema.png)

Na Figura X é apresentado a execução do script que realiza chamadas HTTP na API anteriormente citada para a postagem dos eventos no respectivo tópico Kafka. O script foi invocado passando como parâmetro o nome do esquema criado anteriormente e, como segundo parâmetro um número indicando o tempo de espera entre cada chamada a API. O script realiza infinitas chamadas, mas para fins de testes a execução foi interrompida.

![Resultado script de postagem de eventos na API](./images/script_spam_api.png)

A partir das postagens realizadas na API HTTP consequentemente no tópico Kafka, a aplicação Spark Structured Streaming passa a realizar o processamento dos eventos que são entregues pelo tópico Kafka. A Figura X e X apresentam algumas métricas fornecidas pelo próprio Spark, como por exemplo, o número de eventos e linhas processadas, a duração de cada registro processado etc.

![Métricas de execução da aplicação Clickstream - Parte 1](./images/app_clickstream_pt1.png)

![Métricas de execução da aplicação Clickstream - Parte 2](./images/app_clickstream_pt2.png)

A Figura X apresenta os dados processados e persistidos pela aplicação Clickstream no Data Lake. Os dados foram particionados por tipo de evento e armazenado em sub-pastas individuais. As partições levam o prefixo event_name= e por fim o nome do evento, click, scroll ou submit.

![Dados processados pelo Clickstream persistidos no Data Lake](./images/clickstream_hdfs.png)

A Figura X apresenta os dados da Figura X em um formato consultável e acessível via uma tabela Hive - tabela dumping.clickstream. Na figura é apresentado a consulta SQL ao qual retorna os dados agrupados pelas colunas username, page, event_name juntamente com a quantidade de eventos respectivos a cada agrupamento, apresentado na coluna count.

![Tabela Hive contendo os dados persistidos pela aplicação Clickstream](./images/clickstream_table.png)

### 4-3 Painel Kubernetes

Na Figura X é ilustrado um painel que apresenta os componentes (pods e containers) implantados no cluster Kubernetes. O painel apresenta uma tabela contendo o nome do pod e algumas métricas, como por exemplo, a utilização média e máxima de CPU de cada pod. Com este painel tornou-se possível visualizar métricas de consumo de hardware e logs gerado pelas aplicações do ecossistema da plataforma.

![Painel de métricas do Kubernetes](./images/kubernetes_panel.png)

## 5 Considerações finais

Neste capítulo serão apresentadas as contribuições e conclusões deste trabalho,
assim como os trabalhos futuros.

### 5-1 Contribuições e Conclusões

A plataforma de extração, transformação e disponibilização de dados em tempo real e lote apresentado neste trabalho cumpre com o objetivo de disponibilizar uma plataforma ao qual engenheiros de dados podem implementar scripts e aplicações para realizar extrações e transformações massivas em dados disponibilizados, por exemplo, por banco de dados, APIs HTTP, arquivos de texto etc.

Com o uso restrito e total de apenas ferramentas de código aberto neste trabalho, foi possível construir uma plataforma com zero custo financeiro, como por exemplo, a não necessidade da compra de licenças de softwares. Além de que, com a utilização das ferramentas aplicadas neste trabalho permitiu a possibilidade da implementação de códigos personalizados nas próprias ferramentas, como também a contribuição de tais códigos para o projeto oficial finalizando como contribuição para a comunidade de código aberto. Neste trabalho também foi possível implementar uma plataforma cloud native e pronta para ser portada para um ambiente produtivo com a ferramenta Kubernetes, aproveitando-se dos principais benefícios de portabilidade e gerenciamento de aplicações na nuvem que esta ferramenta provê.

A fundamentação técnica e desenvolvimento apresentado neste trabalho contribuiu para decisões técnicas aplicadas em um time de engenharia de dados, ao qual utilizou-se como base o conteúdo apresentado na seção 3.7.2 para a construção de uma aplicação Clickstream juntamente com o componente de persistência de dados e metadados apresentados nas seções 3.3 e 3.4. Como resultado, foi possível implementar uma ferramenta de captura de dados em tempo real indicando o comportamento de usuários suportando decisões de negócio por parte de times de análise de dados e marketing. Tal implementação também contribuiu para a redução do uso de ferramentas de rastreamento, como Google Analytics, que por fim resultou na redução de custos.

### 5-2 Trabalhos futuros

Este trabalho não encerra as pesquisas no desenvolvimento de uma plataforma para extração, transformação e disponibilização de dados em tempo real e lote, mas abre a oportunidade para os seguintes trabalhos futuros:

- Aplicar práticas e técnicas para atingir a separação de contextos de dados utilizando-se camadas com escopos definidos dentro do Data Lake.
- Utilizar ferramentas, como por exemplo Apache Ranger, para o gerenciamento de níveis de acessos aos dados persistidos no Data Lake.
- Com relação à aplicações em tempo real que a latência e o tempo de processamento são requisitos críticos, a ferramenta Spark Strucuted Streaming pode se tornar um gargalo. Outra ferramenta especialista em processamento em tempo real, como por exemplo Apache Flink, pode ser uma candidata a substituição.
- É interessante aplicar um novo formato de dados, como por exemplo Apache Hudi ou Delta Lake, para a possibilidade de operações atualização-inserção (upsert) e alteração (update), já que o formato Apache Parquet não atende à essas necessidades.

## Referências

DIGITAL, Tail. **O que é Customer Data Platform (CDP) e porque você precisa de uma**. Disponível em: https://blog.tail.digital/o-que-e-customer-data-platform-e-porque-voce-precisa-de-um Acesso em: 30/03/2021.

REDHAT. **What is a data lake?**. Disponível em: https://www.redhat.com/en/topics/data-storage/what-is-a-data-lake Acesso em: 30/03/2021.

REDHAT. **Understanding big data**. Disponível em: https://www.redhat.com/en/topics/big-data Acesso em: 30/03/2021.

IBM. **What is ETL (Extract, Transform, Load)?**. Disponível em: https://www.ibm.com/cloud/learn/etl Acesso em: 06/04/2021.

AIRFLOW, Apache. **Apache Airflow Documentation**. Disponível em: https://airflow.apache.org/docs/apache-airflow/stable/index.html Acesso em: 06/04/2021.

SPARK, Apache. **Apache Spark™ - Unified Engine for large-scale data analytics**. Disponível em: http://spark.apache.org/ Acesso em: 06/04/2021.

HIVE, Apache. **Apache Hive - Apache Software Foundation**. Disponível em: https://cwiki.apache.org/confluence/display/Hive/Home Acesso em: 06/04/2021.

KAFKA, Apache. **Apache Kafka Documentation**. Disponível em: https://kafka.apache.org/documentation/ Acesso em: 06/04/2021.

KAFKA, Apache. **Apache Kafka**. Disponível em: https://kafka.apache.org/ Acesso em: 06/04/2021.

TRINO. **Overview - Trino Documentation**. Disponível em: https://trino.io/docs/current/overview.html Acesso em: 06/04/2021.

TRINO. **Use Cases - Trino Documentation**. Disponível em: https://trino.io/docs/current/overview/use-cases.html Acesso em: 06/04/2021.

IBM. **What is HDFS?**. Disponível em: https://www.ibm.com/analytics/hadoop/hdfs Acesso em: 12/04/2021.

PARQUET, Apache. **Apache Parquet**. Disponível em: https://parquet.apache.org/ Acesso em: 13/04/2021.

SPICIER, Thomas. **Apache Parquet: How to be a hero with the open-source columnar data format**. Disponível em: https://blog.openbridge.com/how-to-be-a-hero-with-powerful-parquet-google-and-amazon-f2ae0f35ee04 Acesso em: 13/04/2021.

IBM. **What is Avro?**. Disponível em: https://www.ibm.com/analytics/hadoop/avro Acesso em: 13/04/2021.

SHEN, Catherine. **Why you should use Avro and schema registry for your streaming application**. Disponível em: https://catherine-shen.medium.com/why-you-should-use-avro-and-schema-registry-for-your-streaming-application-2f24dcf017c8 Acesso em: 13/04/2021.

CONFLUENT. **Schema Registry Overview**. Disponível em: https://docs.confluent.io/platform/current/schema-registry/index.html Acesso em: 08/05/2021.

IBM. **What is distributed computing**. Disponível em: https://www.ibm.com/docs/ko/txseries/8.1.0?topic=overview-what-is-distributed-computing Acesso em: 08/05/2021.

POWIS, Owen. **What is Clickstream data?**. Disponível em: https://www.wordtracker.com/blog/keyword-research/what-is-clickstream-data Acesso em: 22/05/2021.

SPARK, Apache. **Structured Streaming Programming Guide**. Disponível em: https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html Acesso em: 25/05/2021.

RAY, Amit. **Hadoop architecture in big data Yarn HDFS and MapReduce**. Disponível em: https://amitray.com/hadoop-architecture-in-big-data-yarn-hdfs-and-mapreduce/ Acesso em: 15/08/2021.

DOCKER. **Docker overview**. Disponível em: https://docs.docker.com/get-started/overview/ Acesso em: 04/10/2021.

KUBERNETES. **Kubernetes Overview**. Disponível em: https://kubernetes.io/ Acesso em: 11/10/2021.
