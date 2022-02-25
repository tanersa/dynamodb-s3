# S3 Storage to DynamoDB Data Transfer

**AWS DynamoDB Service**

In which scenario we need **non-relational database** table?

Let's say we have S3 bucket and whenever upload event happens to S3 bucket, we would like to automatically take that json file and parse it then place
it in DynamoDB Table for consistency. 

Therefore, if we would like to query in the future to retrieve the data we can achieve our goal. Since json file is a flat file (non-relational) we are going to use
DynamoDB Table. Based on the use case, one also can store the data in **Relational DBs** such as **PostGres, MySQL, Oracle SQL,** or **PL/SQL developer.** 

**Advantages of DynamoDB as follows:**
   -  Delivers single-digit millisecond performance at any scale.
   -  Supports tables of virtually any size.
   -  No maintenance since DynamoDB is serverless.
   -  DynamoDB encrypts data at rest by default using encryption keys stored in AWS KMS whereas RDS encrypts your databases using keys you manage through AWS KMS.         With encryption enabled, data stored at rest is encrypted.

It would truely be cumbersome to fetch the data directly from S3 bucket since you have to go to file and fetch the data one by one. User can not query to get the data from S3 bucket. However, once data is in DB, it's very easy to query and within one milisecond you can accesss the data (records).
After taking the data from S3 bucket, we are going to parse it by leveraging **Lambda function** and put in **directory object** (Key_Value pairs).

**Data Flow:**
    
    Once all VMs get scanned, Lambda function will get triggered then Lambda will put the data in S3 bucket and all scan 
    results will be in S3 bucket. 
    
    Whenever upload event happens to S3 bucket               ------->  Lambda service will be triggered.
    Using Python code, Lambda will parse the json object     ------->  Then data will be uploaded to DynamoDB by Lambda.
    And from DynamoDB, data would be transported to Splunk   ------->  So we can visualize all the logs and monitor them.
    
    That's the Efficiency!
    
    Note-1: While Lambda parsing the json object, it will keep only necessary key and values out of json file.
    Note-2: S3 bucket name must be globally unique because we use S3 bucket for static website hosting. It means no one else 
            should be able to accesss other than user who has privilege.
    
    
Since DynamoDB has a persistent storage, we can access the data whenever we need to.    
     
**LET'S BUILD OUR SOLUTION...**

   -  Go to AWS Console for DynamoDB Service and create a table called **"Employees"** with Partition key (Primary key) **"emp_id"**
   -  We just created **Managed Non-Relational DB.**
   -  Then create an S3 bucket that has globally unique name.
   -  Enable **versioning** so we can prevent accidental deletion of our S3 bucket which has critical data.
   -  Next, we need to create **Lambda function** but before doing it we would need to create an IAM role 
      because we will need to add that role while creating our Lambda function. 
   -  Then we are going to attach this role to **Lambda function.**
   -  For that, go to IAM and Roles then choose use case as **"Lambda"**
   -  Once you come to **"Permissions"** section, click on **"Create a Policy"**
   -  Now, we need to write our policy for **accessing S3 bucket**, and **DynamoDB Table** and **write the logs to CloudWatch**.
   -  Go to AWS policy generator and generate your policy for above permissions. 

          iampolicy.json
        
          {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "Stmt1641137509840",
                  "Action": [
                    "s3:GetObject"
                  ],
                  "Effect": "Allow",
                  "Resource": "*"
                },
                {
                  "Sid": "Stmt1641137545555",
                  "Action": [
                    "dynamodb:PutItem"
                  ],
                  "Effect": "Allow",
                  "Resource": "*"
                },
                {
                  "Effect": "Allow",
                  "Action": [
                      "logs:CreateLogGroup",
                      "logs:CreateLogStream",
                      "logs:PutLogEvents"
                  ],
                  "Resource": "arn:aws:logs:*:*:*"
                }
              ]
            }
     
  **Our Current Logic:** 
   -  **Lambda** function must get the object from **S3**. 
   -  Then we get the **permissions.**
   -  Once Lambda gets the object, it will **parse** it.
   -  After parsing the json object based on our logic, it will **put the item in DynamoDB table**.
   -  Lastly, we will be able to **monitor** the logs from **CloudWatch.**

After generating our policy with AWS Policy Generator...
   -  Go to AWS Console and create a role, choose Lambda as your use case. Paste generated policy in permisssions section. 
   -  Go back to IAM Roles, and create a role then **"Attach Permission Policy"**, choose your policy aftering filtering your policy name. 
   -  Add a role name which holds above permissions.  
   -  Our IAM role is created, now.
   
Now, it's time to create our **Lambda** function...

**LAMBDA**: Lambda is a serverless service. That means, we do not need to provision Lambda in order to run our code. In other words, creating an
            instance is not needed or no need for template to provision infrastructure. 
     
All we need to choose is our **Runtime Environment**. During the creation of our Lambda function, choose Permissions as
**"Use an existing role"**, then put the role name just created previously.

Basically, our **Lambda function** is created. 

We also need to add **Trigger** which will allow Lambda function gets triggered whenever there is upload events in S3.

Then choose your bucket name created before.

**Note:** Bucket created must be in same region. 

   -  Let's **configure** our S3 bucket more.
      Go to **Properties** and **Event Notifications** then choose **"Destination Type"** as Lambda function.
      
Next, develop Lambda function using Python script.
          
         handler.py
        
         import boto3 
         import json

         s3_client = boto3.client('s3')
         dynamodb_client = boto3.resource('dynamodb')

         def lambda_handler(event, context):
             bucket = event.get("Records")[0].get("s3").get("bucket").get("name")
             filename = event.get("Records")[0].get("s3").get("object").get("key")
             print(f'Print bucket name: {bucket}')
             print(f'Print object name: {filename}')
             json_object = s3_client.get_object(Bucket=bucket, Key=filename)
             json_file_reader = json_object['Body'].read()
             print(json_file_reader)
             print(type(json_file_reader))
             json_dict = json.loads(json_file_reader)
             table = dynamodb_client.Table('Employees')
             table.put_item(Item=json_dict)

Additionally, create a new file called **"employee.json"** to update the file.

         {
             "position": "DevOps",
             "location": "USA",
             "company": "Usertech",
             "name": "user",
             "emp_id": "1"
         }

   -  Now, let's go ahead and upload **employee.json** file to S3 bucket
   -  To do that, find your **bucketname** then **Objects>Uploads>Add Files**
   -  Find employee.json and click on upload. 
   -  File is uploaded.
   
Check the results in **CloudWatch**. 

   -  Go to **CloudWatch** and **Log Groups**.
   -  You will be able to see log group is created automatically by **CloudWatch** such as **aws/lambda/dynamodb-s3**.
   -  Go to **Log Stream hyperlink** and **Log Events**. 
   -  We successfully printed bucket name and object name with the script. 
 
Everything comes from **"event"** parameter in our **Lambda function**

      def lambda_handler(event, context):
      
Now, we have to get the content of this file from the bucket and we need to parse it then write it to DynamoDB Table. 
To do that, we can go to BOTO3 documentation. It has lots of built-in function. 
 
   -  Go to S3  and upload employee.json file then check CloudWatch. Refresh the same log group.
   -  We can see our data which starts with **"position"** = **"DevOps"**

As seen from our Lambda function, we use **BOTO3** as our **AWS SDK** where we get all the functions from.



Lastly, in last lines we write our data in **Employees** table using:

          json_dict = json.loads(json_file_reader)
          table = dynamodb_client.Table('Employees')
          table.put_item(Item=json_dict)

After uploading **"employee.json"**, we are able to see the data in "Employees" table.
Lambda took care of everything!

**Note:** For Lambda, we get access to **CloudWatch**. On the other hand, for CloudTrial, no need to get access. You get all API logs for events. 
          **CloudTrial** gets audit logs only.
 













  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
