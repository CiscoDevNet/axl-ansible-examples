# Sample Vault/oauthapp Setup Commands

1. Start Vault in dev mode, load plugins from local directory:

   ```
   vault server -dev -dev-plugin-dir=./vault/plugins
   ```    
1. Export the Vault server location

   ```
   export VAULT_ADDR=http://localhost:8200
   ```

1. Export the Vault admin token (careful!) to the environment - this allows it to be picked automatically by Ansible/hvac:

   ```
   export VAULT_TOKEN=hvs.TXpC...YmxbaTMWU7O
   ```

1. Login to Vault so we can setup the oauthapp configuration

   ```
   vault login
   ```

1. Enable the oauthapp plugin

   ```
   vault secrets enable oauthapp
   ```

1. Configure the Webex OAuth2 provider and integration details:

   ```
   vault write oauthapp/servers/webex-adminapp \
   provider=custom client_id=C6de0ebc0ad61...29a5369e22f37a631 \
   client_secret=81f640a666b333cf9...3302bee83746c11954197 \
   provider_options=auth_code_url="https://webexapis.com/v1/authorize" \
   provider_options=token_url="https://webexapis.com/v1/access_token"
   ```

1. Generate an OAuth2 launch URL and print it to the console:

   ```
   vault write oauthapp/auth-code-url \
   server=webex-adminapp \
   redirect_url="https://localhost/callback" scopes="spark-admin:licenses_read" \
   state=12345
   ```

1. (Copy to the URL, paste into an incognito browser, complete the login, and copy the resulting `code` URL parameter value from the browser URL bar.)

1. Create a credential entry in the Webex provider, based on the returned authorization code:

   ```
   vault write oauthapp/creds/testauth \
   server=webex-adminapp \
   code=MDIxOWU3NTItYzc3OC00ODNkL...58e99f-9f97-4dbd-aeb5-65d102b37d42 \
   redirect_url="https://localhost/callback"
   ```

   Internally Vault/oauthapp will use the code to retrieve the user's `access_token`/`refresh_token` and keep them up to date.

1. Retrieve an up-to-date `access_token`:

   ```
   vault read oauthapp/creds/testauth
   ```