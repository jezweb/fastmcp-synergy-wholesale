"""
Base server class for all Synergy Wholesale MCP servers.
Provides common SOAP client functionality and authentication.
"""

import os
import logging
from typing import Dict, Any, Optional
from zeep import Client, Settings, helpers
from zeep.exceptions import Fault, TransportError
from zeep.transports import Transport
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
WSDL_URL = "https://api.synergywholesale.com/server.php?wsdl"
DEFAULT_TIMEOUT = 30

class SynergyWholesaleBase:
    """Base class for Synergy Wholesale MCP servers"""

    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize base server with logging and configuration"""
        self.name = name
        self.version = version
        self._soap_client = None

        # Configure logging
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(name)

        # Enable SOAP debug logging if DEBUG level
        if log_level == "DEBUG":
            logging.getLogger('zeep.transports').setLevel(logging.DEBUG)
            logging.getLogger('zeep.wsdl').setLevel(logging.DEBUG)
            self.logger.info("SOAP debug logging enabled")

    def get_soap_client(self) -> Client:
        """Get or create SOAP client instance"""
        if self._soap_client is None:
            self.logger.info("Initializing SOAP client")
            try:
                # Create transport with timeout
                timeout = int(os.getenv("API_TIMEOUT", str(DEFAULT_TIMEOUT)))
                transport = Transport(timeout=timeout)

                # Create settings with non-strict mode
                settings = Settings(
                    strict=False,  # Allow slightly malformed XML
                    xml_huge_tree=True,  # Support large documents
                    forbid_dtd=False,
                    forbid_entities=False,
                    forbid_external=False
                )

                # Create client
                self._soap_client = Client(
                    WSDL_URL,
                    transport=transport,
                    settings=settings
                )
                self.logger.info(f"SOAP client initialized successfully")

            except Exception as e:
                self.logger.error(f"Failed to initialize SOAP client: {e}")
                raise ValueError(f"Could not connect to Synergy Wholesale API: {e}")

        return self._soap_client

    def validate_credentials(self, reseller_id: Optional[str] = None, api_key: Optional[str] = None):
        """Validate and return credentials from parameters or environment"""
        final_reseller_id = reseller_id or os.getenv("SYNERGY_RESELLER_ID")
        final_api_key = api_key or os.getenv("SYNERGY_API_KEY")

        if not final_reseller_id or not final_api_key:
            error_msg = (
                "Missing required credentials. Please provide reseller_id and api_key parameters, "
                "or set SYNERGY_RESELLER_ID and SYNERGY_API_KEY environment variables."
            )
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        return final_reseller_id, final_api_key

    def add_auth(self, params: Dict[str, Any], reseller_id: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Add authentication to request parameters"""
        final_reseller_id, final_api_key = self.validate_credentials(reseller_id, api_key)
        return {
            "resellerID": final_reseller_id,
            "apiKey": final_api_key,
            **params
        }

    def handle_soap_response(self, response: Any) -> Dict[str, Any]:
        """Convert SOAP response to dictionary"""
        self.logger.debug(f"Processing SOAP response: {response}")

        if response is None:
            return {"error": "No response received from API"}

        # Serialize zeep response object
        try:
            result = helpers.serialize_object(response)
            if hasattr(result, 'items'):
                result = dict(result)
            self.logger.debug(f"Serialized response with {len(result)} fields")
        except Exception as e:
            self.logger.debug(f"Could not serialize with zeep helpers: {e}")
            # Fallback to manual extraction
            result = {}
            if hasattr(response, '__values__'):
                result = dict(response.__values__)
            elif hasattr(response, "__dict__"):
                for k, v in response.__dict__.items():
                    if not k.startswith("_"):
                        result[k] = v
            else:
                result = {"result": str(response)}

        # Check for error status
        if "status" in result and isinstance(result["status"], str):
            if result["status"].startswith("ERR_"):
                error_msg = result.get("errorMessage", "Unknown error occurred")
                self.logger.error(f"API Error: {result['status']} - {error_msg}")
                return {"error": error_msg, "status": result["status"], **result}
            elif result["status"] == "OK":
                self.logger.info(f"API call successful with status OK")

        self.logger.info(f"Returning result with {len(result)} fields")
        return result

    def safe_soap_call(self, method_name: str, params: Dict[str, Any],
                      reseller_id: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Safely call SOAP method with error handling"""
        try:
            client = self.get_soap_client()
            method = getattr(client.service, method_name)

            # Add authentication
            auth_params = self.add_auth(params, reseller_id, api_key)

            self.logger.debug(f"Calling {method_name} with params: {list(params.keys())}")

            # Get the request type for this method
            request_type_name = f'{method_name}Request'

            try:
                # Try to create request object
                request_type = client.get_type(f'{{urn:WholesaleSystem}}{request_type_name}')
                request_obj = request_type(**auth_params)

                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug(f"SOAP method: {method_name}")
                    self.logger.debug(f"Request object created: {request_obj}")

                response = method(request_obj)
                self.logger.info(f"SOAP call successful for {method_name}")

            except Exception as type_error:
                # Fallback: try direct call
                self.logger.debug(f"Could not create request object for {method_name}, trying direct call: {type_error}")
                response = method(**auth_params)
                self.logger.info(f"SOAP call successful for {method_name} (direct call)")

            return self.handle_soap_response(response)

        except TransportError as e:
            self.logger.error(f"Transport/XML error in {method_name}: {e}")
            return {
                "error": f"Transport error: {e}",
                "method": method_name,
                "suggestion": "Check network connectivity and API endpoint"
            }

        except Fault as e:
            self.logger.error(f"SOAP Fault in {method_name}: {e}")
            fault_detail = {
                "error": f"SOAP Fault: {e.message if hasattr(e, 'message') else str(e)}",
                "method": method_name
            }
            if hasattr(e, 'code'):
                fault_detail["fault_code"] = str(e.code)
            if hasattr(e, 'detail'):
                fault_detail["fault_detail"] = str(e.detail)
            return fault_detail

        except Exception as e:
            self.logger.error(f"Unexpected error calling {method_name}: {e}")
            return {"error": str(e), "method": method_name, "error_type": type(e).__name__}