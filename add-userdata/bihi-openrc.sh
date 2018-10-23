#!/usr/bin/env bash

export OS_AUTH_URL=https://uppmax.cloud.snic.se:5000/v3

export OS_PROJECT_ID=2344cddf33a1412b846290a9fb90b762
export OS_PROJECT_NAME="SNIC 2018/10-30"
export OS_USER_DOMAIN_NAME="snic"
export OS_PROJECT_DOMAIN_NAME="snic"
if [ -z "$OS_USER_DOMAIN_NAME" ]; then unset OS_USER_DOMAIN_NAME; fi

unset OS_TENANT_ID
unset OS_TENANT_NAME

export OS_USERNAME="s11856"

export OS_PASSWORD="acc3project"

export OS_REGION_NAME="UPPMAX"
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi

export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
