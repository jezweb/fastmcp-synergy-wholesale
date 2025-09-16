#!/usr/bin/env python3
"""
Synergy Wholesale DNS & Routing Management MCP Server
Provides tools for DNS records, email forwarding, and URL forwarding
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
    name="Synergy Wholesale DNS",
    version="1.0.0",
    instructions="""
    This server provides DNS and routing management tools for Synergy Wholesale.

    Key features:
    - DNS zone management
    - DNS record management (A, AAAA, CNAME, MX, TXT, etc.)
    - Email forwarding configuration
    - URL forwarding/redirects
    - Bulk DNS operations

    All tools support dynamic credential passing or environment variables:
    - SYNERGY_RESELLER_ID: Your Synergy Wholesale reseller ID
    - SYNERGY_API_KEY: Your Synergy Wholesale API key
    """
)

# Initialize base server
base = SynergyWholesaleBase("SynergyDNS")

# ============================================================================
# DNS ZONE MANAGEMENT
# ============================================================================

@mcp.tool()
def add_dns_zone(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a DNS zone for a domain.

    Args:
        domain_name: The domain name to create zone for
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with zone creation result
    """
    return base.safe_soap_call("addDNSZone", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def delete_dns_zone(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a DNS zone for a domain.

    Args:
        domain_name: The domain name to delete zone for
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with zone deletion result
    """
    return base.safe_soap_call("deleteDNSZone", {"domainName": domain_name}, reseller_id, api_key)

@mcp.tool()
def list_dns_zone(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all DNS records in a zone.

    Args:
        domain_name: The domain name to list records for
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of DNS records
    """
    return base.safe_soap_call("listDNSZone", {"domainName": domain_name}, reseller_id, api_key)

# ============================================================================
# DNS RECORD MANAGEMENT
# ============================================================================

@mcp.tool()
def add_dns_record(
    domain_name: str,
    record_type: str,
    name: str,
    content: str,
    ttl: int = 3600,
    priority: Optional[int] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a DNS record to a zone.

    Args:
        domain_name: The domain name
        record_type: Type of record (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA)
        name: Record name (e.g., "www", "@" for root)
        content: Record content (IP address, hostname, text value)
        ttl: Time to live in seconds (default 3600)
        priority: Priority for MX/SRV records (required for those types)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with record creation result
    """
    params = {
        "domainName": domain_name,
        "type": record_type.upper(),
        "name": name,
        "content": content,
        "TTL": ttl
    }

    # Add priority for record types that require it
    if record_type.upper() in ["MX", "SRV"] and priority is not None:
        params["priority"] = priority
    elif record_type.upper() in ["MX", "SRV"]:
        return {"error": f"Priority is required for {record_type} records"}

    return base.safe_soap_call("addDNSRecord", params, reseller_id, api_key)

@mcp.tool()
def delete_dns_record(
    domain_name: str,
    record_id: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a DNS record from a zone.

    Args:
        domain_name: The domain name
        record_id: ID of the record to delete
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with deletion result
    """
    return base.safe_soap_call("deleteDNSRecord", {
        "domainName": domain_name,
        "recordID": record_id
    }, reseller_id, api_key)

@mcp.tool()
def update_dns_record(
    domain_name: str,
    record_id: str,
    record_type: Optional[str] = None,
    name: Optional[str] = None,
    content: Optional[str] = None,
    ttl: Optional[int] = None,
    priority: Optional[int] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing DNS record.

    Args:
        domain_name: The domain name
        record_id: ID of the record to update
        record_type: New record type (optional)
        name: New record name (optional)
        content: New record content (optional)
        ttl: New TTL value (optional)
        priority: New priority for MX/SRV records (optional)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with update result
    """
    params = {
        "domainName": domain_name,
        "recordID": record_id
    }

    # Add optional update parameters
    if record_type:
        params["type"] = record_type.upper()
    if name is not None:
        params["name"] = name
    if content is not None:
        params["content"] = content
    if ttl is not None:
        params["TTL"] = ttl
    if priority is not None:
        params["priority"] = priority

    if len(params) == 2:  # Only domain and record ID provided
        return {"error": "At least one field to update must be provided"}

    return base.safe_soap_call("updateDNSRecord", params, reseller_id, api_key)

@mcp.tool()
def bulk_update_dns(
    domain_name: str,
    records: List[Dict[str, Any]],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update multiple DNS records at once.

    Args:
        domain_name: The domain name
        records: List of record updates, each containing:
            - record_id: ID of record to update
            - type: Record type (optional)
            - name: Record name (optional)
            - content: Record content (optional)
            - ttl: TTL value (optional)
            - priority: Priority for MX/SRV (optional)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with update results for each record
    """
    if len(records) > 50:
        return {"error": "Maximum 50 records can be updated at once"}

    results = {}
    for record_info in records:
        record_id = record_info.get("record_id")
        if not record_id:
            results[f"record_{len(results)}"] = {"error": "Missing record_id"}
            continue

        result = update_dns_record(
            domain_name=domain_name,
            record_id=record_id,
            record_type=record_info.get("type"),
            name=record_info.get("name"),
            content=record_info.get("content"),
            ttl=record_info.get("ttl"),
            priority=record_info.get("priority"),
            reseller_id=reseller_id,
            api_key=api_key
        )
        results[record_id] = result

    return results

# ============================================================================
# EMAIL FORWARDING
# ============================================================================

@mcp.tool()
def add_email_forward(
    domain_name: str,
    source_email: str,
    destination_email: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Set up email forwarding for a domain.

    Args:
        domain_name: The domain name
        source_email: Source email address (e.g., "info" or "info@domain.com")
        destination_email: Destination email address to forward to
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with forwarding setup result
    """
    # Ensure source email is properly formatted
    if "@" not in source_email:
        source_email = f"{source_email}@{domain_name}"

    return base.safe_soap_call("addMailForward", {
        "domainName": domain_name,
        "sourceEmail": source_email,
        "destinationEmail": destination_email
    }, reseller_id, api_key)

@mcp.tool()
def delete_email_forward(
    domain_name: str,
    source_email: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove email forwarding for a domain.

    Args:
        domain_name: The domain name
        source_email: Source email address to remove forwarding for
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with forwarding removal result
    """
    # Ensure source email is properly formatted
    if "@" not in source_email:
        source_email = f"{source_email}@{domain_name}"

    return base.safe_soap_call("deleteMailForward", {
        "domainName": domain_name,
        "sourceEmail": source_email
    }, reseller_id, api_key)

@mcp.tool()
def list_email_forwards(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all email forwarding rules for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of email forwarding rules
    """
    return base.safe_soap_call("listMailForwards", {"domainName": domain_name}, reseller_id, api_key)

# ============================================================================
# URL FORWARDING
# ============================================================================

@mcp.tool()
def add_url_forward(
    domain_name: str,
    subdomain: str,
    destination_url: str,
    forward_type: str = "301",
    forward_title: Optional[str] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Set up URL forwarding/redirect for a domain.

    Args:
        domain_name: The domain name
        subdomain: Subdomain to forward (use "@" for root domain, "www" for www)
        destination_url: URL to forward to (must include http:// or https://)
        forward_type: Type of forward ("301" for permanent, "302" for temporary, "frame" for masked)
        forward_title: Title for framed forwarding (optional, only for "frame" type)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with URL forwarding setup result
    """
    if forward_type not in ["301", "302", "frame"]:
        return {"error": "forward_type must be '301', '302', or 'frame'"}

    params = {
        "domainName": domain_name,
        "subdomain": subdomain,
        "destinationURL": destination_url,
        "type": forward_type
    }

    if forward_type == "frame" and forward_title:
        params["title"] = forward_title

    return base.safe_soap_call("addSimpleURLForward", params, reseller_id, api_key)

@mcp.tool()
def delete_url_forward(
    domain_name: str,
    subdomain: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove URL forwarding for a domain.

    Args:
        domain_name: The domain name
        subdomain: Subdomain to remove forwarding for
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with forwarding removal result
    """
    return base.safe_soap_call("deleteSimpleURLForward", {
        "domainName": domain_name,
        "subdomain": subdomain
    }, reseller_id, api_key)

@mcp.tool()
def list_url_forwards(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all URL forwarding rules for a domain.

    Args:
        domain_name: The domain name
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of URL forwarding rules
    """
    return base.safe_soap_call("listSimpleURLForwards", {"domainName": domain_name}, reseller_id, api_key)

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