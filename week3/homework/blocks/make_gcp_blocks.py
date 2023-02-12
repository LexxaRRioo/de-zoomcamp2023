from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

# alternative to creating GCP blocks in the UI
# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!


credentials_block = GcpCredentials(
    service_account_info={
  "type": "service_account",
  "project_id": "de-zoomcamp-2023-375411",
  "private_key_id": "380c4b80eee9fd4d4e1c474afe7de1cfbac5f479",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCYswXKhywuXX1R\nyT6in+fi70eGYPLJBV4R3+qm5Prcjne8vOlfRGhBHGu/MbaQ+i2txkDmtTDp3Sw/\nB6eDugbKL7ZWCk80prFZKu2Slx1pApyjVq25g6WziSiUnqq9hn/RYMV/7W2vxGd/\n1Wn40zW1t4i/DlaGMSOXzfsg9iUgGLX+SFVnw3ltc8l3dYec1CwFqoCpn18wxfw5\nq7lnKEx9Mo76/tUz1IuBosqM0+b5z/xRX4EB3HMj/op9opidMJIVe61B/KTz+B9M\n8TQxBFnKG9ZkFTiZJEcLCOKpKaE8+xcFofcvQn7RfimoXBr8aaXnxtwPv91V3EIC\nAVwHCZ/RAgMBAAECggEAAk1QnQkEpX5LUVxTUWhPuqAY1/HGNzmZfXN+uh1hmsmb\nDIFck08Ys0KWbT92nSDoZ2JBwDijECOBc0HOSLIZQBsQCKQHJagNrGZ1Rmx4yQh9\nDAlWfSF68gXzUqpBsLHCY4mt8IvHx4qSdN7mxhWJDcBCk37H1yYOf09fpdOQI7e1\nqv5mLGQvxA3z38Kiami0YQCYO4GnAjskqp0caVO2vX7p00HNLO9wf24dnENNw6bY\n5s5sTfPWDG+lRPp8k1apP6BfsDI34oXIxrcyTNPkbXCkCODuXWGBdr+mDaA7EY2Y\nel8dUguWPA46FKjdEnUr8c9QFKlHKNSn4WKrvUpSsQKBgQDXV0Az8hHyg3TR98KK\nlqcslvV15KGPMACl9wXxXs4SKONZur/qWZ379YICX5jLTy98iC8RAedPoJJZIq3X\nJE3iQcIxym9Ou9NaqVgyYPo/Pm3B+K/CD4PGDW1PMrUF8juFQF9uJK1sTNskqtil\nTVA6SsN05QwNdYlRkkO0Rr708wKBgQC1h+vYL6QDOVs6bGSxGAXtXuiLQvLL4zFp\nf1Y6cgleSo2R98q5bkOpwE8m6aAnVoRfOlX6yP1uEPm+Jik2HeB2OvKp9YDg6PEg\nwJ//u8dyTC43Q8LwPPbT1vilydCraatZz7rXgpLtTIyzZnecNUE4Di1oNcBLs84X\nSs3yYnpZKwKBgFzKbA/2L2Wg36XabSnq4P6Fzh+O9U8OEDlzyEvJ3mJU3CK+JhSF\nqV343JzJNL3m0T+ILz/U4ieduXJPTzl1m1nznAp4gJ4csWZPsoGC6FJ4RDNhRdsJ\ndG7TOlb2MqrtRliU9Ioxo8kXFRcnx1Lzja6QqMimKhtimllb/XChS4ehAoGAOuhP\npUjYbV9odk4EYt+L1NqOldp01ar1NunmfnLRDXMd+7cwZvocJPLN/K+lk/5kWE6i\n5g3hB52knYreprwNQfChHHwZhWKyFNHNWfyCnVmRScfIc5Mk+dtxtsMF3wocW7mo\nRRUPPsgvhGwE9oDlmB4pp/6BV0+S2kYhDL3ePB8CgYBds+uaMoE88+BNDwuedfw5\nh5RlB2hclsqdozfGILKT6QNckPmLfr2yfkbjU/RxLSSRo2VebDOB7oeAoeaKSv8g\n/VIdg4BlG6OFihS7UtUfVaCSQ/kW6LuatzY51JWMSY8zDzpz67CNlQVsd/5QlJm8\n12ed7mtXjtfgUw76CqDi1w==\n-----END PRIVATE KEY-----\n",
  "client_email": "dez-sa@de-zoomcamp-2023-375411.iam.gserviceaccount.com",
  "client_id": "116753441877421780679",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dez-sa%40de-zoomcamp-2023-375411.iam.gserviceaccount.com"
}
  # enter your credentials from the json file
)
credentials_block.save("zoom-gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("zoom-gcp-creds"),
    bucket="prefect-de-zoomcamp",  # insert your  GCS bucket name
)

bucket_block.save("zoom-gcs", overwrite=True)
