#!/usr/bin/env python3
"""
Synergy Wholesale Domain Portfolio Management MCP Server
Provides tools for managing existing domains and their settings
"""

import sys
import os
from typing import Dict, Any, List, Optional

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from fastmcp import FastMCP
from base_server import SynergyWholesaleBase

# Initialize FastMCP server
mcp = FastMCP(
    name="Synergy Wholesale Portfolio",
    version="1.0.0",
    instructions="""
    This server provides domain portfolio management tools for Synergy Wholesale.

    Key features:
    - List and get information about domains
    - Manage nameservers and passwords
    - Control domain locks and auto-renewal
    - Manage WHOIS privacy protection
    - Handle domain renewals
    - Manage domain contacts
    - Handle registrant updates

    All tools support dynamic credential passing or environment variables:
    - SYNERGY_RESELLER_ID: Your Synergy Wholesale reseller ID
    - SYNERGY_API_KEY: Your Synergy Wholesale API key
    """
)

# Initialize base server
base = SynergyWholesaleBase("SynergyPortfolio")

# ============================================================================
# DOMAIN LISTING & INFORMATION
# ============================================================================

@mcp.tool()
def list_domains(
    limit: int = 100,
    offset: int = 0,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all domains in your account.

    Args:
        limit: Maximum number of results (default 100)
        offset: Starting position for pagination (default 0)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of domains
    """
    return base.safe_soap_call("listDomains", {
        "limit": limit,
        "offset": offset
    }, reseller_id, api_key)

@mcp.tool()
def domain_info(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a domain.

    Args:
        domain_name: The domain name to query
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with domain details including status, expiry, nameservers, etc.
    """
    return base.safe_soap_call("domainInfo", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def bulk_domain_info(
    domain_names: List[str],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get information for multiple domains at once.

    Args:
        domain_names: List of domain names to query
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with information for each domain
    """
    if len(domain_names) > 50:
        return {"error": "Maximum 50 domains can be queried at once"}

    return base.safe_soap_call("bulkDomainInfo", {
        "domainNameList": domain_names
    }, reseller_id, api_key)

# ============================================================================
# DOMAIN SETTINGS MANAGEMENT
# ============================================================================

@mcp.tool()
def update_nameservers(
    domain_name: str,
    nameservers: List[str],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update nameservers for a domain.

    Args:
        domain_name: The domain name to update
        nameservers: List of nameservers (2-6)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with update result
    """
    if len(nameservers) < 2 or len(nameservers) > 6:
        return {"error": "Must provide between 2 and 6 nameservers"}

    return base.safe_soap_call("updateNameServers", {
        "domainName": domain_name,
        "nameServers": nameservers
    }, reseller_id, api_key)

@mcp.tool()
def update_domain_password(
    domain_name: str,
    new_password: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update the EPP/auth code for a domain.

    Args:
        domain_name: The domain name to update
        new_password: The new EPP/auth code
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with update result
    """
    return base.safe_soap_call("updateDomainPassword", {
        "domainName": domain_name,
        "newPassword": new_password
    }, reseller_id, api_key)

@mcp.tool()
def lock_domain(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enable transfer lock for a domain.

    Args:
        domain_name: The domain name to lock
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with lock status
    """
    return base.safe_soap_call("lockDomain", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def unlock_domain(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Disable transfer lock for a domain.

    Args:
        domain_name: The domain name to unlock
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with unlock status
    """
    return base.safe_soap_call("unlockDomain", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def enable_auto_renewal(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enable automatic renewal for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with auto-renewal status
    """
    return base.safe_soap_call("enableAutoRenewal", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def disable_auto_renewal(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Disable automatic renewal for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with auto-renewal status
    """
    return base.safe_soap_call("disableAutoRenewal", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def enable_id_protection(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enable WHOIS privacy protection for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with privacy protection status
    """
    return base.safe_soap_call("enableIDPrivacyProtection", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def disable_id_protection(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Disable WHOIS privacy protection for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with privacy protection status
    """
    return base.safe_soap_call("disableIDPrivacyProtection", {"domainName": domain_name}, reseller_id, api_key)

# ============================================================================
# DOMAIN RENEWAL
# ============================================================================

@mcp.tool()
def renew_domain(
    domain_name: str,
    years: int = 1,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Renew a domain for additional years.

    Args:
        domain_name: The domain name to renew
        years: Number of years to renew (default 1)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with renewal result
    """
    return base.safe_soap_call("renewDomain", {
        "domainName": domain_name,
        "years": years
    }, reseller_id, api_key)

@mcp.tool()
def bulk_renew_domain(
    domains: List[Dict[str, Any]],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Renew multiple domains at once.

    Args:
        domains: List of domain renewal requests, each containing:
            - domain_name: Domain to renew
            - years: Number of years to renew
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with renewal results for each domain
    """
    if len(domains) > 20:
        return {"error": "Maximum 20 domains can be renewed at once"}

    results = {}
    for domain_info in domains:
        domain_name = domain_info.get("domain_name")
        years = domain_info.get("years", 1)

        if not domain_name:
            results[f"domain_{len(results)}"] = {"error": "Missing domain_name"}
            continue

        result = renew_domain(domain_name, years, reseller_id, api_key)
        results[domain_name] = result

    return results

# ============================================================================
# CONTACT MANAGEMENT
# ============================================================================

@mcp.tool()
def update_contacts(
    domain_name: str,
    registrant_contact: Optional[Dict[str, str]] = None,
    technical_contact: Optional[Dict[str, str]] = None,
    admin_contact: Optional[Dict[str, str]] = None,
    billing_contact: Optional[Dict[str, str]] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update domain contact information.

    Args:
        domain_name: The domain name
        registrant_contact: New registrant contact (optional)
        technical_contact: New technical contact (optional)
        admin_contact: New admin contact (optional)
        billing_contact: New billing contact (optional)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with update result
    """
    params = {"domainName": domain_name}

    if registrant_contact:
        params["registrant_contact"] = registrant_contact
    if technical_contact:
        params["technical_contact"] = technical_contact
    if admin_contact:
        params["admin_contact"] = admin_contact
    if billing_contact:
        params["billing_contact"] = billing_contact

    if len(params) == 1:  # Only domain name provided
        return {"error": "At least one contact must be provided for update"}

    return base.safe_soap_call("updateContacts", params, reseller_id, api_key)

@mcp.tool()
def list_contacts(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get contact information for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with contact information
    """
    return base.safe_soap_call("listContacts", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def get_raw_contacts(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed raw contact information for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with detailed contact information
    """
    return base.safe_soap_call("getRawContacts", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def list_id_protected_contacts(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get ID protected contact information for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with protected contact information
    """
    return base.safe_soap_call("listIDProtectedContacts", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def resend_registrant_email(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Resend registrant verification email.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with email send result
    """
    return base.safe_soap_call("resendRegistrantUpdateEmail", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def cancel_pending_registrant_update(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cancel a pending registrant update.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with cancellation result
    """
    return base.safe_soap_call("cancelPendingRegistrantUpdate", {"domainName": domain_name}, reseller_id, api_key)

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