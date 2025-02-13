provider "aws" {
  region = "us-east-1"
}

resource "aws_dynamodb_table" "expenses-table" {
  name           = "FinancialExpenses"
  billing_mode   = "PAY_PER_REQUEST"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "user_id"
  range_key      = "date"

  attribute {
    name = "transaction_id"
    type = "S"
  }

  attribute {
    name = "name"
    type = "S"
  }

  attribute {
    name = "cost"
    type = "N"
  }

  attribute {
    name = "category"
    type = "S"
  }

  attribute {
    name = "flagged"
    type = "B"
  }
  attribute {
    name = "user_id"
    type = "S"
  }
  attribute {
    name = "date"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }


  global_secondary_index {
    name            = "TransactionIndex"
    hash_key        = "transaction_id"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }


  global_secondary_index {
    name            = "CategoryIndex"
    hash_key        = "category"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }


  global_secondary_index {
    name            = "CostIndex"
    hash_key        = "cost"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }


  global_secondary_index {
    name            = "FlaggedIndex"
    hash_key        = "flagged"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }


  global_secondary_index {
    name            = "NameIndex"
    hash_key        = "name"
    projection_type = "ALL"
    read_capacity   = 10
    write_capacity  = 10
  }



  tags = {
    Name        = "expenses-table"
    Environment = "dev"
  }
}
