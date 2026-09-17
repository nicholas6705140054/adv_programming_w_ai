"""CampusWheels - classes for Siam University's campus vehicle-rental desk."""


class Vehicle:
    """A vehicle the rental desk can rent out and take back."""

    def __init__(self, make, model, plate):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = False

    @property
    def status(self):
        """Read-only text version of is_rented, used when printing."""
        return "rented" if self.is_rented else "available"

    def rent(self):
        self.is_rented = True

    def return_vehicle(self):
        self.is_rented = False

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate}) [{self.status}]"


class Renter:
    """A member who rents vehicles. Name and licence are always kept valid."""

    def __init__(self, name, license_no):
        # These go through the setters below, so bad values are refused
        # right from the start, not only when changed later.
        self.name = name
        self.license_no = license_no
        self.rented = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Renter name must not be empty.")
        self._name = value.strip()

    @property
    def license_no(self):
        return self._license_no

    @license_no.setter
    def license_no(self, value):
        # bool is a kind of int in Python (True == 1), so rule it out on purpose.
        is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
        if not is_number or value <= 0:
            raise ValueError("Licence number must be a positive number.")
        self._license_no = value

    def rent_vehicle(self, vehicle):
        if vehicle.is_rented:
            raise ValueError(f"{vehicle.make} {vehicle.model} is already rented.")
        vehicle.rent()
        self.rented.append(vehicle)

    def return_vehicle(self, vehicle):
        if vehicle not in self.rented:
            raise ValueError(f"{self.name} is not renting {vehicle.make} {vehicle.model}.")
        vehicle.return_vehicle()
        self.rented.remove(vehicle)

    def __str__(self):
        return f"Renter {self.name} (licence {self.license_no}) - renting {len(self.rented)} vehicle(s)"


class ElectricCar(Vehicle):
    """A Vehicle that also has a battery size."""

    def __init__(self, make, model, plate, battery_kwh):
        super().__init__(make, model, plate)
        self.battery_kwh = battery_kwh

    def __str__(self):
        return (f"Electric car: {self.make} {self.model} ({self.plate}), "
                f"{self.battery_kwh} kWh battery [{self.status}]")


class Motorbike(Vehicle):
    """A Vehicle that also has an engine size."""

    def __init__(self, make, model, plate, engine_cc):
        super().__init__(make, model, plate)
        self.engine_cc = engine_cc

    def __str__(self):
        return (f"Motorbike: {self.make} {self.model} ({self.plate}), "
                f"{self.engine_cc}cc engine [{self.status}]")
