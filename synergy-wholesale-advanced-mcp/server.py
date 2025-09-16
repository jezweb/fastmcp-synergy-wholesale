#!/usr/bin/env python3
"""
Synergy Wholesale Advanced/Registry Operations MCP Server
Provides tools for advanced features, DNSSEC, glue records, categories, and .AU management
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
    name="Synergy Wholesale Advanced",
    version="1.0.0",
    instructions="""
    This server provides advanced registry and domain management tools for Synergy Wholesale.

    Key features:
    - Registry host (glue record) management
    - DNSSEC configuration
    - Domain category organization
    - .AU specific operations including Change of Registrant
    - ABN/ACN/RBN lookups
    - .US nexus data management

    All tools support dynamic credential passing or environment variables:
    - SYNERGY_RESELLER_ID: Your Synergy Wholesale reseller ID
    - SYNERGY_API_KEY: Your Synergy Wholesale API key
    """
)

# Initialize base server
base = SynergyWholesaleBase("SynergyAdvanced")

# ============================================================================
# REGISTRY HOST (GLUE RECORDS) MANAGEMENT
# ============================================================================

@mcp.tool()
def add_registry_host(
    domain_name: str,
    host_name: str,
    ip_addresses: List[str],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a registry host (glue record) for a domain.

    Args:
        domain_name: The domain name
        host_name: The host name (e.g., "ns1.example.com")
        ip_addresses: List of IP addresses for the host
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with host creation result
    """
    return base.safe_soap_call("addRegistryHost", {
        "domainName": domain_name,
        "hostName": host_name,
        "ipAddresses": ip_addresses
    }, reseller_id, api_key)

@mcp.tool()
def delete_registry_host(
    domain_name: str,
    host_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a registry host (glue record) for a domain.

    Args:
        domain_name: The domain name
        host_name: The host name to delete
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with deletion result
    """
    return base.safe_soap_call("deleteRegistryHost", {
        "domainName": domain_name,
        "hostName": host_name
    }, reseller_id, api_key)

@mcp.tool()
def add_registry_host_ip(
    domain_name: str,
    host_name: str,
    ip_address: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add an IP address to an existing registry host.

    Args:
        domain_name: The domain name
        host_name: The host name
        ip_address: IP address to add
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with IP addition result
    """
    return base.safe_soap_call("addRegistryHostIPAddress", {
        "domainName": domain_name,
        "hostName": host_name,
        "ipAddress": ip_address
    }, reseller_id, api_key)

@mcp.tool()
def delete_registry_host_ip(
    domain_name: str,
    host_name: str,
    ip_address: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove an IP address from a registry host.

    Args:
        domain_name: The domain name
        host_name: The host name
        ip_address: IP address to remove
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with IP removal result
    """
    return base.safe_soap_call("deleteRegistryHostIPAddress", {
        "domainName": domain_name,
        "hostName": host_name,
        "ipAddress": ip_address
    }, reseller_id, api_key)

@mcp.tool()
def list_registry_hosts(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all registry hosts (glue records) for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of registry hosts
    """
    return base.safe_soap_call("listAllRegistryHosts", {
        "domainName": domain_name
    }, reseller_id, api_key)

@mcp.tool()
def registry_host_info(
    domain_name: str,
    host_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get information about a specific registry host.

    Args:
        domain_name: The domain name
        host_name: The host name to query
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with host information
    """
    return base.safe_soap_call("registryHostInformation", {
        "domainName": domain_name,
        "hostName": host_name
    }, reseller_id, api_key)

# ============================================================================
# DNSSEC MANAGEMENT
# ============================================================================

@mcp.tool()
def add_dnssec_record(
    domain_name: str,
    key_tag: int,
    algorithm: int,
    digest_type: int,
    digest: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a DNSSEC record to a domain.

    Args:
        domain_name: The domain name
        key_tag: The key tag value
        algorithm: Algorithm number (e.g., 7 for RSASHA1-NSEC3-SHA1)
        digest_type: Digest type (e.g., 1 for SHA-1, 2 for SHA-256)
        digest: The digest string
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with DNSSEC addition result
    """
    return base.safe_soap_call("addDNSSECRecord", {
        "domainName": domain_name,
        "keyTag": key_tag,
        "algorithm": algorithm,
        "digestType": digest_type,
        "digest": digest
    }, reseller_id, api_key)

@mcp.tool()
def remove_dnssec_record(
    domain_name: str,
    key_tag: int,
    algorithm: int,
    digest_type: int,
    digest: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove a DNSSEC record from a domain.

    Args:
        domain_name: The domain name
        key_tag: The key tag value
        algorithm: Algorithm number
        digest_type: Digest type
        digest: The digest string
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with DNSSEC removal result
    """
    return base.safe_soap_call("removeDNSSECRecord", {
        "domainName": domain_name,
        "keyTag": key_tag,
        "algorithm": algorithm,
        "digestType": digest_type,
        "digest": digest
    }, reseller_id, api_key)

@mcp.tool()
def list_dnssec_entries(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all DNSSEC records for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of DNSSEC records
    """
    return base.safe_soap_call("listDNSSECEntries", {
        "domainName": domain_name
    }, reseller_id, api_key)

@mcp.tool()
def dnssec_info(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get DNSSEC information for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with DNSSEC status and details
    """
    return base.safe_soap_call("DNSSECInformation", {
        "domainName": domain_name
    }, reseller_id, api_key)

# ============================================================================
# DOMAIN CATEGORY MANAGEMENT
# ============================================================================

@mcp.tool()
def create_domain_category(
    category_name: str,
    description: Optional[str] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new domain category for organization.

    Args:
        category_name: Name of the category
        description: Optional description
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with category creation result
    """
    params = {"categoryName": category_name}
    if description:
        params["description"] = description

    return base.safe_soap_call("createDomainCategory", params, reseller_id, api_key)

@mcp.tool()
def update_domain_category(
    category_id: str,
    category_name: Optional[str] = None,
    description: Optional[str] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing domain category.

    Args:
        category_id: ID of the category to update
        category_name: New category name (optional)
        description: New description (optional)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with update result
    """
    params = {"categoryID": category_id}
    if category_name:
        params["categoryName"] = category_name
    if description:
        params["description"] = description

    if len(params) == 1:
        return {"error": "At least one field to update must be provided"}

    return base.safe_soap_call("updateDomainCategory", params, reseller_id, api_key)

@mcp.tool()
def remove_domain_category(
    category_id: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a domain category.

    Args:
        category_id: ID of the category to delete
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with deletion result
    """
    return base.safe_soap_call("removeDomainCategory", {
        "categoryID": category_id
    }, reseller_id, api_key)

@mcp.tool()
def assign_domain_category(
    domain_name: str,
    category_id: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Assign a domain to a category.

    Args:
        domain_name: Domain to categorize
        category_id: Category ID to assign
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with assignment result
    """
    return base.safe_soap_call("assignDomainCategory", {
        "domainName": domain_name,
        "categoryID": category_id
    }, reseller_id, api_key)

@mcp.tool()
def unassign_domain_category(
    domain_name: str,
    category_id: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove a domain from a category.

    Args:
        domain_name: Domain to uncategorize
        category_id: Category ID to remove from
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with unassignment result
    """
    return base.safe_soap_call("unassignDomainCategory", {
        "domainName": domain_name,
        "categoryID": category_id
    }, reseller_id, api_key)

@mcp.tool()
def list_domain_categories(
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all domain categories.

    Args:
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of categories
    """
    return base.safe_soap_call("listDomainCategories", {}, reseller_id, api_key)

# ============================================================================
# .AU SPECIFIC OPERATIONS
# ============================================================================

@mcp.tool()
def get_abn_acn_rbn_info(
    lookup_value: str,
    lookup_type: str = "ABN",
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lookup ABN/ACN/RBN information for .AU eligibility.

    Args:
        lookup_value: The ABN, ACN, or RBN to lookup
        lookup_type: Type of lookup ("ABN", "ACN", or "RBN")
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with business information
    """
    if lookup_type not in ["ABN", "ACN", "RBN"]:
        return {"error": "lookup_type must be 'ABN', 'ACN', or 'RBN'"}

    return base.safe_soap_call("lookupABNACNRBNInformation", {
        "lookupValue": lookup_value,
        "lookupType": lookup_type
    }, reseller_id, api_key)

@mcp.tool()
def generate_au_eligibility(
    business_number: str,
    business_type: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate .AU eligibility information from business number.

    Args:
        business_number: ABN, ACN, or RBN
        business_type: Type of business number ("ABN", "ACN", "RBN")
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with generated eligibility data
    """
    return base.safe_soap_call("generateAUEligibilityFromBusinessNumber", {
        "businessNumber": business_number,
        "businessType": business_type
    }, reseller_id, api_key)

@mcp.tool()
def au_change_registrant_request(
    domain_name: str,
    new_registrant: Dict[str, str],
    new_eligibility: Dict[str, Any],
    explanation: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submit a .AU Change of Registrant (CoR) request.

    Args:
        domain_name: .AU domain to change registrant for
        new_registrant: New registrant contact details:
            - firstname: First name
            - lastname: Last name
            - organisation: Organization name
            - email: Email address
            - phone: Phone number
            - address: Street address
            - city: City
            - state: State
            - postcode: Postcode
            - country: Country code (AU)
        new_eligibility: New eligibility information:
            - registrantID: ABN/ACN/RBN
            - registrantIDType: "ABN", "ACN", or "RBN"
            - eligibilityType: e.g., "Company", "Registered Business"
            - eligibilityName: Legal entity name
            - eligibilityID: Same as registrantID
        explanation: Reason for the change
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with CoR submission result
    """
    return base.safe_soap_call("AUChangeOfRegistrantRequest", {
        "domainName": domain_name,
        "newRegistrant": new_registrant,
        "newEligibility": new_eligibility,
        "explanation": explanation
    }, reseller_id, api_key)

# ============================================================================
# .US SPECIFIC OPERATIONS
# ============================================================================

@mcp.tool()
def retrieve_us_nexus_data(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve .US nexus data for a domain.

    Args:
        domain_name: .US domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with nexus data
    """
    return base.safe_soap_call("retrieveUSNexusData", {
        "domainName": domain_name
    }, reseller_id, api_key)

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