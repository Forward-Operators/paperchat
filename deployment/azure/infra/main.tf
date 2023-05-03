terraform {
  required_version = ">= 1.3"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.54.0"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {
}

resource "random_string" "resource_prefix" {
  length  = 6
  special = false
  upper   = false
  numeric = false
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.resource_prefix != "" ? var.resource_prefix : random_string.resource_prefix.result}${var.resource_group_name}"
  location = var.location
  tags     = var.tags
}

module "log_analytics_workspace" {
  source              = "./modules/log_analytics"
  name                = "${var.resource_prefix != "" ? var.resource_prefix : random_string.resource_prefix.result}${var.log_analytics_workspace_name}"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = var.tags
}

module "application_insights" {
  source              = "./modules/application_insights"
  name                = "${var.resource_prefix != "" ? var.resource_prefix : random_string.resource_prefix.result}${var.application_insights_name}"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = var.tags
  application_type    = var.application_insights_application_type
  workspace_id        = module.log_analytics_workspace.id
}

module "virtual_network" {
  source                       = "./modules/virtual_network"
  resource_group_name          = azurerm_resource_group.rg.name
  vnet_name                    = "${var.resource_prefix != "" ? var.resource_prefix : random_string.resource_prefix.result}${var.vnet_name}"
  location                     = var.location
  address_space                = var.vnet_address_space
  tags                         = var.tags
  log_analytics_workspace_id   = module.log_analytics_workspace.id
  log_analytics_retention_days = var.log_analytics_retention_days

  subnets = [
    {
      name : var.aca_subnet_name
      address_prefixes : var.aca_subnet_address_prefix
      private_endpoint_network_policies_enabled : true
      private_link_service_network_policies_enabled : false
    },
    {
      name : var.private_endpoint_subnet_name
      address_prefixes : var.private_endpoint_subnet_address_prefix
      private_endpoint_network_policies_enabled : true
      private_link_service_network_policies_enabled : false
    }
  ]
}

module "blob_private_dns_zone" {
  source              = "./modules/private_dns_zone"
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.rg.name
  virtual_networks_to_link = {
    (module.virtual_network.name) = {
      subscription_id     = data.azurerm_client_config.current.subscription_id
      resource_group_name = azurerm_resource_group.rg.name
    }
  }
}

module "blob_private_endpoint" {
  source                         = "./modules/private_endpoint"
  name                           = "${title(module.storage_account.name)}PrivateEndpoint"
  location                       = var.location
  resource_group_name            = azurerm_resource_group.rg.name
  subnet_id                      = module.virtual_network.subnet_ids[var.private_endpoint_subnet_name]
  tags                           = var.tags
  private_connection_resource_id = module.storage_account.id
  is_manual_connection           = false
  subresource_name               = "blob"
  private_dns_zone_group_name    = "BlobPrivateDnsZoneGroup"
  private_dns_zone_group_ids     = [module.blob_private_dns_zone.id]
}

module "storage_account" {
  source              = "./modules/storage_account"
  name                = lower("${var.resource_prefix != "" ? var.resource_prefix : random_string.resource_prefix.result}${var.storage_account_name}")
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = var.tags
  account_kind        = var.storage_account_kind
  account_tier        = var.storage_account_tier
  replication_type    = var.storage_account_replication_type
}

module "container_apps" {
  source                   = "./modules/container_apps"
  managed_environment_name = "${var.resource_prefix != "" ? var.resource_prefix : random_string.resource_prefix.result}${var.managed_environment_name}"
  location                 = var.location
  resource_group_name      = azurerm_resource_group.rg.name
  tags                     = var.tags
  infrastructure_subnet_id = module.virtual_network.subnet_ids[var.aca_subnet_name]
  instrumentation_key      = module.application_insights.instrumentation_key
  workspace_id             = module.log_analytics_workspace.id
  dapr_components = [{
    name           = var.dapr_name
    component_type = var.dapr_component_type
    version        = var.dapr_version
    ignore_errors  = var.dapr_ignore_errors
    init_timeout   = var.dapr_init_timeout
    secret = [
      {
        name  = "storageaccountkey"
        value = module.storage_account.primary_access_key
      }
    ]
    metadata : [
      {
        name  = "accountName"
        value = module.storage_account.name
      },
      {
        name  = "containerName"
        value = var.container_name
      },
      {
        name        = "accountKey"
        secret_name = "storageaccountkey"
      }
    ]
    scopes = var.dapr_scopes
  }]
  container_apps = var.container_apps
}