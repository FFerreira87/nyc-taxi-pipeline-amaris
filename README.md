NYC Taxi Data Pipeline - Senior Data Engineering Challenge
Este repositório contém uma solução completa de engenharia de dados para o processamento dos dados de viagens dos táxis de Nova Iorque (NYC TLC). A arquitetura segue o padrão Medallion (Bronze, Silver, Gold) e utiliza Terraform para provisionamento de infraestrutura na GCP.

🏗 Arquitetura da Solução
A solução foi desenhada para ser escalável e resiliente, utilizando:

Armazenamento: Google Cloud Storage (GCS) como Data Lake.

Processamento: PySpark para transformações distribuídas.

Data Warehouse: BigQuery para a camada Gold (Modelo Dimensional).

IaC: Terraform para gestão de recursos e IAM.

Fluxo de Dados:
Bronze (Ingestion): Ingestão de arquivos brutos (Parquet/CSV) com adição de metadados de auditoria.

Silver (Processing): Limpeza de dados, filtragem de anomalias (valores negativos/zero) e enriquecimento via Broadcast Join com a tabela de zonas.

Gold (Curated): Modelagem Dimensional (Star Schema) com tabelas particionadas e clusterizadas no BigQuery.

🛠️ Tecnologias Utilizadas
Python / PySpark

Terraform (Provider: Google Cloud)

Google Cloud Platform (GCS e BigQuery)

Parquet (Formato de armazenamento otimizado)

📂 Estrutura do Projeto
Plaintext

├── scripts/
│   ├── bronze_ingestion.py      # Job 1: Raw to Bronze
│   ├── silver_transformation.py # Job 2: Bronze to Silver (Cleaning & Join)
│   └── gold_transformation.py   # Job 3: Silver to Gold (Dimensional Modeling)
├── terraform/
│   ├── main.tf                 # Recursos GCP (Storage, BQ, IAM)
│   └── variables.tf            # Parametrização do ambiente
├── architecture/
│   └── diagram.png             # Desenho da arquitetura
└── README.md

🚀 Como Executar
1. Infraestrutura (Terraform)
Para provisionar o ambiente na GCP:

Bash

cd terraform
terraform init
terraform plan
terraform apply

2. Pipeline de Dados (Local)
Certifique-se de ter o pyspark instalado e o JAVA_HOME configurado.

Bash

# Execute os jobs na ordem da arquitetura medalhão
python scripts/bronze_ingestion.py
python scripts/silver_transformation.py
python scripts/gold_transformation.py

📈 Decisões de Engenharia (Visão Sênior)
Modelagem Dimensional (Gold)
Fact_Trips: Particionada por pickup_date para otimizar consultas temporais e reduzir custos de scan no BigQuery.

Dim_Zones: Criada a partir do cruzamento com o Zone Lookup para facilitar a análise por bairro (Borough) sem necessidade de joins custosos em tempo de execução de BI.

Performance & Otimização
Utilização de Broadcast Join na camada Silver para a tabela de zonas, visto que é uma tabela pequena (Lookup), evitando o shuffle de rede no Spark.

Uso do formato Parquet com compressão Snappy para reduzir o footprint de armazenamento e acelerar a leitura de colunas específicas.

Estratégia de Dados Históricos
A pipeline foi construída utilizando o conceito de Idempotência. Os jobs de escrita utilizam o modo overwrite baseado em partições. Isso permite que qualquer período histórico possa ser reprocessado manualmente apenas re-executando o job para o arquivo de origem correspondente, sem gerar duplicidade no Data Warehouse.

👤 Autor
Fabio M Ferreira - Senior Data Engineer Candidate