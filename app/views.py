from django.shortcuts import render
from sqlalchemy import create_engine, exc
import hashlib
import pandas as pd
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Create your views here.
def login(request):
    return render(request, 'login.html')

def connection():
    try:
        conn = create_engine('mysql+pymysql://root:root@localhost/stock')
    except exc.SQLAlchemyError as e:
        print(e)

    return conn


conn = connection()

def validation(request):
    return render(request, 'index.html')


def registration(request):
    conn = connection()
    try:
        uname = request.POST.dict().get('username')
        fname = request.POST.dict().get('fname')
        lname = request.POST.dict().get('lname')
        pword = request.POST.dict().get('pword')
        email = request.POST.dict().get('email')
        modules = request.POST.getlist('modules')
        modules = ", ".join(modules)
        encpw = hashlib.sha256(pword.encode()).hexdigest()
        conn.execute(
            f"INSERT into users (username,firstname,lastname,password,email,modules) VALUES ('{uname}','{fname}','{lname}','{encpw}','{email}','{modules}')")
        conn.dispose()
    except Exception as e:
        print(e)
    return render(request, 'login.html')


def intelliextract(request):
    return render(request, 'intelliextract.html')


def search_history(request):
    return render(request, 'search-history.html')

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = "https://ai-adi.cognitiveservices.azure.com/"
key = "8f3ce2551e3c484888f9c4c83a085ae3"

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join("Page #{}: {}".format(region.page_number, format_polygon(region.polygon)) for region in bounding_regions)

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

def analyze_invoice(request):
    id = [1,2,3,4,5]
    return render(request,'intelliextract.html',{'id':id})

# def analyze_invoice(request):
#
#     invoiceUrl = request.FILES['pdf']
#     print(invoiceUrl,'hfjfkl')
#     document_analysis_client = DocumentAnalysisClient(
#         endpoint=endpoint, credential=AzureKeyCredential(key)
#     )
#
#     with open(invoiceUrl, "rb") as f:
#        poller = document_analysis_client.begin_analyze_document(
#            "prebuilt-invoice", document=f, locale="en-US"
#        )
#     # poller = document_analysis_client.begin_analyze_document(
#     #         "prebuilt-invoice", invoiceUrl)
#     invoices = poller.result()
#     print(invoices)
#
#     for idx, invoice in enumerate(invoices.documents):
#         print("--------Recognizing invoice #{}--------".format(idx + 1))
#         vendor_name = invoice.fields.get("VendorName")
#         if vendor_name:
#             print(
#                 "Vendor Name: {} has confidence: {}".format(
#                     vendor_name.value, vendor_name.confidence
#                 )
#             )
#         vendor_address = invoice.fields.get("VendorAddress")
#         if vendor_address:
#             print(
#                 "Vendor Address: {} has confidence: {}".format(
#                     vendor_address.value, vendor_address.confidence
#                 )
#             )
#         vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
#         if vendor_address_recipient:
#             print(
#                 "Vendor Address Recipient: {} has confidence: {}".format(
#                     vendor_address_recipient.value, vendor_address_recipient.confidence
#                 )
#             )
#         customer_name = invoice.fields.get("CustomerName")
#         if customer_name:
#             print(
#                 "Customer Name: {} has confidence: {}".format(
#                     customer_name.value, customer_name.confidence
#                 )
#             )
#         customer_id = invoice.fields.get("CustomerId")
#         if customer_id:
#             print(
#                 "Customer Id: {} has confidence: {}".format(
#                     customer_id.value, customer_id.confidence
#                 )
#             )
#         customer_address = invoice.fields.get("CustomerAddress")
#         if customer_address:
#             print(
#                 "Customer Address: {} has confidence: {}".format(
#                     customer_address.value, customer_address.confidence
#                 )
#             )
#         customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
#         if customer_address_recipient:
#             print(
#                 "Customer Address Recipient: {} has confidence: {}".format(
#                     customer_address_recipient.value,
#                     customer_address_recipient.confidence,
#                 )
#             )
#         invoice_id = invoice.fields.get("InvoiceId")
#         if invoice_id:
#             print(
#                 "Invoice Id: {} has confidence: {}".format(
#                     invoice_id.value, invoice_id.confidence
#                 )
#             )
#         invoice_date = invoice.fields.get("InvoiceDate")
#         if invoice_date:
#             print(
#                 "Invoice Date: {} has confidence: {}".format(
#                     invoice_date.value, invoice_date.confidence
#                 )
#             )
#         invoice_total = invoice.fields.get("InvoiceTotal")
#         if invoice_total:
#             print(
#                 "Invoice Total: {} has confidence: {}".format(
#                     invoice_total.value, invoice_total.confidence
#                 )
#             )
#         due_date = invoice.fields.get("DueDate")
#         if due_date:
#             print(
#                 "Due Date: {} has confidence: {}".format(
#                     due_date.value, due_date.confidence
#                 )
#             )
#         purchase_order = invoice.fields.get("PurchaseOrder")
#         if purchase_order:
#             print(
#                 "Purchase Order: {} has confidence: {}".format(
#                     purchase_order.value, purchase_order.confidence
#                 )
#             )
#         billing_address = invoice.fields.get("BillingAddress")
#         if billing_address:
#             print(
#                 "Billing Address: {} has confidence: {}".format(
#                     billing_address.value, billing_address.confidence
#                 )
#             )
#         billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
#         if billing_address_recipient:
#             print(
#                 "Billing Address Recipient: {} has confidence: {}".format(
#                     billing_address_recipient.value,
#                     billing_address_recipient.confidence,
#                 )
#             )
#         shipping_address = invoice.fields.get("ShippingAddress")
#         if shipping_address:
#             print(
#                 "Shipping Address: {} has confidence: {}".format(
#                     shipping_address.value, shipping_address.confidence
#                 )
#             )
#         shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
#         if shipping_address_recipient:
#             print(
#                 "Shipping Address Recipient: {} has confidence: {}".format(
#                     shipping_address_recipient.value,
#                     shipping_address_recipient.confidence,
#                 )
#             )
#         print("Invoice items:")
#         if invoice.fields.get("Items"):
#             for idx, item in enumerate(invoice.fields.get("Items").value):
#                 print("...Item #{}".format(idx + 1))
#                 item_description = item.value.get("Description")
#                 if item_description:
#                     print(
#                         "......Description: {} has confidence: {}".format(
#                             item_description.value, item_description.confidence
#                         )
#                     )
#                 item_quantity = item.value.get("Quantity")
#                 if item_quantity:
#                     print(
#                         "......Quantity: {} has confidence: {}".format(
#                             item_quantity.value, item_quantity.confidence
#                         )
#                     )
#                 unit = item.value.get("Unit")
#                 if unit:
#                     print(
#                         "......Unit: {} has confidence: {}".format(
#                             unit.value, unit.confidence
#                         )
#                     )
#                 unit_price = item.value.get("UnitPrice")
#                 if unit_price:
#                     print(
#                         "......Unit Price: {} has confidence: {}".format(
#                             unit_price.value, unit_price.confidence
#                         )
#                     )
#                 product_code = item.value.get("ProductCode")
#                 if product_code:
#                     print(
#                         "......Product Code: {} has confidence: {}".format(
#                             product_code.value, product_code.confidence
#                         )
#                     )
#                 item_date = item.value.get("Date")
#                 if item_date:
#                     print(
#                         "......Date: {} has confidence: {}".format(
#                             item_date.value, item_date.confidence
#                         )
#                     )
#                 tax = item.value.get("Tax")
#                 if tax:
#                     print(
#                         "......Tax: {} has confidence: {}".format(tax.value, tax.confidence)
#                     )
#                 amount = item.value.get("Amount")
#                 if amount:
#                     print(
#                         "......Amount: {} has confidence: {}".format(
#                             amount.value, amount.confidence
#                         )
#                     )
#         subtotal = invoice.fields.get("SubTotal")
#         if subtotal:
#             print(
#                 "Subtotal: {} has confidence: {}".format(
#                     subtotal.value, subtotal.confidence
#                 )
#             )
#         total_tax = invoice.fields.get("TotalTax")
#         if total_tax:
#             print(
#                 "Total Tax: {} has confidence: {}".format(
#                     total_tax.value, total_tax.confidence
#                 )
#             )
#         previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
#         if previous_unpaid_balance:
#             print(
#                 "Previous Unpaid Balance: {} has confidence: {}".format(
#                     previous_unpaid_balance.value, previous_unpaid_balance.confidence
#                 )
#             )
#         amount_due = invoice.fields.get("AmountDue")
#         if amount_due:
#             print(
#                 "Amount Due: {} has confidence: {}".format(
#                     amount_due.value, amount_due.confidence
#                 )
#             )
#         service_start_date = invoice.fields.get("ServiceStartDate")
#         if service_start_date:
#             print(
#                 "Service Start Date: {} has confidence: {}".format(
#                     service_start_date.value, service_start_date.confidence
#                 )
#             )
#         service_end_date = invoice.fields.get("ServiceEndDate")
#         if service_end_date:
#             print(
#                 "Service End Date: {} has confidence: {}".format(
#                     service_end_date.value, service_end_date.confidence
#                 )
#             )
#         service_address = invoice.fields.get("ServiceAddress")
#         if service_address:
#             print(
#                 "Service Address: {} has confidence: {}".format(
#                     service_address.value, service_address.confidence
#                 )
#             )
#         service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
#         if service_address_recipient:
#             print(
#                 "Service Address Recipient: {} has confidence: {}".format(
#                     service_address_recipient.value,
#                     service_address_recipient.confidence,
#                 )
#             )
#         remittance_address = invoice.fields.get("RemittanceAddress")
#         if remittance_address:
#             print(
#                 "Remittance Address: {} has confidence: {}".format(
#                     remittance_address.value, remittance_address.confidence
#                 )
#             )
#         remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
#         if remittance_address_recipient:
#             print(
#                 "Remittance Address Recipient: {} has confidence: {}".format(
#                     remittance_address_recipient.value,
#                     remittance_address_recipient.confidence,
#                 )
#             )

# if __name__ == "__main__":
#     analyze_invoice()
#
#     print("----------------------------------------")