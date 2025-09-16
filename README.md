# Synergy Wholesale MCP Servers

A collection of 6 specialized MCP (Model Context Protocol) servers for comprehensive Synergy Wholesale API integration. Each server focuses on a specific domain of functionality, providing 77+ tools total for domain and DNS management.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Synergy Wholesale reseller account
- API credentials (reseller ID and API key)
- IP address whitelisted with Synergy Wholesale

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastmcp-synergy-wholesale.git
cd fastmcp-synergy-wholesale
```

2. Install dependencies for the server you want to use:
```bash
cd synergy-wholesale-discovery-mcp
pip install -r requirements.txt
```

3. Run the server:
```bash
python server.py
```

## 📦 Available Servers

### 1. Discovery & Registration Server
**`synergy-wholesale-discovery-mcp`** - 8 tools

Find and register domains:
- Domain availability checking
- Bulk availability checks (up to 30)
- TLD pricing and eligibility
- Domain registration (single & bulk)
- Renewal status checking

### 2. Portfolio Management Server
**`synergy-wholesale-portfolio-mcp`** - 18 tools

Manage your existing domains:
- List and query domains
- Update nameservers and passwords
- Lock/unlock domains
- Auto-renewal settings
- WHOIS privacy protection
- Contact management
- Domain renewals

### 3. Transfers Server
**`synergy-wholesale-transfers-mcp`** - 10 tools

Handle domain transfers:
- Transfer eligibility checking
- Initiate inbound transfers
- Bulk transfers
- Approve/reject outbound transfers
- Transfer lock management
- Transfer status monitoring

### 4. DNS & Routing Server
**`synergy-wholesale-dns-mcp`** - 14 tools

Manage DNS and forwarding:
- DNS zone management
- DNS record CRUD (A, AAAA, CNAME, MX, TXT, etc.)
- Bulk DNS updates
- Email forwarding setup
- URL forwarding/redirects

### 5. Advanced Operations Server
**`synergy-wholesale-advanced-mcp`** - 18 tools

Advanced registry features:
- Registry hosts (glue records)
- DNSSEC configuration
- Domain categories
- .AU Change of Registrant (CoR)
- ABN/ACN/RBN lookups
- .US nexus data

### 6. Account & Utilities Server
**`synergy-wholesale-account-mcp`** - 9 tools

Account management and diagnostics:
- Balance checking
- Transaction history
- Invoice management
- Renewal checks
- ICANN verification
- API connectivity testing

## 🔑 Authentication

All servers support two authentication methods:

### Method 1: Environment Variables
Set credentials once in your environment:
```bash
export SYNERGY_RESELLER_ID="your_reseller_id"
export SYNERGY_API_KEY="your_api_key"
```

### Method 2: Dynamic Credentials (Recommended)
Pass credentials with each tool call:
```json
{
  "domain_name": "example.com",
  "reseller_id": "your_reseller_id",
  "api_key": "your_api_key"
}
```

## 🖥️ Configuration for Claude Desktop

### Local Installation
Edit your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "synergy-discovery": {
      "command": "python",
      "args": ["path/to/synergy-wholesale-discovery-mcp/server.py"],
      "env": {
        "SYNERGY_RESELLER_ID": "your_reseller_id",
        "SYNERGY_API_KEY": "your_api_key"
      }
    },
    "synergy-dns": {
      "command": "python",
      "args": ["path/to/synergy-wholesale-dns-mcp/server.py"],
      "env": {
        "SYNERGY_RESELLER_ID": "your_reseller_id",
        "SYNERGY_API_KEY": "your_api_key"
      }
    }
    // Add other servers as needed
  }
}
```

### FastMCP Cloud Deployment
Deploy to FastMCP Cloud for remote access:

1. Push each server to its own GitHub repository
2. Deploy on [fastmcp.cloud](https://fastmcp.cloud)
3. Configure in Claude Desktop:

```json
{
  "mcpServers": {
    "synergy-discovery": {
      "url": "https://your-discovery-server.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

## 📚 Usage Examples

### Check Domain Availability
```python
# Using discovery server
result = await client.call_tool("check_domain", {
    "domain_name": "example.com.au",
    "reseller_id": "YOUR_ID",
    "api_key": "YOUR_KEY"
})
```

### Add DNS Record
```python
# Using DNS server
result = await client.call_tool("add_dns_record", {
    "domain_name": "example.com",
    "record_type": "A",
    "name": "www",
    "content": "192.0.2.1",
    "ttl": 3600,
    "reseller_id": "YOUR_ID",
    "api_key": "YOUR_KEY"
})
```

### .AU Change of Registrant
```python
# Using advanced server
result = await client.call_tool("au_change_registrant_request", {
    "domain_name": "example.com.au",
    "new_registrant": {
        "firstname": "John",
        "lastname": "Doe",
        "organisation": "Example Pty Ltd",
        "email": "john@example.com.au",
        "phone": "+61.298765432",
        "address": "123 Example St",
        "city": "Sydney",
        "state": "NSW",
        "postcode": "2000",
        "country": "AU"
    },
    "new_eligibility": {
        "registrantID": "12345678910",
        "registrantIDType": "ABN",
        "eligibilityType": "Company",
        "eligibilityName": "Example Pty Ltd",
        "eligibilityID": "12345678910"
    },
    "explanation": "Change of company ownership",
    "reseller_id": "YOUR_ID",
    "api_key": "YOUR_KEY"
})
```

## 🏗️ Architecture

### Shared Components
All servers use a common base class (`shared/base_server.py`) that provides:
- SOAP client initialization
- Authentication handling
- Response serialization
- Error handling
- Debug logging

### Benefits
- **Modular**: Load only the servers you need
- **Focused**: Each server has a clear purpose
- **Scalable**: Easy to add new servers or tools
- **Maintainable**: Update servers independently
- **Secure**: Credentials never stored on server

## 🐛 Troubleshooting

### Missing Credentials Error
- Ensure credentials are set in environment or passed with each call
- Check for typos in reseller ID and API key

### Connection Errors
- Verify your IP is whitelisted with Synergy Wholesale
- Check network connectivity to api.synergywholesale.com
- Enable debug logging: `export LOG_LEVEL=DEBUG`

### SOAP Faults
- Check API documentation for required parameters
- Verify domain ownership for management operations
- Ensure sufficient account balance for registrations

## 📖 Documentation

- [Synergy Wholesale API Documentation](https://www.synergywholesale.com/api/documentation)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Synergy Wholesale API](https://www.synergywholesale.com)
- SOAP client using [Zeep](https://github.com/mvantellingen/python-zeep)