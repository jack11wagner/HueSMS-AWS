# Cloud Computing Project


**Hue SMS: Migrating to the AWS Cloud** 

Final Project for CSCI 390

---

# Table of Contents
* [Overview](#Overview)
* [Setup](#Setup)
* [Technologies Used](#Technologies-Used)
* [Background](#Background)

---

# Overview 
- This project builds upon the existing project at Moravian University which is the [Hue_SMS Project](https://github.com/MoravianCollege/hue_sms)
- The goal of this project was to migrate as much as possible from our on-premises device to the AWS Cloud 
- Project utilized many of the concepts learned in CSCI 390 to successfully bridge an existing application to a cloud application
- Through the use of various AWS Services such as _API Gateway_, _AWS Lambda_, _DynamoDB_ and _Amazon Elastic Compute Cloud_ we were able to move almost all processes from an on-premises Raspberry Pi to the AWS Cloud 
- 
### Basic Structure
![HueSMS](https://github.com/jack11wagner/aws_hue_light_399/blob/main/hue_sms_aws_structure.png)



[comment]: <> (### Continuous Deployment)

[comment]: <> (- After our pull request has been properly tested we then want to automate the process of deploying our app with our new changes immediately)

[comment]: <> (- Our deployment is in the form of an aws instance which deploys our original flask server using gunicorn)

[comment]: <> (- Using the aws cli we use the run-instances command which deploys our tested and ready for production code as an EC2 instance)

[comment]: <> (---)

[comment]: <> (# Setup)

[comment]: <> (Each CI/CD pipeline will be unique but the main steps in creating this pipeline are the following:)

[comment]: <> (1. Create a directory in your github repository labeled ```.github/workflows```)
    
[comment]: <> (   - This is the directory where any actions yaml files will be located... For example in our repository we have )

[comment]: <> (   two files named ```continuous-integration.yml``` and ```continuous-deployment.yml``` these files have the instructions for each of our automation processes)

[comment]: <> (   - I recommend taking a look at this tutorial for a baseline on Github Actions [Github-Actions-Demo]&#40;https://docs.github.com/en/actions/quickstart&#41;)

[comment]: <> (2. Identify what behaviors or actions your CI/CD should be triggered on in a github repository )
   
[comment]: <> (    - visit this link [Github Workflow Triggers]&#40;https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows&#41;)

[comment]: <> (    - In the yml file this is what comes after the ```on:``` statement)

[comment]: <> (      - Examples could be ```on: [push, pull_request, pull, fork]```)

[comment]: <> (3. For the CI part of this pipeline you will want to have tests in place for your code, other options for the CI could be using linting as well as looking at testing coverage)

[comment]: <> (   - In order to make pull requests mergeable **ONLY** after tests have passed there are a few extra steps you have to do in the repository)

[comment]: <> (   - Head to **Settings > Branches** on your repo's homepage)

[comment]: <> (   - You will see branch protection rules, you want to click **Add rule**)

[comment]: <> (   - Now you will see a number of different settings...)

[comment]: <> (   - The first input heading is the branches for which this rule will apply to, if you just type '*' this will refer to all branches future and existing)

[comment]: <> (   - You will want to check off the following ```Require a pull request before merging``` and ```Require status checks to pass before merging```)

[comment]: <> (      - The status check setting requires a specified status check to run in order to verify the pull request still passes the tests.)

[comment]: <> (      - If using the standard integration format for your .yml file you can just specify ```integration``` here)

[comment]: <> (      - Now the CI only allows merging if the code is both automatically mergeable and the tests have passed.)

[comment]: <> (4. For the CD part of this pipeline we decided to use AWS to deploy our production code but there are a number of other options out there for continuous deployment)

[comment]: <> (- For AWS in particular we had to configure our AWS cli with credentials from our AWS account before being able to launch instances from our workflow file)

[comment]: <> (- Visit this page for information on how to configure the AWS CLI - [AWS CLI SETUP]&#40;https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html&#41;)

[comment]: <> (  - You will need to create an ```ACCESS_KEY_ID``` and ```SECRET_ACCESS_KEY``` to configure the aws cli this is done by going to the **IAM>USERS>SECURITY CREDENTIALS>CREATE ACCESS KEY** here you will be able to create these two credentials.)

[comment]: <> (  - These credentials will be stored in our repo with Github secrets)

[comment]: <> (- Using Github Secrets is very important to maintaining the privacy of our sensitive Key information)
  
[comment]: <> (   - In order to create a repository secret go to **Settings > Secrets > Actions** and you can create encrypted secrets there to be used in any github actions files)

[comment]: <> (   - In order to access these values here is an example: )
  
[comment]: <> (     - ```key : ${{ secrets.KEY_SECRET }}```)

[comment]: <> (- Once our aws cli was configured with our account, we used the command ```aws ec2 run-instances``` in order to deploy our updated instance of our web server )

[comment]: <> (  - This page has more information on the ```run-instances``` command [run-instances]&#40;https://docs.aws.amazon.com/cli/latest/reference/ec2/run-instances.html&#41;)

[comment]: <> (  - With this ```run-instances``` command you are able to launch an instance from the command line if you specify the proper parameters such as )

[comment]: <> (      - --image-id)

[comment]: <> (      - --instance-type)

[comment]: <> (      - --user-data)

[comment]: <> (      - --security-groups)

[comment]: <> (- After these setup instructions are complete your repo should have functional CI and CD capabilities to test and deploy automatically)


[comment]: <> (---)

[comment]: <> (# Technologies-Used)

[comment]: <> (- [Github-Actions-Demo]&#40;https://docs.github.com/en/actions/quickstart&#41;)

[comment]: <> (- [Flask Testing]&#40;https://flask.palletsprojects.com/en/1.1.x/testing/&#41;)

[comment]: <> (- [Pytest]&#40;https://docs.pytest.org/en/7.1.x/&#41;)

[comment]: <> (- [Pytest-Cov]&#40;https://github.com/marketplace/actions/pytester-cov&#41;)

[comment]: <> (- [AWS-CLI]&#40;https://aws.amazon.com/cli/&#41;)

[comment]: <> (- [AWS-run-instances]&#40;https://docs.aws.amazon.com/cli/latest/reference/ec2/run-instances.html&#41;)

[comment]: <> (- [PyLint]&#40;https://pylint.pycqa.org/en/latest/&#41;)

[comment]: <> (# Background)

[comment]: <> (- [Branch Protection Rules]&#40;https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule&#41;)

[comment]: <> (- [Github Secrets]&#40;https://docs.github.com/en/actions/security-guides/encrypted-secrets&#41;)

[comment]: <> (- [AWS CLI]&#40;https://aws.amazon.com/cli/&#41;)
