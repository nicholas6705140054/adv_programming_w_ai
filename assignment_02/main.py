"""CampusWheels demo - run with:  python main.py"""

from rental import Vehicle, Renter, ElectricCar, Motorbike


def main():
    print("=== 1. Create a few vehicles and a renter ===")
    yaris = Vehicle("Toyota", "Yaris", "1AB234")
    tesla = ElectricCar("Tesla", "Model 3", "2EV555", battery_kwh=60)
    wave = Motorbike("Honda", "Wave", "3MB789", engine_cc=110)
    alice = Renter("Alice", 12345)
    print(yaris)
    print(tesla)
    print(wave)
    print(alice)

    print("\n=== 2. Rent and return a vehicle ===")
    alice.rent_vehicle(yaris)
    print("Alice rents the Yaris:")
    print("  ", yaris)
    print("  ", alice)
    alice.return_vehicle(yaris)
    print("Alice returns the Yaris:")
    print("  ", yaris)
    print("  ", alice)

    print("\n=== 3. Bad renter details are refused (ValueError) ===")
    bad_renters = [("", 12345), ("Bob", 0), ("Carol", -7)]
    for name, licence in bad_renters:
        try:
            Renter(name, licence)
            print(f"Renter({name!r}, {licence}) was accepted - this should not happen!")
        except ValueError as error:
            print(f"Renter({name!r}, {licence}) -> caught ValueError: {error}")

    # The same check also runs when an existing renter's details are changed.
    try:
        alice.license_no = -1
    except ValueError as error:
        print(f"alice.license_no = -1 -> caught ValueError: {error}")
    print("Alice is unchanged:", alice)

    print("\n=== 4. One list, three types, each prints its own way ===")
    wave.rent()  # Motorbike uses rent() inherited from Vehicle
    fleet = [yaris, tesla, wave]
    for vehicle in fleet:
        print(vehicle)


if __name__ == "__main__":
    main()
