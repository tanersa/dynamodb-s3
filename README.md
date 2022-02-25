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
   
Now, it's time to create our Lambda function...







  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
