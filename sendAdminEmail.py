import boto3
import json
import os

ses = boto3.client("ses")

def lambda_handler(event, context):

    admin_emails = os.environ["ADMIN_EMAILS"].split(",")

    for record in event["Records"]:
        msg = json.loads(record["body"])
        detail = json.loads(msg["Message"])

        status = detail["status"]
        order_id = detail["order_id"]
        tenant_id = detail["tenant_id"]
        error = detail.get("error")

        text = f"""
Evento administrativo
---------------------
Pedido: {order_id}
Tenant: {tenant_id}
Estado: {status}
"""

        if error:
            text += f"Error: {error}\n"

        ses.send_email(
            Source=os.environ["SOURCE_EMAIL"],
            Destination={"ToAddresses": admin_emails},
            Message={
                "Subject": {"Data": f"[ADMIN] Evento: {status}"},
                "Body": {"Text": {"Data": text}}
            }
        )
