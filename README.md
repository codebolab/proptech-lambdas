# Lambda Functions para Capturar Datos de Propiedades en Venta

Este repositorio contiene funciones lambda diseñadas para capturar datos relacionados a propiedades en venta de diversas fuentes.

## Fuentes soportadas

Actualmente, se obtienen datos de las siguientes fuentes:

- lostiempos.com

## Configuración del entorno

Para configurar el entorno, instale las dependencias necesarias ejecutando los siguientes comandos:

```bash
pip install ansible
pip install boto3 botocore
ansible-galaxy collection install amazon.aws
```

## Ejecución del playbook

Una vez que haya configurado el entorno, ejecute el playbook utilizando el siguiente comando:

```bash
ansible-playbook lambda_playbook.yml
```
