class Customer:
    customer_id               : int
    first_name                : str
    last_name                 : str
    company                   : str
    primary_phone             : str
    contact_phone             : str
    email                     : str
    drivers_license           : int
    store_credit              : float
    preferred_contact_methods : list[str]
    billing_agent             : str
    net_terms                 : str
    postal_code               : int
    referral_source_id        : None
    street1                   : str
    street2                   : str
    country                   : str
    state                     : str
    city                      : str

    def __init__(self, customerId:int, firstName: str, lastName: str, company: str, primaryPhone: str, contactPhone: str, email: str, driversLicense: int, \
                 storeCredit: float, preferredContactMethods: list[str], billingAgent: str, netTerms: str, postalCode: int, referralSourceId: str,         \
                 street1: str, street2: str, country: str, state: str, city: str):
        self.customer_id = customerId
        self.first_name = firstName
        self.last_name = lastName
        self.company = company
        self.primary_phone = primaryPhone
        self.contact_phone = contactPhone
        self.email = email
        self.drivers_license = driversLicense
        self.store_credit = storeCredit
        self.preferred_contact_methods = preferredContactMethods
        self.billing_agent = billingAgent
        self.net_terms = netTerms
        self.postal_code = postalCode
        self.referral_source_id = referralSourceId
        self.street1 = street1
        self.street2 = street2
        self.country = country
        self.state = state
        self.city = city

    def __dict__(self):
        return {"id": self.customer_id, "firstName": self.first_name, "lastName": self.last_name, "company": self.company, "primaryPhone": self.primary_phone,            \
                "contactPhone": self.contact_phone, "email": self.email, "driversLicense": self.drivers_license, "storeCredit": self.store_credit,                        \
                "preferredContactMethods": self.preferred_contact_methods if len(self.preferred_contact_methods) != 0 else None, "billingAgent": self.billing_agent,      \
                "netTerms": self.net_terms, "postalCode": self.postal_code, "referralSourceId": self.referral_source_id, "street1": self.street1, "street2": self.street2,\
                "country": self.country, "state": self.state, "city": self.city}
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"