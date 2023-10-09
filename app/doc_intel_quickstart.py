# import libraries
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
from hdbcli import dbapi
from hana_ml.dataframe import ConnectionContext
# import pandas as pd
# import os
from sqlalchemy import create_engine
import pyhdb
from sqlalchemy import create_engine, exc

def connection():
    try:
        conn = create_engine('mysql+pymysql://root:root@localhost/stock')
    except exc.SQLAlchemyError as e:
        print(e)

    return conn

conn=connection()
# connection = pyhdb.connect(
#     host='03b7ba32-1aca-46d2-b2ab-7e832d9d8881.hana.trial-us10.hanacloud.ondemand.com',
#     port=443,  # Default SAP HANA port
#     user='DBADMIN',
#     password='Acceron@123'
# )

# cursor = connection.cursor()


sapconn = dbapi.connect(
    address='03b7ba32-1aca-46d2-b2ab-7e832d9d8881.hana.trial-us10.hanacloud.ondemand.com',
    port=443,
    user='DBADMIN',
    password='Acceron@123'
)

print('jj')
cursor = sapconn.cursor()
# insert_query = "INSERT INTO your_table_name (column1, column2, ...) VALUES (?, ?, ...)"

# conn = dbapi.connect(address="03b7ba32-1aca-46d2-b2ab-7e832d9d8881.hana.trial-us10.hanacloud.ondemand.com",
#                      port=443,user="03b7ba32-1aca-46d2-b2ab-7e832d9d8881.hana.trial-us10.hanacloud.ondemand.com", password="Acceron@123")
# cursor = conn.cursor()
# engine = create_engine('hana://DBADMIN:Acceron@123@03b7ba32-1aca-46d2-b2ab-7e832d9d8881.hana.trial-us10.hanacloud.ondemand.com:443')

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


def analyze_invoice(invoiceUrl):
    print(invoiceUrl)
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    with open(invoiceUrl, "rb") as f:
       poller = document_analysis_client.begin_analyze_document(
           "prebuilt-invoice", document=f, locale="en-US"
       )
    # poller = document_analysis_client.begin_analyze_document(
    #         "prebuilt-invoice", invoiceUrl)
    invoices = poller.result()
    extracted = {}

    for idx, invoice in enumerate(invoices.documents):
        print(invoice)
        print("--------Recognizing invoice #{}--------".format(idx + 1))
        extracted[f'invoice{idx+1}'] = {}
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            extracted[f'invoice{idx+1}']['vendor_name'] = "Vendor Name: {} has confidence: {}".format(
                    vendor_name.value, vendor_name.confidence
                )
            print(
                "Vendor Name: {} has confidence: {}".format(
                    vendor_name.value, vendor_name.confidence
                )
            )
        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            extracted[f'invoice{idx+1}']['vendor_address'] = "Vendor Address: {} has confidence: {}".format(
                    vendor_address.value, vendor_address.confidence
                )
            print(
                "Vendor Address: {} has confidence: {}".format(
                    vendor_address.value, vendor_address.confidence
                )
            )
        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
            extracted[f'invoice{idx+1}']['vendor_address_recipient'] = "Vendor Address Recipient: {} has confidence: {}".format(
                    vendor_address_recipient.value, vendor_address_recipient.confidence
                )
            print(
                "Vendor Address Recipient: {} has confidence: {}".format(
                    vendor_address_recipient.value, vendor_address_recipient.confidence
                )
            )
        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
            extracted[f'invoice{idx+1}']['customer_name'] = "Customer Name: {} has confidence: {}".format(
                    customer_name.value, customer_name.confidence
                )
            print(
                "Customer Name: {} has confidence: {}".format(
                    customer_name.value, customer_name.confidence
                )
            )
        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
            extracted[f'invoice{idx+1}']['customer_id'] = "Customer Id: {} has confidence: {}".format(
                    customer_id.value, customer_id.confidence
                )
            print(
                "Customer Id: {} has confidence: {}".format(
                    customer_id.value, customer_id.confidence
                )
            )
        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
            extracted[f'invoice{idx+1}']['customer_address'] = "Customer Address: {} has confidence: {}".format(
                    customer_address.value, customer_address.confidence
                )
            print(
                "Customer Address: {} has confidence: {}".format(
                    customer_address.value, customer_address.confidence
                )
            )
        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
            extracted[f'invoice{idx+1}']['customer_address_recipient'] = "Customer Address Recipient: {} has confidence: {}".format(
                    customer_address_recipient.value,
                    customer_address_recipient.confidence,
                )
            print(
                "Customer Address Recipient: {} has confidence: {}".format(
                    customer_address_recipient.value,
                    customer_address_recipient.confidence,
                )
            )
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            extracted[f'invoice{idx+1}']['invoice_id'] = "Invoice Id: {} has confidence: {}".format(
                    invoice_id.value, invoice_id.confidence
                )
            print(
                "Invoice Id: {} has confidence: {}".format(
                    invoice_id.value, invoice_id.confidence
                )
            )
        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            extracted[f'invoice{idx+1}']['invoice_date'] = "Invoice Date: {} has confidence: {}".format(
                    invoice_date.value, invoice_date.confidence
                )
            print(
                "Invoice Date: {} has confidence: {}".format(
                    invoice_date.value, invoice_date.confidence
                )
            )
        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            extracted[f'invoice{idx+1}']['invoice_total'] = "Invoice Total: {} has confidence: {}".format(
                    invoice_total.value, invoice_total.confidence
                )
            print(
                "Invoice Total: {} has confidence: {}".format(
                    invoice_total.value, invoice_total.confidence
                )
            )
        due_date = invoice.fields.get("DueDate")
        if due_date:
            extracted[f'invoice{idx+1}']['due_date'] = "Due Date: {} has confidence: {}".format(
                    due_date.value, due_date.confidence
                )
            print(
                "Due Date: {} has confidence: {}".format(
                    due_date.value, due_date.confidence
                )
            )
        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order:
            extracted[f'invoice{idx+1}']['purchase_order'] = "Purchase Order: {} has confidence: {}".format(
                    purchase_order.value, purchase_order.confidence
                )
            print(
                "Purchase Order: {} has confidence: {}".format(
                    purchase_order.value, purchase_order.confidence
                )
            )
        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
            extracted[f'invoice{idx+1}']['billing_address'] = "Billing Address: {} has confidence: {}".format(
                    billing_address.value, billing_address.confidence
                )
            print(
                "Billing Address: {} has confidence: {}".format(
                    billing_address.value, billing_address.confidence
                )
            )
        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient:
            extracted[f'invoice{idx+1}']['billing_address_recipient'] = "Billing Address Recipient: {} has confidence: {}".format(
                    billing_address_recipient.value,
                    billing_address_recipient.confidence,
                )
            print(
                "Billing Address Recipient: {} has confidence: {}".format(
                    billing_address_recipient.value,
                    billing_address_recipient.confidence,
                )
            )
        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
            extracted[f'invoice{idx+1}']['shipping_address'] = "Shipping Address: {} has confidence: {}".format(
                    shipping_address.value, shipping_address.confidence
                )
            print(
                "Shipping Address: {} has confidence: {}".format(
                    shipping_address.value, shipping_address.confidence
                )
            )
        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
            extracted[f'invoice{idx+1}']['shipping_address_recipient'] = "Shipping Address Recipient: {} has confidence: {}".format(
                    shipping_address_recipient.value,
                    shipping_address_recipient.confidence,
                )
            print(
                "Shipping Address Recipient: {} has confidence: {}".format(
                    shipping_address_recipient.value,
                    shipping_address_recipient.confidence,
                )
            )
        print("Invoice items:")
        if invoice.fields.get("Items"):
            extracted[f'invoice{idx+1}']['items'] = {}
            for idx, item in enumerate(invoice.fields.get("Items").value):
                extracted[f'invoice{idx+1}']['items'][f'item{idx+1}'] = {}
                print("...Item #{}".format(idx + 1))
                item_description = item.value.get("Description")
                if item_description:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['description'] = "Description: {} has confidence: {}".format(
                            item_description.value, item_description.confidence
                        )
                    print(
                        "......Description: {} has confidence: {}".format(
                            item_description.value, item_description.confidence
                        )
                    )
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['quantity'] = "Quantity: {} has confidence: {}".format(
                            item_quantity.value, item_quantity.confidence
                        )
                    print(
                        "......Quantity: {} has confidence: {}".format(
                            item_quantity.value, item_quantity.confidence
                        )
                    )
                unit = item.value.get("Unit")
                if unit:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['unit'] = "Unit: {} has confidence: {}".format(
                            unit.value, unit.confidence
                        )
                    print(
                        "......Unit: {} has confidence: {}".format(
                            unit.value, unit.confidence
                        )
                    )
                unit_price = item.value.get("UnitPrice")
                if unit_price:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['unit_price'] = "Unit Price: {} has confidence: {}".format(
                            unit_price.value, unit_price.confidence
                        )
                    print(
                        "......Unit Price: {} has confidence: {}".format(
                            unit_price.value, unit_price.confidence
                        )
                    )
                product_code = item.value.get("ProductCode")
                if product_code:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['product_code'] = "Product Code: {} has confidence: {}".format(
                            product_code.value, product_code.confidence
                        )
                    print(
                        "......Product Code: {} has confidence: {}".format(
                            product_code.value, product_code.confidence
                        )
                    )
                item_date = item.value.get("Date")
                if item_date:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['item_date'] = "Date: {} has confidence: {}".format(
                            item_date.value, item_date.confidence
                        )
                    print(
                        "......Date: {} has confidence: {}".format(
                            item_date.value, item_date.confidence
                        )
                    )
                tax = item.value.get("Tax")
                if tax:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['tax'] = "Tax: {} has confidence: {}".format(tax.value, tax.confidence)
                    print(
                        "......Tax: {} has confidence: {}".format(tax.value, tax.confidence)
                    )
                amount = item.value.get("Amount")
                if amount:
                    extracted[f'invoice{idx+1}']['items'][f'item{idx+1}']['amount'] = "Amount: {} has confidence: {}".format(
                            amount.value, amount.confidence
                        )
                    print(
                        "......Amount: {} has confidence: {}".format(
                            amount.value, amount.confidence
                        )
                    )
        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            extracted[f'invoice{idx+1}']['subtotal'] = "Subtotal: {} has confidence: {}".format(
                    subtotal.value, subtotal.confidence
                )
            print(
                "Subtotal: {} has confidence: {}".format(
                    subtotal.value, subtotal.confidence
                )
            )
        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            extracted[f'invoice{idx+1}']['total_tax'] = "Total Tax: {} has confidence: {}".format(
                    total_tax.value, total_tax.confidence
                )
            print(
                "Total Tax: {} has confidence: {}".format(
                    total_tax.value, total_tax.confidence
                )
            )
        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            extracted[f'invoice{idx+1}']['previous_unpaid_balance'] = "Previous Unpaid Balance: {} has confidence: {}".format(
                    previous_unpaid_balance.value, previous_unpaid_balance.confidence
                )
            print(
                "Previous Unpaid Balance: {} has confidence: {}".format(
                    previous_unpaid_balance.value, previous_unpaid_balance.confidence
                )
            )
        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            extracted[f'invoice{idx+1}']['amount_due'] = "Amount Due: {} has confidence: {}".format(
                    amount_due.value, amount_due.confidence
                )
            print(
                "Amount Due: {} has confidence: {}".format(
                    amount_due.value, amount_due.confidence
                )
            )
        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            extracted[f'invoice{idx+1}']['service_start_date'] = "Service Start Date: {} has confidence: {}".format(
                    service_start_date.value, service_start_date.confidence
                )
            print(
                "Service Start Date: {} has confidence: {}".format(
                    service_start_date.value, service_start_date.confidence
                )
            )
        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            extracted[f'invoice{idx+1}']['service_end_date'] = "Service End Date: {} has confidence: {}".format(
                    service_end_date.value, service_end_date.confidence
                )
            print(
                "Service End Date: {} has confidence: {}".format(
                    service_end_date.value, service_end_date.confidence
                )
            )
        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            extracted[f'invoice{idx+1}']['service_address'] = "Service Address: {} has confidence: {}".format(
                    service_address.value, service_address.confidence
                )
            print(
                "Service Address: {} has confidence: {}".format(
                    service_address.value, service_address.confidence
                )
            )
        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            extracted[f'invoice{idx+1}']['service_address_recipient'] = "Service Address Recipient: {} has confidence: {}".format(
                    service_address_recipient.value,
                    service_address_recipient.confidence,
                )
            print(
                "Service Address Recipient: {} has confidence: {}".format(
                    service_address_recipient.value,
                    service_address_recipient.confidence,
                )
            )
        remittance_address = invoice.fields.get("RemittanceAddress")
        if remittance_address:
            extracted[f'invoice{idx+1}']['remittance_address'] = "Remittance Address: {} has confidence: {}".format(
                    remittance_address.value, remittance_address.confidence
                )
            print(
                "Remittance Address: {} has confidence: {}".format(
                    remittance_address.value, remittance_address.confidence
                )
            )
        remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
        if remittance_address_recipient:
            extracted[f'invoice{idx+1}']['remittance_address_recipient'] = "Remittance Address Recipient: {} has confidence: {}".format(
                    remittance_address_recipient.value,
                    remittance_address_recipient.confidence,
                )
            print(
                "Remittance Address Recipient: {} has confidence: {}".format(
                    remittance_address_recipient.value,
                    remittance_address_recipient.confidence,
                )
            )
    return extracted


extracted = analyze_invoice("invoices/invoice_sample.jpg")
for head,data in extracted.items():
    data_df = pd.DataFrame.from_dict(data)
    df = data_df.to_json()
    print(df)

    # create_table_sql = f"""
    # CREATE COLUMN TABLE "{'DBADMIN'}"."{'ocrdata'}" (
    #     {', '.join([f'"{col}" NVARCHAR(255)' for col in data_df.columns])}
    # )
    # """

    create_table_sql = "CREATE COLUMN TABLE ocrdata ("
    for column_name, dtype in data_df.dtypes.items():
        sql_data_type = "VARCHAR(255)"  # Default SQL data type (you can customize this)
        if dtype == 'int64':
            sql_data_type = "INTEGER"
        elif dtype == 'float64':
            sql_data_type = "DOUBLE"
        elif dtype == 'datetime64':
            sql_data_type = "TIMESTAMP"
        create_table_sql += f'"{column_name}" {sql_data_type}, '
    create_table_sql = create_table_sql.rstrip(', ') + ")"
    # cursor.execute(create_table_sql)
    print('table created')
    data_to_insert = [tuple(row) for row in data_df.values]
    schema_name = 'DBADMIN'
    table_name = 'OCRDATA'
    insert_sql = f"""
    INSERT INTO "{schema_name}"."{table_name}"
    VALUES ({', '.join(['?' for _ in data_df.columns])})
    """

    cursor.executemany(insert_sql, data_to_insert)

    sapconn.commit()
    print('data inserted')
    sapconn.close()


# connection.commit()

# cursor.close()
# conn.close()
    # print(data_df)
    # data_df = data_df.apply()
    # data_df.to_csv('data.csv')

# print(data_df.head(5))
# if __name__ == "__main__":
#     extracted = analyze_invoice("invoices/invoice_sample.jpg")



#     print("----------------------------------------")
#     print("----------------------------------------")
#     print("----------------------------------------")
#     print(extracted,'----')
#     print(type(extracted),'----')