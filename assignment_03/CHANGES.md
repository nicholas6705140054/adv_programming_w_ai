# Assignment 03 — CHANGES

**Name:** Min Htet Aung  **Student ID:** 6705140054

This is the written part of your submission. Explain **what you changed and why**, then record your **prompt log**. Keep before/after snippets to a line or two.

---

## 1 · What I changed

One row per change. Name the OOP concept and say how you checked the behaviour was unchanged.

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Products were bare tuples `("Laptop", 1200.0, "electronics")`; orders pointed at them by list index `(0, 1)` | `Product` / `FoodProduct` classes; `OrderItem(product, quantity)` holds the actual `Product`; `Order(customer, items)` | Classes / composition (has-a, has-many) | Ran `python Assignment_03.py` → PASS |
| 2 | Two `if t == "silver" / "gold" / ...` chains, one for discount, one for points | `Customer` base + `SilverCustomer` / `GoldCustomer` / `PlatinumCustomer`, each setting `small_order_rate`, `large_order_rate`, `points_multiplier`; shared `discount_rate()` and `points_for()` | Inheritance & polymorphism | PASS (all four tiers appear in the test orders) |
| 3 | `calc()` did the maths **and** printed the receipt in one function | `Order.subtotal()`, `discount()`, `tax()`, `total()`, `points()` only return numbers; `format_receipt(order)` builds the text; `refactored_main()` prints | Pure functions vs modifiers; interface vs implementation | PASS |
| 4 | No checks at all: a quantity of 0 or a negative price would be accepted silently | Constructors raise `ValueError`/`TypeError` (qty ≥ 1, price ≥ 0, non-empty names, order needs items); values exposed through read-only properties | Encapsulation & validation | PASS, plus tried `OrderItem(pen, 0)`, `Product("Pen", -1)`, `Customer("")`, `Order(bob, [])` → all rejected |
| 5 | Magic numbers (`0.07`, `0.03`, `100`, `10`, `40`), `global TAXRATE`, and `if cat == "food"` inside the totals | Named constants (`STANDARD_TAX_RATE`, `BULK_DISCOUNT_RATE`, `DISCOUNT_THRESHOLD`, ...); no `global`; each product knows its own `tax_rate` (`FoodProduct` = 0%) | Clean code; polymorphism for tax (stretch F) | PASS |
| 6 | Receipt lines were glued together with `+` inside the calculation loop | `__str__` on `Customer` (`Alice (gold)`), `OrderItem` (`Laptop x1 = 1200.0`) and `Product` | `__str__` (stretch G) | PASS |

## 2 · Short reflection (4–6 sentences)

Which change improved the code the most, and why? Where did keeping the behaviour identical force you to be careful?

> The biggest improvement was replacing the two `if tier == ...` chains with a `Customer` class family (`SilverCustomer`, `GoldCustomer`, `PlatinumCustomer`), where each tier holds its own discount rates and points multiplier. In the original, the rules for one tier were split across two separate chains (one for discount, one for points), so changing or adding a tier meant editing both and hoping they stayed in sync; now everything about a tier lives in one class, and `Order` just asks its customer for the discount and points without knowing which tier it is. Keeping the output identical forced me to be careful with number formatting: the receipt prints with `str()`, so line totals must stay floats (`1200.0`, not `1200` or `1200.00`), and rounding can only happen at print time, because the grand total adds up the *unrounded* order totals and rounding each order early could change the last digit. I also had to keep the two boundaries exactly as written: the tier discount switches when the subtotal is strictly greater than 100, while the bulk discount starts at 10 *or more* items, and Charlie's order has exactly 10 items, so an off-by-one mistake would show up straight away. Finally, I kept the bulk 3% calculated on the original subtotal (not the already-discounted amount) and kept tax added line by line, because those are the legacy rules and the self-test compares the output character for character.

---

## 3 · Prompt log (Level 2 — required)

Record **every** prompt where AI helped. If you wrote a part yourself, say so in one row. AI-shaped code with an empty log does **not** meet the Level-2 policy.

| # | My prompt to the AI | What it suggested (summary) | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | "Finish the refactor in Assignment_03.py so the self-test passes." | Full refactor: named constants, `Product`/`FoodProduct`, `OrderItem`, `Customer` + `SilverCustomer`/`GoldCustomer`/`PlatinumCustomer`, `Order` with pure calculation methods, separate `format_receipt()`; also filled in the change table | Accepted | Ran `python Assignment_03.py` → PASS; tried invalid inputs (qty 0, negative price, blank name, empty order) → all rejected |
| 2 | "Write the reflection section of CHANGES.md, using Assignment_03.py for context." | A 5-sentence reflection: the tier class family as the biggest improvement; care needed with `str()` number formatting, rounding only at print time, the `> 100` vs `>= 10` boundaries, and the bulk 3% taken from the original subtotal | Edited (class names changed to match the final refactor) | Checked each point against the legacy `calc()` code |

**Ownership statement.** *By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.*

---

## 4 · Before-you-submit checklist

- [ ] `python Assignment_03.py` prints **PASS**.
- [ ] No tuples / parallel lists left — products, orders, and items are objects.
- [ ] No `if tier == ...` chains — tiers are a class family.
- [ ] Calculation methods **return** values and do not `print`; printing is separate.
- [ ] Constructors validate state; no leftover `global`; magic numbers are named.
- [ ] The change table and reflection above are filled in.
- [ ] The prompt log is complete and the ownership statement is signed.
