class Category:
  def __init__(self, name):
    self.name= name
    self.total = 0.00
    self. ledger =[]

  def __str__(self):
    s=''
    s+=self.name.center(30,'*')+'\n'
    tt = 0
    for each  in self.ledger:
      x1 ="%.2f" % each['amount']
      s+=f"{each['description'][:23]}{x1:>{30-len(each['description'][:23])}}\n"
      tt+=each['amount']
    x2 ="%.2f" % tt
    s+=f"Total: {x2}"
    return s
  def deposit (self, amount, description=""):
    self.total += amount
    self. ledger.append({"amount": amount,"description": description})

  def withdraw(self, amount, description=""):
    
    can_withdraw = self.check_funds (amount)
    if can_withdraw:
      self.total -= amount
      self. ledger.append ({"amount": -amount,"description": description})
    return can_withdraw

  def get_balance(self):
    return self.total

  def transfer(self, amount, instance):
    can_transfer= self.check_funds(amount)
    if can_transfer:
      self.withdraw(amount, f"Transfer to {instance.name}")
      instance.deposit(amount, f"Transfer from {self.name}")
    return can_transfer

  def check_funds(self, amount):
    if amount > self.total:
      return False
    return True


def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")