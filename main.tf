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

resource "aws_iam_role_policy" "ecr_lambda_policy" {
  name        = "lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:UpdateItem",
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
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
        "Resource": "${aws_lambda_function.financial_anomaly_detection.arn}"
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

# resource "aws_lambda_function" "detect_anomalies" {
#   function_name    = "detect_anomalies_function"
#   runtime          = "python3.8"
#   role             = aws_iam_role.lambda_role.arn
#   handler          = "detect_anomalies.lambda_handler"
#   filename         = "detect_anomalies_function.zip"
#   source_code_hash = filebase64sha256("detect_anomalies_function.zip")
 
# }

# resource "aws_lambda_layer_version" "dependencies_layer_v1" {
#   s3_bucket           = aws_s3_bucket.lambda_layer_bucket.bucket
#   s3_key              = aws_s3_bucket_object.lambda_layer_zip1.key
#   layer_name          = "dependencies_layer_v1"  
#   compatible_runtimes = ["python3.9", "python3.8"]
#   description         = "Lambda layer with external dependencies for the detect_anomalies function (v1)"

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# resource "aws_lambda_layer_version" "dependencies_layer_v2" {
#   s3_bucket           = aws_s3_bucket.lambda_layer_bucket.bucket
#   s3_key              = aws_s3_bucket_object.lambda_layer_zip2.key
#   layer_name          = "dependencies_layer_v2"  # Unique name for the next version
#   compatible_runtimes = ["python3.9", "python3.8"]
#   description         = "Lambda layer with external dependencies for the detect_anomalies function (v2)"

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# resource "aws_s3_bucket_policy" "bucket_policy" {
#   bucket = aws_s3_bucket.pkl_model.bucket

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Principal = {
#           Service = "sagemaker.amazonaws.com"
#         }
#         Action = "s3:GetObject"
#         Resource = "arn:aws:s3:::${aws_s3_bucket.pkl_model.bucket}/*"
#       }
#     ]
#   })
# }

# resource "aws_s3_bucket" "pkl_model" {
#   bucket = "my-lambda-layer-bucket-126815st43"
  
#   tags = {
#     Name        = "My bucket"
#     Environment = "Dev"
#   }
# }


# resource "aws_s3_bucket_object" "anomaly_model" {
#   bucket = aws_s3_bucket.pkl_model.bucket
#   key    = "anomaly_model.pkl"
#   source = "anomaly_model.pkl"
  
# }

# resource "aws_s3_bucket_object" "lambda_layer_zip2" {
#   bucket = aws_s3_bucket.lambda_layer_bucket.bucket
#   key    = "lambda-layer-2.zip"
#   source = "lambda-layer-2.zip"
#   acl    = "private"
# }

resource "aws_lambda_function" "financial_anomaly_detection" {
  function_name = "detect_anomalies_function"
  package_type  = "Image"

  image_uri = "463470969308.dkr.ecr.us-east-1.amazonaws.com/my-lambda-container:latest"
  
  role = aws_iam_role.lambda_role.arn
}
