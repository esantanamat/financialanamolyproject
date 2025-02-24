variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "FinancialExpenses"
}

variable "billing_mode" {
  description = "Billing mode for DynamoDB"
  type        = string
  default     = "PAY_PER_REQUEST"
}

variable "table_attributes" {
  description = "List of attributes for the DynamoDB table"
  type = list(object({
    name = string
    type = string
  }))
  default = [
    { name = "date_transaction_id", type = "S" },
    { name = "transaction_id", type = "S" },
    { name = "name", type = "S" },
    { name = "cost", type = "N" },
    { name = "category", type = "S" },
    { name = "flagged", type = "S" },
    { name = "user_id", type = "S" },
    { name = "date", type = "S" }
  ]
}

variable "global_secondary_indexes" {
  description = "List of global secondary indexes"
  type = list(object({
    name            = string
    hash_key        = string
    projection_type = string
  }))
  default = [
    { name = "TransactionIndex", hash_key = "transaction_id", projection_type = "ALL" },
    { name = "DateIndex", hash_key = "date", projection_type = "ALL" },
    { name = "CategoryIndex", hash_key = "category", projection_type = "ALL" },
    { name = "CostIndex", hash_key = "cost", projection_type = "ALL" },
    { name = "FlaggedIndex", hash_key = "flagged", projection_type = "ALL" },
    { name = "NameIndex", hash_key = "name", projection_type = "ALL" }
  ]
}

variable "dynamodb_tags" {
  description = "Tags for the DynamoDB table"
  type        = map(string)
  default = {
    Name        = "expenses-table"
    Environment = "dev"
  }
}
