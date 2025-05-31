print("What year were you born in?")
year = int(input("Enter your birth year: "))
age = 2025 - year
if age <= 12:
    ticketprice = 5
    print("You are", age, "years old.")
    print("You will be charged ", ticketprice)
elif age >= 13 and age <= 59:
    ticketprice = 10
    if age >= 18:
        tax = 0.18 * ticketprice
        ticketprice = ticketprice + tax
    print("You are", age, "years old.")
    print("You will be charged ", ticketprice, "including tax of", tax if age >= 18 else "0")
elif age > 60:
    ticketprice = 7
    tax = 0.18 * ticketprice
    ticketprice = ticketprice + tax
    print("You are", age, "years old.")
    print("You will be charged ", ticketprice, "including tax of", tax)