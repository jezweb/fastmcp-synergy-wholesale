# Synergy Wholesale MCP Servers Implementation Plan

## Overview
Split the monolithic Synergy Wholesale MCP server into 6 focused servers for better organization and usability.

## Project Structure
```
fastmcp-synergy-wholesale/
├── synergy-wholesale-discovery-mcp/    # Server 1: Discovery & Registration
├── synergy-wholesale-portfolio-mcp/    # Server 2: Portfolio Management
├── synergy-wholesale-transfers-mcp/    # Server 3: Domain Transfers
├── synergy-wholesale-dns-mcp/          # Server 4: DNS & Routing
├── synergy-wholesale-advanced-mcp/     # Server 5: Advanced/Registry Ops
├── synergy-wholesale-account-mcp/      # Server 6: Account & Utilities
└── shared/
    ├── base_server.py                  # Shared base class
    ├── soap_client.py                  # Shared SOAP client logic
    └── auth.py                         # Shared authentication
```

## Server Specifications

### 🔍 Server 1: Domain Discovery & Registration
**Repository:** `synergy-wholesale-discovery-mcp`
**Purpose:** Finding and registering new domains

**Tools to implement:**
- [x] check_domain - Check single domain availability
- [x] bulk_check_domain - Check multiple domains (up to 30)
- [x] get_domain_pricing - Get all TLD pricing
- [x] get_domain_eligibility_fields - Get TLD-specific requirements
- [ ] list_available_extensions - List all available TLDs
- [x] register_domain - Register single domain
- [ ] bulk_register_domain - Register multiple domains
- [ ] determine_domain_renewable - Check if domain needs renewal

### 📋 Server 2: Domain Portfolio Management
**Repository:** `synergy-wholesale-portfolio-mcp`
**Purpose:** Managing existing domains and their settings

**Tools to implement:**
- [x] list_domains - List all domains in account
- [x] domain_info - Get detailed domain information
- [ ] bulk_domain_info - Get info for multiple domains
- [x] update_nameservers - Change nameservers
- [x] update_domain_password - Update EPP/auth code
- [x] lock_domain / unlock_domain - Transfer lock management
- [x] enable_auto_renewal / disable_auto_renewal - Auto-renewal settings
- [ ] enable_id_protection / disable_id_protection - WHOIS privacy
- [x] renew_domain - Renew single domain
- [ ] bulk_renew_domain - Renew multiple domains
- [ ] update_contacts - Update domain contacts
- [ ] list_contacts - View domain contacts
- [ ] get_raw_contacts - Get detailed contact info
- [ ] list_id_protected_contacts - Get protected contact info
- [ ] resend_registrant_email - Resend verification emails
- [ ] cancel_pending_registrant_update - Cancel pending updates

### 🔄 Server 3: Domain Transfers
**Repository:** `synergy-wholesale-transfers-mcp`
**Purpose:** Handling domain transfers in and out

**Tools to implement:**
- [x] is_domain_transferrable - Check transfer eligibility
- [x] transfer_domain - Initiate inbound transfer
- [ ] bulk_transfer_domain - Transfer multiple domains
- [ ] resend_transfer_email - Resend transfer approval
- [ ] cancel_inbound_transfer - Cancel incoming transfer
- [ ] approve_outbound_transfer - Approve outgoing transfer
- [ ] reject_outbound_transfer - Reject outgoing transfer
- [ ] transfer_lock / transfer_unlock - Manage transfer locks (specific)
- [ ] get_transfer_status - Check transfer progress

### 🌐 Server 4: DNS & Routing Management
**Repository:** `synergy-wholesale-dns-mcp`
**Purpose:** DNS records, email forwarding, URL forwarding

**Tools to implement:**
- [x] add_dns_zone - Create DNS zone
- [ ] delete_dns_zone - Remove DNS zone
- [x] list_dns_zone - List all DNS records
- [x] add_dns_record - Add DNS record (A, CNAME, MX, etc.)
- [x] update_dns_record - Update existing record
- [x] delete_dns_record - Remove DNS record
- [ ] bulk_update_dns - Update multiple records
- [ ] add_email_forward - Set up email forwarding
- [ ] delete_email_forward - Remove email forwarding
- [ ] list_email_forwards - List email forwards
- [ ] add_url_forward - Set up URL redirect
- [ ] delete_url_forward - Remove URL redirect
- [ ] list_url_forwards - List URL forwards

### 🏢 Server 5: Advanced/Registry Operations
**Repository:** `synergy-wholesale-advanced-mcp`
**Purpose:** Advanced features, DNSSEC, glue records, categories, .AU management

**Tools to implement:**
- [ ] add_registry_host - Add glue records
- [ ] delete_registry_host - Remove glue records
- [ ] add_registry_host_ip - Add IP to registry host
- [ ] delete_registry_host_ip - Remove IP from registry host
- [ ] list_registry_hosts - List all glue records
- [ ] registry_host_info - Get registry host details
- [ ] add_dnssec_record - Enable DNSSEC
- [ ] remove_dnssec_record - Remove DNSSEC
- [ ] list_dnssec_entries - List DNSSEC records
- [ ] dnssec_info - Get DNSSEC details
- [ ] create_domain_category - Organize domains
- [ ] update_domain_category - Update category
- [ ] remove_domain_category - Delete category
- [ ] assign_domain_category - Categorize domains
- [ ] unassign_domain_category - Remove from category
- [ ] list_domain_categories - View categories
- [ ] get_abn_acn_rbn_info - Lookup ABN/ACN/RBN
- [ ] generate_au_eligibility - Generate .au eligibility
- [ ] au_change_registrant_request - .AU Change of Registrant (CoR)
- [ ] retrieve_us_nexus_data - Get .US nexus data

### 💰 Server 6: Account & Utilities
**Repository:** `synergy-wholesale-account-mcp`
**Purpose:** Account management and diagnostic tools

**Tools to implement:**
- [x] balance_query - Check account balance
- [x] test_api_connectivity - Test API connection
- [ ] get_transaction_history - View recent transactions
- [ ] get_invoice_list - List invoices
- [ ] domain_renew_required_check - Check upcoming renewals
- [ ] max_years_domain_renewable - Check max renewal period
- [ ] get_transfer_away_list - List domains transferred away
- [ ] resend_icann_verification - Resend ICANN verification email

## Implementation Steps

### Phase 1: Setup Infrastructure
1. Create shared module structure
2. Extract common SOAP client logic
3. Create base server class with authentication
4. Set up error handling framework

### Phase 2: Build Servers (Priority Order)
1. **Server 1**: Discovery & Registration (most commonly used)
2. **Server 4**: DNS & Routing (essential for domain management)
3. **Server 2**: Portfolio Management (manage existing domains)
4. **Server 3**: Transfers (less frequent but important)
5. **Server 5**: Advanced Operations (specialized features)
6. **Server 6**: Account & Utilities (support functions)

### Phase 3: Testing & Documentation
1. Test each server with real credentials
2. Create comprehensive README for each server
3. Add example usage for each tool
4. Create integration tests

### Phase 4: Deployment
1. Create individual GitHub repositories
2. Configure for FastMCP Cloud deployment
3. Document configuration for Claude Desktop
4. Create meta-repository with links to all servers

## Shared Components

### base_server.py
```python
class SynergyWholesaleBase:
    - Authentication handling
    - SOAP client initialization
    - Error handling
    - Response serialization
```

### soap_client.py
```python
- get_soap_client()
- safe_soap_call()
- handle_soap_response()
```

### auth.py
```python
- validate_credentials()
- add_auth()
```

## Benefits
1. **Modularity**: Each server can be updated independently
2. **Focused Tools**: Users only load what they need
3. **Better Discovery**: Easier to find the right tool
4. **Performance**: Smaller, faster servers
5. **Maintainability**: Cleaner codebase per server
6. **Scalability**: Can add new servers for new feature areas

## Notes
- All servers support dynamic credential passing
- All servers will be FastMCP Cloud compatible
- Each server will have comprehensive error handling
- Documentation will include common workflows