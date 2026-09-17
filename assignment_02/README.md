# Assignment 2 — CampusWheels Vehicle-Rental Desk

**192-201 · Advanced Computer Programming with Generative AI · Siam University**

A small object-oriented Python program for the campus vehicle-rental desk.

## Files

- `rental.py`: the classes
  - `Vehicle`: make, model, plate, `is_rented`, with `rent()`, `return_vehicle()` and `__str__()`
  - `Renter`: `name` and `license_no` are checked by `@property` setters (a `ValueError` for an empty name or a licence number that is not positive), plus a `rented` list
  - `ElectricCar(Vehicle)`: adds `battery_kwh` and prints its own way
  - `Motorbike(Vehicle)`: adds `engine_cc` and prints its own way
- `main.py`: a demo that shows everything working

## How to run

You need Python 3. From inside this folder, run:

```bash
python main.py
```

(On macOS/Linux you may need `python3 main.py`.)
