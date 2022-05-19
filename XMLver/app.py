import xml.etree.ElementTree as ET

data = ET.parse('test.xml')
tree = data.getroot()


tree[6] = DocumentCurrencyCode 
tree[8] = BuyerReference
tree[9][0] = AccountingSupplierParty
AccountingSupplierParty[2][0] = AccountingSupplierParty_Name
AccountingSupplierParty[3][0] = AccountingSupplierParty_StreetName
AccountingSupplierParty[3][1] = AccountingSupplierParty_AdditionalStreetName
AccountingSupplierParty[3][2] = AccountingSupplierParty_CityName
AccountingSupplierParty[3][3] = AccountingSupplierParty_PostalZone
AccountingSupplierParty[3][4][0] = AccountingSupplierParty_Country
AccountingSupplierParty[4][0] = AccountingSupplierParty_CompanyID
AccountingSupplierParty[5][0] = AccountingSupplierParty_RegistrationName
AccountingSupplierParty[5][1] = AccountingSupplierParty_LegalCompanyID
tree[10][0] = AccountingCustomerParty
AccountingCustomerParty[1][0] = AccountingCustomerParty_Name
AccountingCustomerParty[2][0] = AccountingCustomerParty_StreetName
AccountingCustomerParty[2][1] = AccountingCustomerParty_AdditionalStreetName
AccountingCustomerParty[2][2] = AccountingCustomerParty_AdditionalCityName
AccountingCustomerParty[2][3] = AccountingCustomerParty_PostalZone
AccountingCustomerParty[2][4][0] = AccountingCustomerParty_Country
AccountingCustomerParty[3][0] = AccountingCustomerParty_CompanyID
AccountingCustomerParty[4][0] = AccountingCustomerParty_RegistrationName
AccountingCustomerParty[4][1] = AccountingCustomerParty_LegalCompanyID
AccountingCustomerParty[5][0] = AccountingCustomerParty_ContactName
AccountingCustomerParty[5][1] = AccountingCustomerParty_ContactTelephone
AccountingCustomerParty[5][2] = AccountingCustomerParty_ContactEmail
tree[11] = Delivery
Delivery[1][1][0] = Delivery_StreetName
Delivery[1][1][1] = Delivery_AdditionalStreetName
Delivery[1][1][2] = Delivery_CityName
Delivery[1][1][3] = Delivery_PostalZone
Delivery[1][1][4][0] = Delivery_Country
tree[13] = PaymentTerms
PaymentTerms[0] = PaymentTerms_Note
tree[14] = TaxTotal
TaxTotal[0] = TaxTotal_TaxAmount
TaxTotal[1][0] = TaxTotal_SubTotalTaxableAmount
TaxTotal[1][1] = TaxTotal_SubTotalTaxAmount
TaxTotal[1][2][1] = TaxTotal_Percent
tree[15] = LegalMonetaryTotal
LegalMonetaryTotal[0] = LegalMonetaryTotal_LineExtensionAmount
LegalMonetaryTotal[1] = LegalMonetaryTotal_TaxExclusiveAmount
LegalMonetaryTotal[2] = LegalMonetaryTotal_TaxInclusiveAmount
LegalMonetaryTotal[3] = LegalMonetaryTotal_PayableAmount
tree[16] = InvoiceLine1
InvoiceLine1[4][0] = InvoiceLine1_ItemDescription
InvoiceLine1[4][1] = InvoiceLine1_ItemName
InvoiceLine1[4][6][1] = InvoiceLine1_TaxPercent
tree[17] = InvoiceLine2
InvoiceLine2[4][0] = InvoiceLine2_ItemDescription
InvoiceLine2[4][1] = InvoiceLine2_ItemName
InvoiceLine2[4][6][1] = InvoiceLine2_TaxPercent

tree[6].text = '7'

print(InvoiceLine2_TaxPercent.text)

b_xml = ET.tostring(tree)
with open("test2.xml", "wb") as f:
    f.write(b_xml)