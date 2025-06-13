# 🛡️ SickNote Vault

SickNote Vault is a simple, secure web application that allows doctors and clinics to upload and verify sick notes using AWS services.

This full-stack project demonstrates how to build a functional medical note management system using modern cloud technologies. It includes:

- A lightweight frontend in HTML/CSS/JS hosted via AWS Amplify
- A serverless backend with AWS Lambda, API Gateway, S3, DynamoDB, and SES
- Proper use of IAM roles and permissions for resource access
- Real-time error tracking with CloudWatch

It also allows organizations and public relations officers (PRs) to **verify the authenticity of a submitted sick note**, ensuring the validity of a patient's excuse for absence — all without revealing private details.

---

## 💡 Features

### ✅ Backend
- Accepts sick note uploads (base64-encoded PDF)
- Stores the file in Amazon S3
- Saves metadata (patient name, email, timestamp, note ID) in DynamoDB
- Sends confirmation email via SES
- Verifies sick notes by note ID and returns metadata + download link

### ✅ Frontend
- Clean form for uploading sick notes
- Separate form for verifying by note ID
- Built with vanilla HTML/CSS/JS
- No frameworks or build tools
- Hosted using AWS Amplify

---

## 🗂️ Project Structure

```bash
sicknote-vault/
├── backend/
│   ├── upload_note/
│   │   └── lambda.py
│   └── verify_note/
│       └── lambda.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
```

---

## 🛠️ Tech Stack

- **AWS Lambda** (Python)
- **Amazon S3**
- **Amazon DynamoDB**
- **Amazon SES**
- **Amazon API Gateway**
- **Amazon CloudWatch**
- **AWS IAM** for role-based access

---

## ⚙️ IAM Permissions (Setup)

Two Lambda functions use IAM roles with these permissions:

### ✅ Inline + Managed Policies
- `AmazonDynamoDBFullAccess` – Access to store and retrieve note data
- `AmazonS3FullAccess` – Upload PDF files to S3
- `AWSLambdaBasicExecutionRole` – Required for logging to CloudWatch
- `AllowSendEmailSES` (inline) – Custom policy to allow sending email via SES
- `sicknote_get_object` (inline) – Custom policy for `s3:GetObject` (for verification)

> IAM ensures only specific functions can access specific AWS services — adding a strong layer of security and isolation.

---

## 🚀 Deployment Setup

### 1. Clone the repository
```bash
git clone https://github.com/UkkyNtem/sicknote-vault.git
cd sicknote-vault
```

### 2. Backend Setup
- ✅ Create S3 bucket (e.g., `sicknote-vault-bucket`)
- ✅ Create DynamoDB table named `SickNoteRecords` with `note_id` as primary key
- ✅ Verify a sender email in SES
- ✅ Create IAM role with permissions listed above
- ✅ Upload Lambda functions:
  - `upload_note/lambda.py` → `/upload`
  - `verify_note/lambda.py` → `/verify`
- ✅ Create API Gateway POST endpoints at `/upload` and `/verify`
- ✅ Enable CORS on both endpoints

### 3. Frontend Setup
- Edit `script.js` to include your API Gateway URLs
- Deploy frontend to AWS Amplify:
  - Connect GitHub repo
  - Choose the correct branch
  - Amplify builds and deploys automatically

---

## 🧪 Test with curl

### Upload:
```bash
curl -X POST https://your-api-url/upload   -H "Content-Type: application/json"   -d '{
    "patient_name": "Jane Doe",
    "patient_email": "jane@example.com",
    "note_file": "BASE64_ENCODED_PDF"
}'
```

### Verify:
```bash
curl -X POST https://your-api-url/verify   -H "Content-Type: application/json"   -d '{
    "note_id": "YOUR_NOTE_ID"
}'
```

---

## 🐛 Debugging Tools

- **CloudWatch Logs** for Lambda errors
- **API Gateway Logs** for request/response tracing
- **Custom error messages** shown in browser and curl responses

---

## 🔐 Planned Security Improvements



- [ ] Add authentication (e.g., Cognito or API Key) to restrict access
- [ ] Add expiration to presigned URLs
- [ ] Auto-delete files from S3 using lifecycle rules
- [ ] Implement server-side logging of suspicious uploads

---


Built by [UkkyNtem](https://github.com/UkkyNtem) with love and curiosity.  
For demo access or questions, feel free to reach out.