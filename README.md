# flask_tryout

# Set up

## Enable setup tls cert
`kubectl create secret tls rinopower.com --cert=secrets/tls/certificate.crt --key=secrets/tls/private.key`

# Run
`docker-compose up`


# User

## Create `http post :8000/user username='rino' password='1234'`
- ## Get  `http :8000/user username==rino`
- ## Login 
