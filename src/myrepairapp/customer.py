import enum

"""
{
  "id": "12345",
  "firstName": "John",
  "lastName": "Doe",
  "company": "ACME Corp",
  "primaryPhone": "123-456-7890",
  "contactPhone": "123-456-7890",
  "email": "john.doe@example.com",
  "driversLicense": "123456789",
  "storeCredit": 100.5,
  "preferredContactMethods": ["email", "phone"],
  "billingAgent": "John Smith",
  "netTerms": "30 days",
  "taxExempt": "No",
  "postalCode": "12345",
  "referralSourceId": null,
  "street1": "123 Main St",
  "street2": "Suite 100",
  "country": "US",
  "state": "CA",
  "city": "Los Angeles"
}
"""

class Customer:
    customer_id             : int
    firstName               : str
    lastName                : str
    company                 : str
    primaryPhone            : str
    contactPhone            : str
    email                   : str
    driversLicense          : int
    storeCredit             : float
    preferredContactMethods : list[str]
    billingAgent            : str