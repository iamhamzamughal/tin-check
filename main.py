from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import requests
import xmltodict
import json

app = FastAPI()

class TinCheckRequest(BaseModel):
    username: str
    password: str
    tin: str
    fname: str
    address1: str
    city: str
    state: str
    zip5: str

@app.post("/validate-tin")
async def validate_tin(request: Request):
    raw_data = await request.json()

    print("\n")
    print("********* Incoming Request JSON ********:\n")
    print(json.dumps(raw_data, indent=4))
    print("\n")

    # Trim spaces
    fields_to_trim = ["username", "password", "tin", "city", "state", "zip5"]
    for field in fields_to_trim:
        if field in raw_data and isinstance(raw_data[field], str):
            raw_data[field] = raw_data[field].strip()

    # Format TIN
    # Remove dashes and spaces from TIN
    tin_cleaned = raw_data["tin"].replace("-", "").replace(" ", "")

    print("Formatted TIN Value:", tin_cleaned)
    print("\n")
    print("Type of TIN:", type(tin_cleaned))
    print("\n")
    print("Total Characters of TIN:", len(tin_cleaned))
    print("\n")

    url = "https://www.tincheck.com/PVSws/pvsservice.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://www.TinCheck.com/WebServices/PVSService/ValidateTinNameAddressListMatch"
    }

    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ValidateTinNameAddressListMatch xmlns="http://www.TinCheck.com/WebServices/PVSService/">
      <CurUser>
        <UserLogin>{raw_data['username']}</UserLogin>
        <UserPassword>{raw_data['password']}</UserPassword>
      </CurUser>
      <TinName>
        <TIN>{tin_cleaned}</TIN>
        <FName>{raw_data['fname']}</FName>
      </TinName>
      <USPSAddress>
        <Address1>{raw_data['address1']}</Address1>
        <City>{raw_data['city']}</City>
        <State>{raw_data['state']}</State>
        <Zip5>{raw_data['zip5']}</Zip5>
      </USPSAddress>
    </ValidateTinNameAddressListMatch>
  </soap:Body>
</soap:Envelope>"""

    try:
        response = requests.post(url, data=soap_body.strip(), headers=headers)
        if response.status_code == 200:
            parsed = xmltodict.parse(response.content)
            result_raw = parsed["soap:Envelope"]["soap:Body"]["ValidateTinNameAddressListMatchResponse"]["ValidateTinNameAddressListMatchResult"]

            # Filter required fields only
            filtered_response = {
                "REQUESTID": result_raw.get("REQUESTID"),
                "REQUEST_STATUS": result_raw.get("REQUEST_STATUS"),
                "REQUEST_DETAILS": result_raw.get("REQUEST_DETAILS"),
                "TINNAME_RESULT": {
                    "TINNAME_CODE": result_raw.get("TINNAME_RESULT", {}).get("TINNAME_CODE"),
                    "TINNAME_DETAILS": result_raw.get("TINNAME_RESULT", {}).get("TINNAME_DETAILS"),
                    "DMF_CODE": result_raw.get("TINNAME_RESULT", {}).get("DMF_CODE"),
                    "DMF_DETAILS": result_raw.get("TINNAME_RESULT", {}).get("DMF_DETAILS"),
                    "DMF_DATA": result_raw.get("TINNAME_RESULT", {}).get("DMF_DATA"),
                    "EIN_CODE": result_raw.get("TINNAME_RESULT", {}).get("EIN_CODE"),
                    "EIN_DETAILS": result_raw.get("TINNAME_RESULT", {}).get("EIN_DETAILS"),
                    "EIN_DATA": result_raw.get("TINNAME_RESULT", {}).get("EIN_DATA"),
                    "GIIN_CODE": result_raw.get("TINNAME_RESULT", {}).get("GIIN_CODE"),
                    "GIIN_DETAILS": result_raw.get("TINNAME_RESULT", {}).get("GIIN_DETAILS"),
                    "GIIN_DATA": result_raw.get("TINNAME_RESULT", {}).get("GIIN_DATA"),
                },
                "ADDRESS_RESULT": {
                    "ADDRESS_CODE": result_raw.get("ADDRESS_RESULT", {}).get("ADDRESS_CODE"),
                    "ADDRESS_DETAILS": result_raw.get("ADDRESS_RESULT", {}).get("ADDRESS_DETAILS"),
                },
                "STATUS": {
                    "Status": result_raw.get("STATUS", {}).get("Status"),
                    "CallsRemaining": result_raw.get("STATUS", {}).get("CallsRemaining"),
                }
            }

            print("********** Outgoing Filtered JSON Response **********:\n")
            print(json.dumps(filtered_response, indent=4))
            print("\n")

            return filtered_response
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
