"""
================================================================================
 Assignment 03 — Refactor the Messy Store System
 192-201 Advanced Computer Programming with Generative AI
 Week 5 — OOP Design & Refactoring   |   Faculty of IT (International), Siam University
 Lecturer: Hrang Kap Lian
================================================================================

 Maps to: CLO1 (object-oriented design) and CLO5 (responsible, verified AI use)
 Weight:  10 Points     AI-use level: Level 2 (AI-assisted + PROMPT LOG required)

--------------------------------------------------------------------------------
 THE TASK
--------------------------------------------------------------------------------
 You are given ONE working program that is badly written. Do NOT add features and
 do NOT change what it does. REFACTOR it: reshape the code into a clean,
 object-oriented design while producing the EXACT SAME output.

   The one rule of refactoring:  same behaviour, cleaner code.
   If the output changes, it is no longer a refactor — it is a bug.

 How to run:
   python Assignment_03.py
 It prints PASS when your refactor reproduces the original output exactly,
 or FAIL with the first line that differs.

--------------------------------------------------------------------------------
 WHAT YOU WILL PRACTISE (use ALL of these)
--------------------------------------------------------------------------------
   Week 2  Model data as CLASSES with attributes and methods (not tuples/lists).
   Week 3  ENCAPSULATION — validate object state in the constructor.
   Week 4  INHERITANCE & POLYMORPHISM — replace the `if tier == ...` chains
           with a family of classes.
   Week 5  COMPOSITION (has-a) — an Order has-a customer and has-many items;
           an item has-a product.
   Week 5  PURE FUNCTIONS vs MODIFIERS — calculation methods RETURN values and
           print nothing; keep them separate from the receipt printing.
   Week 5  INTERFACE vs IMPLEMENTATION — separate WHAT the receipt shows from
           HOW the totals are computed.

--------------------------------------------------------------------------------
 RULES
--------------------------------------------------------------------------------
 1. Behaviour must stay identical — the self-test must print PASS.
 2. Refactor only. No new discounts, no prettier receipts, no extra products.
 3. You choose the class design — there is no single correct answer.
 4. Level-2 AI use: you may use AI to explain/suggest/refactor, but YOU verify
    every change and you keep a PROMPT LOG (in CHANGES.md).
 5. Work in small steps: change one thing -> run -> keep it green.

--------------------------------------------------------------------------------
 THE SCENARIO
--------------------------------------------------------------------------------
 A small online store prints a receipt per order and a grand total. Business rules:
   - Tax: electronics & stationery = 7%; food = tax-free.
   - Membership discount on the subtotal:
         tier      subtotal<=100   subtotal>100
         none        0%              0%
         silver      2%              5%
         gold        5%              10%
         platinum    10%             15%
   - Bulk discount: 10+ items in total -> add another 3% of the subtotal.
   - total = subtotal - discount + tax
   - points = int(total // 10) * tier_multiplier   (none x1, silver x2, gold x3, platinum x5)
 You do not change these rules — you express them cleanly.

--------------------------------------------------------------------------------
 YOUR TASKS  (see the rubric at the bottom)
--------------------------------------------------------------------------------
   A. (required) Model the domain with classes + composition
                 e.g. Product, OrderItem (has-a Product), Customer, Order.
   B. (required) Encapsulate & validate state in constructors (e.g. qty >= 1).
   C. (required) Replace the tier `if/elif` chains (discount AND points) with
                 polymorphism — a class family, no `if tier == ...`.
   D. (required) Separate calculation from printing: pure methods return numbers.
   E. (required) Kill magic numbers (name them) and remove the leftover `global`.
   F. (stretch)  Let each product decide its own tax — no `if category` in totals.
   G. (stretch)  Add a sensible __str__ where it helps.

--------------------------------------------------------------------------------
 SUBMIT
--------------------------------------------------------------------------------
   1) This file, Assignment_03.py, with your refactor (self-test prints PASS).
   2) CHANGES.md — your written explanation of each change + your prompt log.
================================================================================
"""

import io
import contextlib


# ==============================================================================
#  LEGACY STORE SYSTEM  —  messy but working.   DO NOT EDIT THIS SECTION.
#  Read it, understand it, and use its output as the correct behaviour.
# ==============================================================================
PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]
TAXRATE = 0.07
foodtax = 0.0
ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE
    n = o[0]; t = o[1]; items = o[2]
    sub = 0.0; tax = 0.0
    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)
    for it in items:
        pi = it[0]; q = it[1]
        p = PRODUCTS[pi][1]; nm = PRODUCTS[pi][0]; cat = PRODUCTS[pi][2]
        line = p * q
        sub = sub + line
        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE
        print(nm + " x" + str(q) + " = " + str(line))
    d = 0.0
    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100: d = sub * 0.05
        else: d = sub * 0.02
    elif t == "gold":
        if sub > 100: d = sub * 0.10
        else: d = sub * 0.05
    elif t == "platinum":
        if sub > 100: d = sub * 0.15
        else: d = sub * 0.10
    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]
    if totalqty >= 10:
        d = d + sub * 0.03
    total = sub - d + tax
    pts = 0
    if t == "none": pts = int(total // 10)
    elif t == "silver": pts = int(total // 10) * 2
    elif t == "gold": pts = int(total // 10) * 3
    elif t == "platinum": pts = int(total // 10) * 5
    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for o in ORDERS:
        grand = grand + calc(o)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
#  BEHAVIOUR LOCK  —  DO NOT EDIT.
#  Captures the exact output of the legacy program as the target you must match.
# ==============================================================================
def capture(fn):
    """Run fn() and return everything it printed, as a string."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


# ==============================================================================
#  YOUR REFACTORED SOLUTION  —  WRITE YOUR CODE BELOW.
#  Design your own classes. A suggested skeleton is commented out — change freely.
#  Your program must define refactored_main() which PRINTS the same output.
# ==============================================================================

# --- named constants (replace the magic numbers) ---
STANDARD_TAX_RATE  = 0.07   # electronics & stationery
FOOD_TAX_RATE      = 0.0    # food is tax-free
DISCOUNT_THRESHOLD = 100    # tier discount is bigger when subtotal is ABOVE this
BULK_QTY_THRESHOLD = 10     # 10 or more items in total -> bulk discount
BULK_DISCOUNT_RATE = 0.03
POINTS_DIVISOR     = 10     # 1 point (x tier multiplier) per 10 spent
MONEY_DECIMALS     = 2
RULE_WIDTH         = 40     # width of the "-----" line on the receipt


# --- products: each product decides its own tax ---
class Product:
    """A product for sale. Standard products are taxed at STANDARD_TAX_RATE."""

    tax_rate = STANDARD_TAX_RATE

    def __init__(self, name, price):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Product price must be a number >= 0")
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    def tax_on(self, amount):
        return amount * self.tax_rate

    def __str__(self):
        return self._name + " @ " + str(self._price)


class FoodProduct(Product):
    """Food is tax-free."""

    tax_rate = FOOD_TAX_RATE


# --- an order line: has-a Product ---
class OrderItem:
    def __init__(self, product, quantity):
        if not isinstance(product, Product):
            raise TypeError("OrderItem needs a Product")
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError("Quantity must be a whole number >= 1")
        self._product = product
        self._quantity = quantity

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    def line_total(self):
        return self._product.price * self._quantity

    def tax(self):
        return self._product.tax_on(self.line_total())

    def __str__(self):
        return self._product.name + " x" + str(self._quantity) + " = " + str(self.line_total())


# --- customers: one class per membership tier (no `if tier == ...`) ---
class Customer:
    """Base tier ("none"): no discount, x1 points."""

    tier_name = "none"
    small_order_rate = 0.0    # subtotal <= DISCOUNT_THRESHOLD
    large_order_rate = 0.0    # subtotal >  DISCOUNT_THRESHOLD
    points_multiplier = 1

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Customer name must be a non-empty string")
        self._name = name

    @property
    def name(self):
        return self._name

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_THRESHOLD:
            return self.large_order_rate
        return self.small_order_rate

    def tier_discount(self, subtotal):
        return subtotal * self.discount_rate(subtotal)

    def points_for(self, total):
        return int(total // POINTS_DIVISOR) * self.points_multiplier

    def __str__(self):
        return self._name + " (" + self.tier_name + ")"


class SilverCustomer(Customer):
    tier_name = "silver"
    small_order_rate = 0.02
    large_order_rate = 0.05
    points_multiplier = 2


class GoldCustomer(Customer):
    tier_name = "gold"
    small_order_rate = 0.05
    large_order_rate = 0.10
    points_multiplier = 3


class PlatinumCustomer(Customer):
    tier_name = "platinum"
    small_order_rate = 0.10
    large_order_rate = 0.15
    points_multiplier = 5


# --- an order: has-a Customer, has-many OrderItem.  Pure calculations only. ---
class Order:
    def __init__(self, customer, items):
        if not isinstance(customer, Customer):
            raise TypeError("Order needs a Customer")
        items = list(items)
        if not items or not all(isinstance(it, OrderItem) for it in items):
            raise ValueError("Order needs at least one OrderItem")
        self._customer = customer
        self._items = items

    @property
    def customer(self):
        return self._customer

    @property
    def items(self):
        return list(self._items)

    def subtotal(self):
        return sum(item.line_total() for item in self._items)

    def total_quantity(self):
        return sum(item.quantity for item in self._items)

    def bulk_discount(self):
        if self.total_quantity() >= BULK_QTY_THRESHOLD:
            return self.subtotal() * BULK_DISCOUNT_RATE
        return 0.0

    def discount(self):
        return self._customer.tier_discount(self.subtotal()) + self.bulk_discount()

    def tax(self):
        return sum(item.tax() for item in self._items)

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        return self._customer.points_for(self.total())


# --- presentation: WHAT the receipt shows (no calculation rules in here) ---
def money(amount):
    return str(round(amount, MONEY_DECIMALS))


def format_receipt(order):
    rule = "-" * RULE_WIDTH
    lines = ["Receipt for " + str(order.customer), rule]
    lines += [str(item) for item in order.items]
    lines += [
        rule,
        "Subtotal: " + money(order.subtotal()),
        "Discount: " + money(order.discount()),
        "Tax: " + money(order.tax()),
        "Total: " + money(order.total()),
        "Points earned: " + str(order.points()),
        "",
    ]
    return "\n".join(lines)


# --- the store's data, as objects ---
def build_orders():
    laptop       = Product("Laptop", 1200.0)
    headphones   = Product("Headphones", 200.0)
    coffee_beans = FoodProduct("Coffee Beans", 15.0)
    notebook     = Product("Notebook", 5.0)
    water_bottle = FoodProduct("Water Bottle", 10.0)
    monitor      = Product("Monitor", 300.0)
    pen          = Product("Pen", 2.0)

    return [
        Order(GoldCustomer("Alice"),
              [OrderItem(laptop, 1), OrderItem(headphones, 2), OrderItem(coffee_beans, 3)]),
        Order(Customer("Bob"),
              [OrderItem(notebook, 10), OrderItem(pen, 5)]),
        Order(PlatinumCustomer("Charlie"),
              [OrderItem(monitor, 2), OrderItem(water_bottle, 6), OrderItem(coffee_beans, 2)]),
        Order(SilverCustomer("Dana"),
              [OrderItem(headphones, 1), OrderItem(notebook, 3), OrderItem(pen, 10)]),
    ]


def refactored_main():
    """Print every receipt and the grand total — same output as legacy_main()."""
    orders = build_orders()
    for order in orders:
        print(format_receipt(order))
    grand_total = sum(order.total() for order in orders)
    print("GRAND TOTAL (all orders): " + money(grand_total))


# ==============================================================================
#  SELF-TEST  —  DO NOT EDIT.   Run:  python Assignment_03.py
# ==============================================================================
def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()
        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"
            if gl != yl:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(gl))
                print("  yours:    " + repr(yl))
                break


if __name__ == "__main__":
    _check()


# ==============================================================================
#  RUBRIC (10 pts)
#   Behaviour preserved (self-test PASS) .................. 2
#   Domain modelling & composition ....................... 2
#   Polymorphism (tier discount & points, no if/elif) .... 1.5
#   Pure calculation vs I/O separation ................... 1.5
#   Encapsulation & validation ........................... 1
#   Clean code (names, no magic numbers, DRY, no global).. 1
#   CHANGES.md explanation (per-change, before->after) ...  0.5
#   CHANGES.md prompt log (Level-2) ......................  0.5
#  NOTE: passing the test alone is only 20/100 — most marks are for the DESIGN
#        and for explaining and verifying your changes. 
# ==============================================================================
