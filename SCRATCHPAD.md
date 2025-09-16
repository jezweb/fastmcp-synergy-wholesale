# Development Scratchpad - Synergy Wholesale MCP Servers

## Current Status
- [x] Project structure created
- [x] Shared base class implemented
- [x] Server 1: Discovery & Registration (8 tools) ✅

## In Progress
Building Server 4: DNS & Routing Management

## Completed
- [x] Server 1: Discovery & Registration (8 tools) ✅
- [x] Server 2: Portfolio Management (18 tools) ✅
- [x] Server 3: Transfers (10 tools) ✅

## Servers Remaining
- [ ] Server 2: Portfolio Management (16 tools)
- [ ] Server 3: Transfers (9 tools)
- [ ] Server 4: DNS & Routing (14 tools)
- [ ] Server 5: Advanced Operations (18 tools)
- [ ] Server 6: Account & Utilities (8 tools)

## Git Commit Plan
- Commit after each server completion
- Include tool count in commit message
- Update documentation with each commit

## Notes
- All servers use shared base_server.py
- Each supports dynamic credentials
- Following consistent pattern from Server 1

## API Methods Reference
From the PDF documentation, tracking which methods go in which server...

### Server 2 Methods to Implement:
- listDomains
- domainInfo
- bulkDomainInfo
- updateNameServers
- updateDomainPassword
- lockDomain/unlockDomain
- enableAutoRenewal/disableAutoRenewal
- enableIDPrivacyProtection/disableIDPrivacyProtection
- renewDomain
- updateContacts
- listContacts
- getRawContacts
- listIDProtectedContacts
- resendRegistrantUpdateEmail
- cancelPendingRegistrantUpdate