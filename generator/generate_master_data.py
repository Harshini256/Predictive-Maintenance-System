
import csv
import random
from pathlib import Path

# Keep generated data consistent every time
random.seed(20261022)

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Create the raw data folder
RAW_DATA = PROJECT_ROOT / "data" / "raw"
RAW_DATA.mkdir(parents=True, exist_ok=True)


def save_csv(filename, records):
    """Save records into a CSV file."""

    if not records:
        return

    file_path = RAW_DATA / filename

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"{filename} created successfully!")


def generate_plants():
    plants = []

    for i in range(1, 4):
        plants.append({
            "plant_id": f"P{i:02d}",
            "plant_name": f"Manufacturing Plant {i}",
            "location": ["Vizag", "Chennai", "Hyderabad"][i - 1],
            "capacity": random.randint(500, 1000)
        })

    return plants


def generate_production_lines(plants):
    lines = []

    for i in range(1, 13):
        plant = plants[(i - 1) % len(plants)]

        lines.append({
            "line_id": f"L{i:02d}",
            "plant_id": plant["plant_id"],
            "line_name": f"Production Line {i}",
            "production_type": random.choice(
                ["Assembly", "Packaging", "Processing"]
            ),
            "status": random.choice(["ACTIVE", "ACTIVE", "INACTIVE"])
        })

    return lines


def generate_machines(lines):
    machines = []

    machine_types = [
        "Motor", "Pump", "Compressor",
        "Conveyor", "Generator"
    ]

    for i in range(1, 101):
        line = lines[(i - 1) % len(lines)]

        installation_year = random.randint(2018, 2025)

        machines.append({
            "machine_id": f"M{i:03d}",
            "line_id": line["line_id"],
            "machine_name": f"Machine {i}",
            "machine_type": random.choice(machine_types),
            "installation_date": f"{installation_year}-01-01",
            "status": random.choice(["RUNNING", "RUNNING", "IDLE"])
        })

    return machines

def generate_sensors(machines):
    sensors = []

    sensor_ranges = {
        "Temperature": (40, 110),
        "Vibration": (0.5, 10),
        "Pressure": (3, 13),
        "Humidity": (30, 100),
        "Current": (5, 35)
    }

    sensor_types = [
        "Temperature", "Vibration",
        "Pressure", "Humidity", "Current"
    ]

    sensor_id = 1

    for machine in machines:
        for sensor_type in sensor_types:

            min_range, max_range = sensor_ranges[sensor_type]

            sensors.append({
                "sensor_id": f"S{sensor_id:04d}",
                "machine_id": machine["machine_id"],
                "sensor_type": sensor_type,
                "unit": {
                    "Temperature": "Celsius",
                    "Vibration": "mm/s",
                    "Pressure": "bar",
                    "Humidity": "%",
                    "Current": "Ampere"
                }[sensor_type],
                "min_range": min_range,
                "max_range": max_range,
                "installed_at": "2026-01-01 00:00:00"
            })

            sensor_id += 1

    return sensors


def generate_shifts():
    shifts = []

    shift_times = [
        ("Morning", "06:00", "14:00"),
        ("Evening", "14:00", "22:00"),
        ("Night", "22:00", "06:00")
    ]

    for plant_id in range(1, 4):
        for name, start, end in shift_times:
            shifts.append({
                "shift_id": f"SH{len(shifts) + 1:02d}",
                "plant_id": f"P{plant_id:02d}",
                "shift_name": name,
                "start_time": start,
                "end_time": end
            })

    return shifts


def generate_technicians():
    technicians = []

    for i in range(1, 21):
        technicians.append({
            "technician_id": f"T{i:03d}",
            "technician_name": f"Technician {i}",
            "specialization": random.choice(
                ["Electrical", "Mechanical", "Automation"]
            ),
            "experience_years": random.randint(1, 15)
        })

    return technicians


def generate_parts():
    parts = []

    part_names = [
        "Bearing", "Motor Belt", "Oil Filter",
        "Cooling Fan", "Gear", "Valve",
        "Pump Seal", "Air Filter", "Fuse",
        "Sensor Cable", "Shaft", "Coupling",
        "Lubricant", "Gasket", "Relay"
    ]

    part_types = {
        "Bearing": "Mechanical",
        "Motor Belt": "Mechanical",
        "Oil Filter": "Filter",
        "Cooling Fan": "Electrical",
        "Gear": "Mechanical",
        "Valve": "Mechanical",
        "Pump Seal": "Mechanical",
        "Air Filter": "Filter",
        "Fuse": "Electrical",
        "Sensor Cable": "Electrical",
        "Shaft": "Mechanical",
        "Coupling": "Mechanical",
        "Lubricant": "Consumable",
        "Gasket": "Mechanical",
        "Relay": "Electrical"
    }

    for i, name in enumerate(part_names, start=1):
        parts.append({
            "part_id": f"PT{i:03d}",
            "part_name": name,
            "part_type": part_types[name],
            "quantity_in_stock": random.randint(10, 100),
            "unit_cost": round(random.uniform(100, 5000), 2)
        })

    return parts

def main():
    print("Generating Predictive Maintenance Master Data...")
    
    plants = generate_plants()
    lines = generate_production_lines(plants)
    machines = generate_machines(lines)
    sensors = generate_sensors(machines)
    shifts = generate_shifts()
    technicians = generate_technicians()
    parts = generate_parts()

    save_csv("Plant.csv", plants)
    save_csv("ProductionLine.csv", lines)
    save_csv("Machine.csv", machines)
    save_csv("Sensor.csv", sensors)
    save_csv("OperatingShift.csv", shifts)
    save_csv("Technician.csv", technicians)
    save_csv("Part.csv", parts)

    print("\nAll master data files generated successfully!")


if __name__ == "__main__":
    main()
