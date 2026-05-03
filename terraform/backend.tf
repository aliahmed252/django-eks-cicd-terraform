terraform {
  backend "s3" {
    bucket = "final-project-bucket-123"
    key    = "malerator-project/terraform.tfstate"
    region = "us-east-1"


  }
}
