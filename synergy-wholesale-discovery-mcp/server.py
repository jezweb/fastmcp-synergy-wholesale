#!/usr/bin/env python3
"""
Synergy Wholesale Domain Discovery & Registration MCP Server
Provides tools for checking domain availability and registering domains
"""

import sys
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from fastmcp import FastMCP
from base_server import SynergyWholesaleBase

# Initialize FastMCP server - MUST be at module level for FastMCP Cloud
mcp = FastMCP(
    name="Synergy Wholesale Discovery",
    version="1.0.0",
    instructions="""
    This server provides domain discovery and registration tools for Synergy Wholesale.

    Key features:
    - Check domain availability (single and bulk)
    - Get domain pricing for all TLDs
    - Check TLD-specific requirements
    - Register domains (single and bulk)
    - Check if domains need renewal

    All tools support dynamic credential passing or environment variables:
    - SYNERGY_RESELLER_ID: Your Synergy Wholesale reseller ID
    - SYNERGY_API_KEY: Your Synergy Wholesale API key
    """
)

# Initialize base server
base = SynergyWholesaleBase("SynergyDiscovery")

# ============================================================================
# DOMAIN DISCOVERY TOOLS
# ============================================================================

@mcp.tool()
def check_domain(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check if a domain is available for registration.

    Args:
        domain_name: The domain name to check (e.g., "example.com")
        reseller_id: Optional Synergy Wholesale reseller ID (falls back to env var)
        api_key: Optional Synergy Wholesale API key (falls back to env var)

    Returns:
        Dictionary with availability status and pricing information
    """
    return base.safe_soap_call("checkDomain", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def bulk_check_domain(
    domain_names: List[str],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check availability of multiple domains (up to 30).

    Args:
        domain_names: List of domain names to check
        reseller_id: Optional Synergy Wholesale reseller ID (falls back to env var)
        api_key: Optional Synergy Wholesale API key (falls back to env var)

    Returns:
        Dictionary with availability status for each domain
    """
    if len(domain_names) > 30:
        return {"error": "Maximum 30 domains can be checked at once"}

    return base.safe_soap_call("bulkCheckDomain", {"domainNameList": domain_names}, reseller_id, api_key)

# Cache for domain pricing
_pricing_cache = {}

@mcp.tool()
def get_domain_pricing(
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None,
    force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Get pricing for all available TLDs.

    Args:
        reseller_id: Optional Synergy Wholesale reseller ID (falls back to env var)
        api_key: Optional Synergy Wholesale API key (falls back to env var)
        force_refresh: Force refresh of cached pricing data

    Returns:
        Dictionary with pricing information for each TLD
    """
    if force_refresh or "pricing" not in _pricing_cache:
        result = base.safe_soap_call("getDomainPricing", {}, reseller_id, api_key)
        if "error" not in result:
            _pricing_cache["pricing"] = result
            _pricing_cache["timestamp"] = datetime.now().isoformat()
            return result
    return _pricing_cache.get("pricing", {"error": "No pricing data available"})

@mcp.tool()
def get_domain_eligibility_fields(
    tld: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get eligibility requirements for a specific TLD.

    Args:
        tld: The TLD to check (e.g., "au", "com.au", "us")
        reseller_id: Optional Synergy Wholesale reseller ID (falls back to env var)
        api_key: Optional Synergy Wholesale API key (falls back to env var)

    Returns:
        Dictionary with eligibility fields required for the TLD
    """
    return base.safe_soap_call("getEligibilityFields", {"tld": tld}, reseller_id, api_key)

@mcp.tool()
def list_available_extensions(
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all available domain extensions (TLDs).

    Args:
        reseller_id: Optional Synergy Wholesale reseller ID (falls back to env var)
        api_key: Optional Synergy Wholesale API key (falls back to env var)

    Returns:
        Dictionary with list of available TLDs and their properties
    """
    return base.safe_soap_call("listAvailableDomainExtensions", {}, reseller_id, api_key)

@mcp.tool()
def determine_domain_renewable(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check if a domain needs renewal.

    Args:
        domain_name: The domain name to check
        reseller_id: Optional Synergy Wholesale reseller ID (falls back to env var)
        api_key: Optional Synergy Wholesale API key (falls back to env var)

    Returns:
        Dictionary with renewal status and expiry information
    """
    return base.safe_soap_call("determineDomainIsRenewable", {"domainName": domain_name}, reseller_id, api_key)

# ============================================================================
# DOMAIN REGISTRATION TOOLS
# ============================================================================

@mcp.tool()
def register_domain(
    domain_name: str,
    years: int,
    nameservers: List[str],
    registrant_contact: Dict[str, str],
    technical_contact: Optional[Dict[str, str]] = None,
    admin_contact: Optional[Dict[str, str]] = None,
    billing_contact: Optional[Dict[str, str]] = None,
    id_protection: bool = False,
    eligibility_fields: Optional[Dict[str, Any]] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Register a new domain.

    Args:
        domain_name: Domain to register
        years: Number of years to register (1-10)
        nameservers: List of nameservers (2-6)
        registrant_contact: Registrant contact details (required)
            - firstname: First name
            - lastname: Last name
            - email: Email address
            - phone: Phone number (format: +1.1234567890)
            - address: Street address
            - city: City
            - state: State/Province
            - postcode: Postal code
            - country: Country code (e.g., "US", "AU")
            - organisation: Organization name (optional)
        technical_contact: Technical contact (optional, defaults to registrant)
        admin_contact: Admin contact (optional, defaults to registrant)
        billing_contact: Billing contact (optional, defaults to registrant)
        id_protection: Enable WHOIS privacy protection
        eligibility_fields: TLD-specific eligibility data
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with registration result
    """
    params = {
        "domainName": domain_name,
        "years": years,
        "nameServers": nameservers,
        "registrant_contact": registrant_contact
    }

    # Use registrant contact as default for other contacts if not provided
    params["technical_contact"] = technical_contact or registrant_contact
    params["admin_contact"] = admin_contact or registrant_contact
    params["billing_contact"] = billing_contact or registrant_contact

    if id_protection:
        params["idProtection"] = "on"

    if eligibility_fields:
        params["eligibilityFields"] = eligibility_fields

    return base.safe_soap_call("registerDomain", params, reseller_id, api_key)

@mcp.tool()
def bulk_register_domain(
    domains: List[Dict[str, Any]],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Register multiple domains at once.

    Args:
        domains: List of domain registration requests, each containing:
            - domain_name: Domain to register
            - years: Number of years
            - nameservers: List of nameservers
            - registrant_contact: Contact details
            - (other fields as in register_domain)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with registration results for each domain
    """
    if len(domains) > 10:
        return {"error": "Maximum 10 domains can be registered at once"}

    results = {}
    for domain_info in domains:
        domain_name = domain_info.get("domain_name")
        if not domain_name:
            results[f"domain_{len(results)}"] = {"error": "Missing domain_name"}
            continue

        # Extract parameters for single registration
        reg_params = {
            "domain_name": domain_name,
            "years": domain_info.get("years", 1),
            "nameservers": domain_info.get("nameservers", []),
            "registrant_contact": domain_info.get("registrant_contact", {}),
            "technical_contact": domain_info.get("technical_contact"),
            "admin_contact": domain_info.get("admin_contact"),
            "billing_contact": domain_info.get("billing_contact"),
            "id_protection": domain_info.get("id_protection", False),
            "eligibility_fields": domain_info.get("eligibility_fields"),
            "reseller_id": reseller_id,
            "api_key": api_key
        }

        # Register individual domain
        result = register_domain(**reg_params)
        results[domain_name] = result

    return results

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Check if credentials are provided via environment
    has_env_creds = bool(os.getenv("SYNERGY_RESELLER_ID") and os.getenv("SYNERGY_API_KEY"))

    if not has_env_creds:
        base.logger.info("No environment credentials found - dynamic credentials mode enabled")
        base.logger.info("Tools will require reseller_id and api_key parameters")

    # Run the server
    mcp.run()