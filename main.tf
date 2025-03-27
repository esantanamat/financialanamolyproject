provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "expenses_table" {
  name         = var.dynamodb_table_name
  billing_mode = var.billing_mode
  hash_key     = "user_id"
  range_key    = "date_transaction_id"

  dynamic "attribute" {
    for_each = var.table_attributes
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

  dynamic "global_secondary_index" {
    for_each = var.global_secondary_indexes
    content {
      name            = global_secondary_index.value.name
      hash_key        = global_secondary_index.value.hash_key
      projection_type = global_secondary_index.value.projection_type
    }
  }

  tags = var.dynamodb_tags
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ],
        "Effect": "Allow",
        "Resource": "${aws_dynamodb_table.expenses_table.arn}"
      }
    ]
  }
  EOF
}
resource "aws_iam_role_policy" "lambda_stream" {
  name   = "lambdastreampolicy"
  role   = aws_iam_role.lambda_role.id
  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "dynamodb:DescribeStream",
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:ListStreams"
        ],
        "Effect": "Allow",
        "Resource": "arn:aws:dynamodb:us-east-1:463470969308:table/FinancialExpenses/stream/2025-02-24T01:18:35.204"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy" "lambda_s3_read" {
  name   = "lambda_s3_read"
  role   = aws_iam_role.lambda_role.id
  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:GetObject"
        ],
        "Effect": "Allow",
        "Resource": ["arn:aws:s3:::mypklbucket12612"]
      }
    ]
  }
  EOF
}
resource "aws_iam_role_policy" "lambda_invoke" {
  name   = "lambda_invoke"
  role   = aws_iam_role.lambda_role.id
  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "lambda:InvokeFunction"
        ],
        "Effect": "Allow",
        "Resource": "${aws_lambda_function.detect_anomalies.arn}"
      }
    ]
  }
  EOF
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF
}



resource "aws_lambda_function" "add_transaction" {
  function_name    = "add_transaction_function"
  runtime          = "python3.13"
  role             = aws_iam_role.lambda_role.arn
  handler          = "add_transaction.lambda_handler"
  filename         = "add_transaction_function.zip"
  source_code_hash = filebase64sha256("add_transaction_function.zip")
}

resource "aws_lambda_function" "detect_anomalies" {
  function_name    = "detect_anomalies_function"
  runtime          = "python3.13"
  role             = aws_iam_role.lambda_role.arn
  handler          = "detect_anomalies.lambda_handler"
  filename         = "detect_anomalies_function.zip"
  source_code_hash = filebase64sha256("detect_anomalies_function.zip")
}
