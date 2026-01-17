# 1. Definição do Provider (GCP)
provider "google" {
  project = var.project_id
  region  = var.region
}

# 2. Bucket para o Data Lake (Camadas Bronze, Silver, Gold)
resource "google_storage_bucket" "datalake_nyc_taxi" {
  name          = "${var.project_id}-datalake"
  location      = var.region
  force_destroy = true # Permite deletar o bucket mesmo com arquivos (útil para testes)

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete" # Exemplo de gestão de custo: deleta arquivos após 30 dias se necessário
    }
  }
}

# 3. Estrutura do Data Warehouse (BigQuery)
resource "google_bigquery_dataset" "gold_layer" {
  dataset_id                  = "nyc_taxi_gold"
  friendly_name               = "NYC Taxi Gold Layer"
  description                 = "Tabelas dimensionais finais para consumo de BI"
  location                    = var.region
  delete_contents_on_destroy = true
}

# 4. Service Account para o Pipeline
resource "google_service_account" "pipeline_sa" {
  account_id   = "taxi-pipeline-svc"
  display_name = "Service Account para execução do Job PySpark"
}

# 5. Roles e Permissões (IAM)
# Permissão para ler/escrever no Storage
resource "google_storage_bucket_iam_member" "sa_storage_admin" {
  bucket = google_storage_bucket.datalake_nyc_taxi.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# Permissão para editar o BigQuery
resource "google_project_iam_member" "sa_bq_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}