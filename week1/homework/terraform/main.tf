terraform {
  required_version = ">= 1.0"
  backend "gcs" {
    bucket = "a6ece7e1a712dc39-bucket-tfstate"
  } 
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.22"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}



# bucket for terraform backend

# resource "random_id" "bucket_prefix" {
#   byte_length = 8
# }

# resource "google_storage_bucket" "backend_bucket" {
#   name          = "${random_id.bucket_prefix.hex}-bucket-tfstate"
#   force_destroy = false
#   location      = "ME-WEST1"
#   storage_class = "STANDARD"
#   versioning {
#     enabled = true
#   }
#   lifecycle_rule {
#     condition {
#       num_newer_versions = 5
#     }
#     action {
#       type = "Delete"
#     }
#   }
# }



# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location = var.location

  # Optional, but recommended settings:
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.location
}
