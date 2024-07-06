import requests
import json
import os
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_API_URL = os.environ.get("LANGFLOW_URL","https://ycchatbot-production.up.railway.app/api/v1/process")
FLOW_ID = os.environ.get("FLOW_ID", "83a51abd-d972-4b50-8bad-8c523f1d57fd")

TWEAKS = {
    "ParseData-pHL0P": {},
    "Prompt-dLJFH": {},
    "ChatInput-FtDLX": {},
    "ChatOutput-vXoKN": {},
    "GroqModel-lP3JZ": {},
    "File-tHVrf": {}
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    try:
        api_url = f"{BASE_API_URL}/{endpoint}"
        logger.info(f"Sending request to: {api_url}")
        logger.info(f"Message: {message}")
        
        payload = {
            "input_value": message,
            "output_type": output_type,
            "input_type": input_type,
        }
        if tweaks:
            payload["tweaks"] = tweaks
        
        headers = {"x-api-key": api_key} if api_key else None
        
        response = requests.post(api_url, json=payload, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text[:500]}...")  # Log first 500 characters
        
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to Langflow: {str(e)}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {str(e)}")
        return {"error": "Invalid JSON response from Langflow"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "An unexpected error occurred"}

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        api_key=args.api_key
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
