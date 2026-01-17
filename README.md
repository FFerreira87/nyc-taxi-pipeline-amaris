# NYC Taxi Data Pipeline - Senior Data Engineering Challenge

Este repositório contém uma solução completa de engenharia de dados para o processamento dos dados de viagens dos táxis de Nova Iorque (NYC TLC). A arquitetura segue o padrão **Medallion (Bronze, Silver, Gold)** e utiliza **Terraform** para provisionamento de infraestrutura na **GCP**.

---

## 🏗 Arquitetura da Solução

A solução foi desenhada para ser escalável e resiliente, utilizando:
* **Armazenamento:** Google Cloud Storage (GCS) como Data Lake.
* **Processamento:** PySpark para transformações distribuídas.
* **Data Warehouse:** BigQuery para a camada Gold (Modelo Dimensional).
* **IaC:** Terraform para gestão de recursos e IAM.

### Fluxo de Dados:
1. **Bronze (Ingestion):** Ingestão de arquivos brutos (Parquet/CSV) com adição de metadados de auditoria.
2. **Silver (Processing):** Limpeza de dados, filtragem de anomalias (valores negativos/zero) e enriquecimento via *Broadcast Join*.
3. **Gold (Curated):** Modelagem Dimensional (*Star Schema*) com tabelas particionadas e clusterizadas.

---

## 🛠️ Tecnologias Utilizadas
* **Python / PySpark**
* **Terraform** (Provider: Google Cloud)
* **Google Cloud Platform** (GCS e BigQuery)
* **Parquet** (Formato de armazenamento otimizado)

---

## 📂 Estrutura do Projeto
```text
├── scripts/
│   ├── bronze_ingestion.py      
│   ├── silver_transformation.py 
│   └── gold_transformation.py   
├── terraform/
│   ├── main.tf                 
│   └── variables.tf            
├── architecture/
│   └── diagram.png             
└── README.md