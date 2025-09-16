# **Synergy Wholesale API \- Quick Start Guide**

This document provides a condensed overview of the Synergy Wholesale API (v3.11) to serve as a starting point for development.

## **1\. Core Concepts & Connection**

* **API Method**: SOAP/WSDL  
* **API Endpoint**: https://api.synergywholesale.com  
* **Authentication**: Every API call requires your resellerID and apiKey.  
* **Case-Sensitivity**: All API commands and parameter names are **case-sensitive** (e.g., apiKey, not apikey).  
* **IP Whitelisting**: You must provide the IP address of your server to Synergy Wholesale for it to be able to connect to the API.

## **2\. Request & Response Format**

All requests pass parameters in a single structure. All responses contain a status and, if an error occurs, an errorMessage.

### **Standard Request Structure**

All commands require your authentication credentials alongside the command-specific parameters.

{  
  "resellerID": "YOUR\_RESELLER\_ID",  
  "apiKey": "YOUR\_API\_KEY",  
  ... (command-specific parameters)  
}

### **Standard Successful Response**

A successful command will typically return a status of OK.

{  
  "status": "OK",  
  ... (response-specific data)  
}

### **Standard Error Response**

A failed command will return a status starting with ERR\_ and a descriptive errorMessage.

{  
  "status": "ERR\_LOGIN\_FAILED",  
  "errorMessage": "Unable to login to wholesale system"  
}

## **3\. Key API Commands (by Category)**

This is a curated list of the most common commands. Note that many older, region-specific commands (e.g., domainRegisterAU, domainRegisterUK) have been **deprecated** in favor of more generic commands like domainRegister.

### **Account Management**

* **balanceQuery**: Fetches your current account balance.

### **Domain Availability & Information**

* **checkDomain**: Checks if a single domain is available for registration.  
* **bulkCheckDomain**: Checks the availability of up to 30 domain names in a single call.  
* **domainInfo**: Retrieves detailed information for a specific domain, including status, expiry date, nameservers, and password (EPP code).  
* **bulkDomainInfo**: Retrieves detailed information for multiple domains at once.  
* **listDomains**: Returns a paginated list of all domains in your account.  
* **getDomainPricing**: Returns all pricing for the TLDs available to you.

### **Domain Registration & Transfer**

* **domainRegister**: The primary command for registering all domain extensions. It handles TLD-specific requirements via an eligibility parameter.  
* **isDomainTransferrable**: Checks if a domain can be transferred using a given password (EPP code).  
* **transferDomain**: Initiates the transfer of a domain into your account.

### **Domain Management**

* **renewDomain**: Renews an existing domain name.  
* **updateDomainPassword**: Updates the password (EPP code) for a domain.  
* **updateNameServers**: Updates the nameservers for a domain. Can also be used to set up parking, forwarding, or DNS hosting using the dnsConfig parameter.  
* **updateContact**: Updates the registrant, admin, billing, or technical contact details for a domain.  
* **lockDomain / unlockDomain**: Enables or disables the registrar lock on a domain.  
* **enableAutoRenewal / disableAutoRenewal**: Toggles the auto-renewal setting for a domain.

### **DNS Management**

* **addDNSZone**: Creates a new DNS zone.  
* **listDNSZone**: Lists all records within a DNS zone.  
* **addDNSRecord**: Adds a new DNS record (A, CNAME, MX, TXT, etc.).  
* **deleteDNSRecord**: Deletes a DNS record using its recordID.

### **Other Services**

The API also includes comprehensive commands for managing:

* **Hosting Services**: hostingPurchaseService, hostingSuspendService, hostingChangePassword, etc.  
* **SSL Certificates**: SSL\_purchaseSSLCertificate, SSL\_getSSLCertificate, SSL\_renewSSLCertificate, etc.  
* **Microsoft 365**: subscriptionCreateClient, subscriptionPurchase, subscriptionUpdateQuantity, etc.

## **4\. Important Implementation Notes**

* **Complex Parameters**:  
  * Multiple values, like nameservers or domain lists for bulk operations, are passed as **arrays**.  
  * Contact details are passed using prefixed field names (e.g., registrant\_firstname, registrant\_address, tech\_firstname, etc.).  
* **Eligibility**: For TLDs with specific registration requirements (like .au or .us), the domainRegister and transferDomain commands accept a JSON-encoded eligibility string. Use the getDomainEligibilityFields command to determine what fields are required for a given extension.