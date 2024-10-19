from datetime import datetime

today = datetime.now()
date = today.strftime("%a, %Y-%m-%d %H:%M:%S")
print(date)

first_name = "Joseph"
last_name = "Choi"

# fstring
full_name = f"{first_name} {last_name}"
print(full_name)
