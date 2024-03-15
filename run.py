from fivesim import FiveSim
import time

# These example values won't work. You must get your own api_key
API_KEY = "yourkey"

client = FiveSim(API_KEY)  # Optional proxy

# Balance request
balance_info = client.get_balance()  # Provides profile data: email, balance and rating.
balance = balance_info["balance"]
print("Your Balance : " + balance + " RUB")


# # Prices by country and product
# regPrice = client.price_requests_by_country_and_product(
#     country="russia", product="google"
# )  # Returns product prices by country and specific product
# print(regPrice)


# Buy activation number
buyNumber = client.buy_number(
    country="russia", operator="virtual52", product="google"
)  # Buy new activation number
# Extract id, phone and product
id = buyNumber["id"]
phone = buyNumber["phone"]
product = buyNumber["product"]

print("Product : " + product)
print("Order Number : " + str(id))
print("Number : " + phone)
print("Status : Waiting for OTP")


start_time = time.time()  # Get the current time

# Check order (Get SMS)
while True:
    getSms = client.check_order(order_id=id)  # Check the sms was received
    sms = getSms["sms"]
    if sms:  # If sms is not null or empty, break the loop
        break
    elif time.time() - start_time > 60:  # If 60 seconds have passed
        print("OTP not received yet. Do you want to reset the time? (y/n)")
        user_input = input("choose an option(y/n) : ")
        if user_input.lower() == "y":
            start_time = time.time()  # Reset the time
        elif user_input.lower() == "n":
            print("Cancelling order...")
            client.cancel_order(order_id=id)
            exit()
    time.sleep(5)  # Wait for 5 seconds before checking again

print("otp: " + sms[0]["code"])
