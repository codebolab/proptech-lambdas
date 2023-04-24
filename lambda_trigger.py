import os
import boto3

PROPERTY_TYPES = {
    "CASA": "https://clasificados.lostiempos.com/inmuebles/tipo/casa-chalet-2014/",
    "DEPTO": "https://clasificados.lostiempos.com/inmuebles/tipo/departamento-2015/",
    "TERRENO": "https://clasificados.lostiempos.com/inmuebles/tipo/lote-terreno-2017/",
    "OFICINA": "https://clasificados.lostiempos.com/inmuebles/tipo/oficina-2018/",
    "LOCAL": "https://clasificados.lostiempos.com/inmuebles/tipo/local-comercial-2019/"
}
LISTING_TYPES = {
    "SELL": "transaccion/venta-2023",
    "RENT": "transaccion/alquiler-2024",
    "ANTICRETIC": "transaccion/anticretico-2025",
}
lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    logging.info("> lambda_handler")

    sent_urls = []
    for property_type, url in PROPERTY_TYPES.items()
        for listing_type, param in LISTING_TYPES.items():
            full_url = os.path.join(url, param)

            payload = {
                "url": full_url
            }
            lambda_client.invoke(
                FunctionName='scrapper',
                InvocationType='Event',  # Esto hace que la invocación sea asincrónica
                Payload=json.dumps(payload)
            )
            sent_urls.append(full_url)
