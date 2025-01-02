# Capstone-Final_Project
Designing an Automatic Data Collection and Storage System with AWS Lambda and Slack Integration for Server Availability Monitoring and Slack Notification.

Problem Statement:
The task is to create an AWS Lambda function that periodically fetches data from an API and stores it in an Amazon RDS instance. The function should be triggered by an Amazon CloudWatch Event every 15 seconds, and an alert should be sent to a Slack channel if the server goes down.

Technologies Used:
AWS Lambda, Amazon RDS, CloudWatch, Slack API.

Project Workflow:
This project involves creating a fully automated data pipeline using AWS Lambda to periodically fetch data from an external API and store it in an Amazon RDS database. The project also includes monitoring the health of the API server using CloudWatch and sending alerts to a Slack channel if the server is down.

Task performed to complete the project:
1. Set Up Amazon RDS Instance - Create an Amazon RDS instance (e.g., PostgreSQL or MySQL). Configure the instance's security group to allow connections from AWS Lambda.
2. Create an AWS Lambda Function - The Lambda function will: Fetch data from the API using the requests library. Insert the fetched data into the Amazon RDS database using a database driver (e.g., psycopg2 for PostgreSQL).
3. Schedule the Lambda Function with CloudWatch - Set up a CloudWatch Event Rule to trigger the Lambda function every 15 seconds.
4. Monitor API Availability - Use CloudWatch to log the Lambda function’s performance and API server status. If the API server is down, log an error and trigger an alert.
5. Send Alerts to Slack - Use the Slack API to send alerts when the API server goes down.
