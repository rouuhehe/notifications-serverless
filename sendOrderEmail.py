import boto3
import json
import os

ses = boto3.client("ses")

def lambda_handler(event, context):
    print("EVENT:", event)

    for record in event["Records"]:
        msg = json.loads(record["body"])
        detail = json.loads(msg["Message"])

        user_email = detail["user_email"]
        status = detail["status"]
        order_id = detail["order_id"]

        ses.send_email(
            Source=os.environ["SOURCE_EMAIL"],
            Destination={"ToAddresses": [user_email]},
            Message={
                "Subject": {"Data": f"Actualización de tu pedido ({order_id})"},
                "Body": {
                    "Text": {
                        "Data": (
                            f"Estado actualizado: {status}\n"
                            f"Pedido: {order_id}\n"
                        )
                    }
                }
            }
        )

    return {"status": "ok"}
