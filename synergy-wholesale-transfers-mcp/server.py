#!/usr/bin/env python3
"""
Synergy Wholesale Domain Transfers MCP Server
Provides tools for handling domain transfers in and out
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
    name="Synergy Wholesale Transfers",
    version="1.0.0",
    instructions="""
    This server provides domain transfer management tools for Synergy Wholesale.

    Key features:
    - Check transfer eligibility
    - Initiate inbound transfers
    - Manage transfer approvals and rejections
    - Cancel transfers
    - Check transfer status
    - Handle transfer locks

    All tools support dynamic credential passing or environment variables:
    - SYNERGY_RESELLER_ID: Your Synergy Wholesale reseller ID
    - SYNERGY_API_KEY: Your Synergy Wholesale API key
    """
)

# Initialize base server
base = SynergyWholesaleBase("SynergyTransfers")

# ============================================================================
# TRANSFER ELIGIBILITY & INITIATION
# ============================================================================

@mcp.tool()
def is_domain_transferrable(
    domain_name: str,
    auth_code: Optional[str] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check if a domain can be transferred.

    Args:
        domain_name: Domain to check
        auth_code: EPP/Authorization code (optional for initial check)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with transfer eligibility status
    """
    params = {"domainName": domain_name}
    if auth_code:
        params["authCode"] = auth_code
    return base.safe_soap_call("isDomainTransferrable", params, reseller_id, api_key)

@mcp.tool()
def transfer_domain(
    domain_name: str,
    auth_code: str,
    years: Optional[int] = None,
    id_protection: bool = False,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Initiate an inbound domain transfer.

    Args:
        domain_name: Domain to transfer
        auth_code: EPP/Authorization code from current registrar
        years: Years to add on transfer (optional)
        id_protection: Enable WHOIS privacy after transfer
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with transfer initiation result
    """
    params = {
        "domainName": domain_name,
        "authCode": auth_code
    }

    if years:
        params["years"] = years
    if id_protection:
        params["idProtection"] = "on"

    return base.safe_soap_call("transferDomain", params, reseller_id, api_key)

@mcp.tool()
def bulk_transfer_domain(
    domains: List[Dict[str, Any]],
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transfer multiple domains at once.

    Args:
        domains: List of transfer requests, each containing:
            - domain_name: Domain to transfer
            - auth_code: EPP/Authorization code
            - years: Years to add (optional)
            - id_protection: Enable privacy (optional)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with transfer results for each domain
    """
    if len(domains) > 10:
        return {"error": "Maximum 10 domains can be transferred at once"}

    results = {}
    for transfer_info in domains:
        domain_name = transfer_info.get("domain_name")
        auth_code = transfer_info.get("auth_code")

        if not domain_name:
            results[f"domain_{len(results)}"] = {"error": "Missing domain_name"}
            continue
        if not auth_code:
            results[domain_name] = {"error": "Missing auth_code"}
            continue

        result = transfer_domain(
            domain_name=domain_name,
            auth_code=auth_code,
            years=transfer_info.get("years"),
            id_protection=transfer_info.get("id_protection", False),
            reseller_id=reseller_id,
            api_key=api_key
        )
        results[domain_name] = result

    return results

# ============================================================================
# TRANSFER MANAGEMENT
# ============================================================================

@mcp.tool()
def resend_transfer_email(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Resend transfer approval email.

    Args:
        domain_name: Domain with pending transfer
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with email send result
    """
    return base.safe_soap_call("resendTransferApprovalEmail", {
        "domainName": domain_name
    }, reseller_id, api_key)

@mcp.tool()
def cancel_inbound_transfer(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cancel an incoming domain transfer.

    Args:
        domain_name: Domain with pending inbound transfer
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with cancellation result
    """
    return base.safe_soap_call("cancelInboundTransfer", {
        "domainName": domain_name
    }, reseller_id, api_key)

@mcp.tool()
def approve_outbound_transfer(
    domain_name: str,
    ack_key: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Approve an outgoing domain transfer.

    Args:
        domain_name: Domain being transferred away
        ack_key: Acknowledgment key from transfer request
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with approval result
    """
    return base.safe_soap_call("approveOutboundTransfer", {
        "domainName": domain_name,
        "ackKey": ack_key
    }, reseller_id, api_key)

@mcp.tool()
def reject_outbound_transfer(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Reject an outgoing domain transfer.

    Args:
        domain_name: Domain being transferred away
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with rejection result
    """
    return base.safe_soap_call("rejectOutboundTransfer", {
        "domainName": domain_name
    }, reseller_id, api_key)

# ============================================================================
# TRANSFER LOCKS
# ============================================================================

@mcp.tool()
def transfer_lock(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Apply transfer lock to prevent unauthorized transfers.

    Args:
        domain_name: Domain to lock
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with lock status
    """
    return base.safe_soap_call("transferLock", {
        "domainName": domain_name
    }, reseller_id, api_key)

@mcp.tool()
def transfer_unlock(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove transfer lock to allow transfers.

    Args:
        domain_name: Domain to unlock
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with unlock status
    """
    return base.safe_soap_call("transferUnlock", {
        "domainName": domain_name
    }, reseller_id, api_key)

# ============================================================================
# TRANSFER STATUS
# ============================================================================

@mcp.tool()
def get_transfer_status(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check the status of a pending transfer.

    Args:
        domain_name: Domain with pending transfer
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with transfer status details
    """
    # This might need to be mapped to a different API call depending on Synergy's implementation
    # Using domainInfo as it often contains transfer status
    result = base.safe_soap_call("domainInfo", {
        "domainName": domain_name
    }, reseller_id, api_key)

    # Extract transfer-related information if available
    if "error" not in result:
        transfer_info = {
            "domain": domain_name,
            "status": result.get("status"),
            "transfer_status": result.get("transferStatus"),
            "transfer_date": result.get("transferDate"),
            "current_registrar": result.get("registrar"),
            "locked": result.get("locked")
        }
        return transfer_info

    return result

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