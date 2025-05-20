## Installation & Launch
1. Clone project
   ```
   git clone https://github.com/LivioSmd/epic_events.git
   cd epic_events
   ```
2. Create virtual environment
   ```
   python3 -m venv venv
   source venv/bin/activate  
   ```
3. install requirements
   ```
   pip install -r requirements.txt
   ```
4. Add a ```.env``` file at the root of the project that will contain :
   ```
   SECRET_KEY=your_secret_key #auth key
   DSN="your_sentry_dsn" #Sentry Dsn
   ```

## Commands :
### Login / Logout / Me
1. Login
    ```
    python -m frontend_click.cli login <email> <password>
    ```
2. Logout
    ```
    python -m frontend_click.cli logout
    ```
3. Me (display current User)
    ```
    python -m frontend_click.cli me
    ```

### Users 
1. Display users
    ```
    python -m frontend_click.cli list-users
    ```
2. Display a user
    ``` 
    python -m frontend_click.cli get-user <user_id>
    ```
3. Create a user
    ``` 
    python -m frontend_click.cli create-user <name> <email> <type> <password>
    ```
4. Update a user (-- for optional)
    ``` 
    python -m frontend_click.cli update-user <id> --name <name> --email <email>
    ```
5. Delete a user
    ``` 
    python -m frontend_click.cli delete-user <id>
    ```

### Clients 
1. Display clients
    ```
    python -m frontend_click.cli list-clients
    ```
2. Display a client
    ``` 
    python -m frontend_click.cli get-client <client_id>
    ```
3. Create a client
    ``` 
    python -m frontend_click.cli create-client <name> <email> <phone_number> <company_name> <information>
    ```
4. Update a client (-- for optional)
    ``` 
    python -m frontend_click.cli update-client <id> --name <name> --email <email> --phone_number <phone_number> --company_name <company_name> --information <information>
    ```
5. Delete a client
    ``` 
    python -m frontend_click.cli delete-client <id>
    ```
   
### Contrats 
1. Display contrats
    ```
    python -m frontend_click.cli list-contrats
    ```
    filter contrats signed
    ```
    python -m frontend_click.cli list-contrats --signed
    ```
    filter contrats not signed
    ```
    python -m frontend_click.cli list-contrats --not_signed
    ```
    filter contrats paid
    ```
    python -m frontend_click.cli list-contrats --paid
    ```
    filter contrats not paid
    ```
    python -m frontend_click.cli list-contrats --no_paid
    ```
2. Display a contrat
    ``` 
    python -m frontend_click.cli create-contrat <client_id> <total_amount> <outstanding_amount> <signed>
    ```
3. Create a contrat
    ``` 
    python -m frontend_click.cli create-contrat <client_id> <total_amount> <outstanding_amount> <signed>
    ``` 
4. Update a contrat (-- for optional)
    ``` 
    python -m frontend_click.cli update-contrat <id> --client_id <client_id> --total_amount <total_amount> --outstanding_amount <outstanding_amount> --signed <signed>
    ```
5. Delete a contrat
    ``` 
    python -m frontend_click.cli delete-contrat <id>
    ```  
    
### Evenements 
1. Display evenements
    ```
    python -m frontend_click.cli list-evenements
    ```
   filter evenements with no support
    ```
    python -m frontend_click.cli list-evenements --no_support
    ```
   filter evenements with support
    ```
    python -m frontend_click.cli list-evenements --support
    ```
   display evenements of the current user (support users only !)
    ```
    python -m frontend_click.cli list-evenements --my_evenements
    ```
2. Display an evenement
    ``` 
    python -m frontend_click.cli create-evenement <id>
    ```
3. Create an evenement
    ``` 
    python -m frontend_click.cli create-evenement <contrat_id> <client_name> <client_contact_id> --support_id <> <start_date> <end_date> <location> <expected> <notes> 
    ``` 
4. Update an evenement (-- for optional)
    ``` 
    python -m frontend_click.cli update-evenement <id> --client_name <> --client_contact_id <> --support_id <> --start_date <> --end_date <> --location <> --expected <> --notes <>
    ```
5. Delete an evenement
    ``` 
    python -m frontend_click.cli delete-evenement <id>
    ```
   
## Tests
1. Launch a test
   ```
   pytest -k «test_name»
   ```
   or
   ```
   PYTHONPATH=. pytest -k «test_name»
   ```
2. Launch tests
   ```
   pytest
   ```
   or
   ```
   PYTHONPATH=. pytest
   ```
3. Launch tests with coverage
   ```
   pytest --cov=.
   ```
   or
   ```
   PYTHONPATH=. pytest --cov=.
   ```