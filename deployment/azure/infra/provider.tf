terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.54.0"
    }

    azapi = {
      source = "Azure/azapi"
    }
  }
}