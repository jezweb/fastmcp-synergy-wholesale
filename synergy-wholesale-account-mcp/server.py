#!/usr/bin/env python3
"""
Synergy Wholesale Account & Utilities MCP Server
Provides tools for account management and diagnostic utilities
"""

import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from fastmcp import FastMCP
from base_server import SynergyWholesaleBase

# Initialize FastMCP server
mcp = FastMCP(
    name="Synergy Wholesale Account",
    version="1.0.0",
    instructions="""
    This server provides account management and utility tools for Synergy Wholesale.

    Key features:
    - Account balance checking
    - Transaction history
    - Invoice management
    - Domain renewal checks
    - ICANN verification
    - API connectivity testing

    All tools support dynamic credential passing or environment variables:
    - SYNERGY_RESELLER_ID: Your Synergy Wholesale reseller ID
    - SYNERGY_API_KEY: Your Synergy Wholesale API key
    """
)

# Initialize base server
base = SynergyWholesaleBase("SynergyAccount")

# ============================================================================
# ACCOUNT INFORMATION
# ============================================================================

@mcp.tool()
def balance_query(
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check your account balance.

    Args:
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with account balance information
    """
    result = base.safe_soap_call("balanceQuery", {}, reseller_id, api_key)

    # Ensure we return the balance information
    if result and "error" not in result:
        base.logger.info(f"Balance query successful: ${result.get('balance', 'N/A')}")

    return result

@mcp.tool()
def get_transaction_history(
    days: int = 30,
    limit: int = 100,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get recent transaction history.

    Args:
        days: Number of days of history to retrieve (default 30)
        limit: Maximum number of transactions (default 100)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with transaction history
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    return base.safe_soap_call("getTransactionHistory", {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "limit": limit
    }, reseller_id, api_key)

@mcp.tool()
def get_invoice_list(
    year: Optional[int] = None,
    month: Optional[int] = None,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    List invoices for a specific period.

    Args:
        year: Year to retrieve invoices for (default current year)
        month: Month to retrieve invoices for (1-12, default all months)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of invoices
    """
    params = {}

    if year:
        params["year"] = year
    else:
        params["year"] = datetime.now().year

    if month and 1 <= month <= 12:
        params["month"] = month

    return base.safe_soap_call("getInvoiceList", params, reseller_id, api_key)

# ============================================================================
# DOMAIN RENEWAL MANAGEMENT
# ============================================================================

@mcp.tool()
def domain_renew_required_check(
    days_ahead: int = 60,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check which domains need renewal within a specified period.

    Args:
        days_ahead: Number of days to look ahead (default 60)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of domains requiring renewal
    """
    return base.safe_soap_call("domainRenewRequired", {
        "daysAhead": days_ahead
    }, reseller_id, api_key)

@mcp.tool()
def max_years_domain_renewable(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check the maximum number of years a domain can be renewed for.

    Args:
        domain_name: Domain to check
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with maximum renewable years
    """
    return base.safe_soap_call("getMaxYearsCanRenewFor", {
        "domainName": domain_name
    }, reseller_id, api_key)

@mcp.tool()
def get_transfer_away_list(
    days: int = 30,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of domains that have been transferred away.

    Args:
        days: Number of days to look back (default 30)
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with list of transferred domains
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    return base.safe_soap_call("getTransferredAwayDomains", {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d")
    }, reseller_id, api_key)

# ============================================================================
# VERIFICATION & COMPLIANCE
# ============================================================================

@mcp.tool()
def resend_icann_verification(
    domain_name: str,
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Resend ICANN registrant verification email.

    Args:
        domain_name: Domain requiring verification
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with email send result
    """
    return base.safe_soap_call("resendVerificationEmail", {
        "domainName": domain_name
    }, reseller_id, api_key)

# ============================================================================
# CONNECTIVITY & DIAGNOSTICS
# ============================================================================

@mcp.tool()
def test_api_connectivity(
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Test connectivity to the Synergy Wholesale API.

    Args:
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with connectivity test results
    """
    try:
        # Test basic connectivity by calling balance query
        base.logger.info("Testing API connectivity...")
        result = base.safe_soap_call("balanceQuery", {}, reseller_id, api_key)

        if "error" in result:
            return {
                "status": "error",
                "message": result["error"],
                "api_endpoint": base.get_soap_client().wsdl.location,
                "suggestion": "Check your credentials and IP whitelist settings"
            }

        return {
            "status": "connected",
            "message": "API connection successful",
            "api_endpoint": base.get_soap_client().wsdl.location,
            "api_version": "v3.11",
            "account_balance": result.get("balance"),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        base.logger.error(f"Connectivity test failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "error_type": type(e).__name__,
            "suggestion": "Verify network connectivity and WSDL availability"
        }

@mcp.tool()
def get_api_limits(
    reseller_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get current API rate limits and usage.

    Args:
        reseller_id: Optional Synergy Wholesale reseller ID
        api_key: Optional Synergy Wholesale API key

    Returns:
        Dictionary with API limits and usage information
    """
    # This might need to be mapped to a specific API call or might return static limits
    # For now, return known limits
    return {
        "rate_limits": {
            "requests_per_second": 10,
            "requests_per_minute": 100,
            "requests_per_hour": 1000,
            "bulk_domain_check_limit": 30,
            "bulk_domain_info_limit": 50,
            "bulk_transfer_limit": 10,
            "bulk_register_limit": 10
        },
        "timeout_seconds": 30,
        "max_nameservers": 6,
        "min_nameservers": 2,
        "max_domain_years": 10,
        "note": "These are general limits. Actual limits may vary based on your account."
    }

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