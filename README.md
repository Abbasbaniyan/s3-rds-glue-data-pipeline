# S3 to RDS with AWS Glue Fallback

## Overview

This project is a Dockerized Python application that reads customer data from an Amazon S3 bucket and uploads it to an Amazon RDS MySQL database.

If the RDS connection fails, the application automatically uses AWS Glue as a fallback and registers the S3 CSV data in the AWS Glue Data Catalog.

## Architecture

S3 Bucket
   |
   | customers.csv
   v
Dockerized Python Application
   |
   |--------------------|
   |                    |
   v                    v
Amazon RDS          AWS Glue
MySQL               Data Catalog
   |                    |
   v                    v
customers          customers_fallback


## AWS Services Used

- Amazon S3
- Amazon RDS MySQL
- AWS Glue Data Catalog
- AWS IAM
- Amazon EC2/RDS networking
- AWS CLI

## Technologies Used

- Python
- Pandas
- SQLAlchemy
- PyMySQL
- Boto3
- Docker
- Git & GitHub

## Project Structure


s3-rds-glue-data-pipeline/
│
├── app.py
├── customers.csv
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
## Screenshots

### 1. S3 CSV Object

<img width="1891" height="867" alt="Screenshot 2026-08-10 203419" src="https://github.com/user-attachments/assets/8db3ab06-2018-4246-a23d-80a89cbbc315" />


### 2. Docker to RDS Successful Ingestion

<img width="1003" height="265" alt="Screenshot 2026-08-10 203453" src="https://github.com/user-attachments/assets/924a3922-106b-4467-8eeb-17f91de6dc1f" />


### 3. RDS Records

<img width="1022" height="303" alt="Screenshot 2026-08-10 203513" src="https://github.com/user-attachments/assets/bd171b21-b0b6-4b7a-a569-54a2cb0e7ae2" />


### 4. AWS Glue Fallback Table

<img width="1897" height="912" alt="Screenshot 2026-08-10 203559" src="https://github.com/user-attachments/assets/e4b6e2e7-16c1-4c63-b8f1-0db267f2398e" />


### 5. Project Files

<img width="375" height="381" alt="Screenshot 2026-08-10 203619" src="https://github.com/user-attachments/assets/298b9cfe-4dce-4a1b-8391-77160beb9b14" />
