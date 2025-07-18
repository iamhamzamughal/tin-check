\# 🧾 FastAPI TIN Validation Service



This is a lightweight FastAPI-based microservice for validating a Taxpayer Identification Number (TIN) using TinCheck's SOAP API (`ValidateTinNameAddressListMatch`). It accepts a JSON payload, formats and sanitizes the input, makes a SOAP request, and returns a structured JSON response.



\## 🚀 Features



\- Accepts TIN, Name, and Address details via JSON

\- Sanitizes and formats input (e.g., removes dashes from TIN)

\- Sends SOAP request to TinCheck web service

\- Parses the XML response to clean JSON

\- Logs incoming request and formatted response

\- Easily deployable to Render, AWS, or Azure



\## 📦 Requirements



Install dependencies:



```bash

pip install -r requirements.txt

```



\## 🧪 API Usage



\### ➤ Endpoint



```

POST /validate-tin

```



\### ➤ Request Headers



```

Content-Type: application/json

```



\### ➤ Request Body Example



```json

{

&nbsp; "username": "your\_username",

&nbsp; "password": "your\_password",

&nbsp; "tin": "12-3456789",

&nbsp; "fname": "John Smith",

&nbsp; "address1": "123 Main St",

&nbsp; "city": "New York",

&nbsp; "state": "NY",

&nbsp; "zip5": "10001"

}

```



\## 💻 Running Locally



```bash

git clone https://github.com/yourusername/fastapi-tincheck.git

cd fastapi-tincheck

pip install -r requirements.txt

uvicorn main:app --reload

```



\## ☁️ Deployment on Render



1\. Push code to GitHub

2\. Go to https://render.com → New Web Service

3\. Connect GitHub repo and set:

&nbsp;  - Build Command: `pip install -r requirements.txt`

&nbsp;  - Start Command: `./start.sh`

&nbsp;  - Port: 10000



\## 📁 Project Structure



```

fastapi-tincheck/

├── main.py

├── requirements.txt

├── start.sh

├── .gitignore

└── README.md

```



\## 📄 License



MIT License



