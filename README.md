## Developing a server side call-billing application with Flask
### Created date: 2022-11-26
### Author: *Binh Lam*

# Environment Setup
* Global Dependencies
1. Run the server-side with Virtualenv:

    ```sh
    cd call-billing
    python3 -m venv callbillingenv
    source callbillingenv/bin/activate
    pip install -r requirements.txt
    ```
    * API RUN:
    ```sh
        cd ~/virtualenvs/callbillingenv/bin
        gunicorn --timeout 3000 --bind 127.0.0.1:8000 main:run()
    ```

2. Run the server-side with Docker:
   ```sh
    cd call-billing
    docker build . -t call-billing:latest
    ```
    * API RUN:
    ```
        docker run -p 8000:8001 call-billing
    ```
   ![img.png](img.png)   

3. Run unittest (local) - after starting app:
   ```sh
      python3 test/call_billing.py
   ```
   ![img_1.png](img_1.png)

4. Sample curl:
   ```sh
   curl --location --request PUT 'http://localhost:8000/mobile/tester/call' \
        --header 'Content-Type: application/json' \
        --data-raw '{
          "call_duration": 6000
        }'
   ```
   ![img_2.png](img_2.png)

   ```sh
   curl --location --request GET 'http://localhost:8000/mobile/tester/billing'
   ```
   ![img_3.png](img_3.png)

   