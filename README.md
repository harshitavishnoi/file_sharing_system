# file_sharing_system
this file sharing system is 
Framework - django rest Framework
Database - MySQL
Created a secure file-sharing system between two different types of users. For
implementation -
I have created a REST API’s for the following action.
User 1: Operation User
Actions which could be done by an Ops User
1. Login
2. Upload File*

* Only Ops User is allowed to upload pptx,docx and xlsx *
the Uploaded file must be only of pptx,docx, and xlsx type

User 2: Client User
Actions which could be done by a Client User
1. Sign Up ( Return an encrypted URL )
2. Email Verify ( Verification Email will be sent to the user on the registered email )
3. Login
4. Download File
5. List all uploaded files

i have also created a test.py file to test this api
