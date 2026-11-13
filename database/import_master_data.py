
import pandas as pd
import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Connect to MySQL database
def get_connection():

    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    return connection


# Import plant data
def import_plants():

    df = pd.read_csv("data/raw/Plant.csv")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Plant
        (plant_id, plant_name, location, capacity)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            plant_name = VALUES(plant_name),
            location = VALUES(location),
            capacity = VALUES(capacity)
    """

    records = [
        tuple(row)
        for row in df[
            ["plant_id", "plant_name", "location", "capacity"]
        ].values
    ]

    cursor.executemany(query, records)

    connection.commit()

    print("Plant data imported successfully!")
    print("Total plants:", cursor.rowcount)

    cursor.close()
    connection.close()

    
def import_production_lines():
    df = pd.read_csv("data/raw/ProductionLine.csv")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO ProductionLine
        (line_id, plant_id, line_name, production_type, status)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            plant_id = VALUES(plant_id),
            line_name = VALUES(line_name),
            production_type = VALUES(production_type),
            status = VALUES(status)
    """

    records = [
        tuple(row)
        for row in df[
            ["line_id", "plant_id", "line_name",
             "production_type", "status"]
        ].values
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("ProductionLine data imported successfully!")
    print("Total production lines:", cursor.rowcount)

    cursor.close()
    connection.close()


def import_machines():
    df = pd.read_csv("data/raw/Machine.csv")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Machine
        (machine_id, line_id, machine_name, machine_type,
         installation_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            line_id = VALUES(line_id),
            machine_name = VALUES(machine_name),
            machine_type = VALUES(machine_type),
            installation_date = VALUES(installation_date),
            status = VALUES(status)
    """

    records = [
        tuple(row)
        for row in df[
            ["machine_id", "line_id", "machine_name",
             "machine_type", "installation_date", "status"]
        ].values
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("Machine data imported successfully!")
    print("Total machines:", cursor.rowcount)

    cursor.close()
    connection.close()


def import_sensors():
    df = pd.read_csv("data/raw/Sensor.csv")

    # Convert sensor types into uppercase
    df["sensor_type"] = df["sensor_type"].str.upper()

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Sensor
        (sensor_id, machine_id, sensor_type, unit,
         min_range, max_range, installed_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            machine_id = VALUES(machine_id),
            sensor_type = VALUES(sensor_type),
            unit = VALUES(unit),
            min_range = VALUES(min_range),
            max_range = VALUES(max_range),
            installed_at = VALUES(installed_at)
    """

    records = [
        tuple(row)
        for row in df[
            ["sensor_id", "machine_id", "sensor_type",
             "unit", "min_range", "max_range", "installed_at"]
        ].values
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("Sensor data imported successfully!")
    print("Total sensors:", cursor.rowcount)

    cursor.close()
    connection.close()


def import_shifts():
    df = pd.read_csv("data/raw/OperatingShift.csv")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO OperatingShift
        (shift_id, plant_id, shift_name, start_time, end_time)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            plant_id = VALUES(plant_id),
            shift_name = VALUES(shift_name),
            start_time = VALUES(start_time),
            end_time = VALUES(end_time)
    """

    records = [
        tuple(row)
        for row in df[
            ["shift_id", "plant_id", "shift_name",
             "start_time", "end_time"]
        ].values
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("OperatingShift data imported successfully!")
    print("Total shifts:", cursor.rowcount)

    cursor.close()
    connection.close()



def import_technicians():
    df = pd.read_csv("data/raw/Technician.csv")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Technician
        (technician_id, technician_name, specialization,
         experience_years)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            technician_name = VALUES(technician_name),
            specialization = VALUES(specialization),
            experience_years = VALUES(experience_years)
    """

    records = [
        tuple(row)
        for row in df[
            ["technician_id", "technician_name",
             "specialization", "experience_years"]
        ].values
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("Technician data imported successfully!")
    print("Total technicians:", cursor.rowcount)

    cursor.close()
    connection.close()


def import_parts():
    df = pd.read_csv("data/raw/Part.csv")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Part
        (part_id, part_name, part_type, stock_quantity, unit_cost)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            part_name = VALUES(part_name),
            part_type = VALUES(part_type),
            stock_quantity = VALUES(stock_quantity),
            unit_cost = VALUES(unit_cost)
    """

    records = [
        tuple(row)
        for row in df[
            ["part_id", "part_name", "part_type",
             "quantity_in_stock", "unit_cost"]
        ].values
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("Part data imported successfully!")
    print("Total parts:", cursor.rowcount)

    cursor.close()
    connection.close()


def import_telemetry():
    df = pd.read_csv("data/raw/SensorReadings.csv")

    # Convert reading IDs into strings
    df["reading_id"] = df["reading_id"].astype(str)

    # Convert timestamps into MySQL-compatible format
    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    ).dt.strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO TelemetryEvent
        (telemetry_id, sensor_id, recorded_at,
         reading_value, operating_state, shift_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            reading_value = VALUES(reading_value),
            operating_state = VALUES(operating_state),
            shift_id = VALUES(shift_id)
    """

    records = [
        (
            row.reading_id,
            row.sensor_id,
            row.timestamp,
            row.reading_value,
            "RUNNING",
            None
        )
        for row in df.itertuples(index=False)
    ]

    cursor.executemany(query, records)
    connection.commit()

    print("Telemetry data imported successfully!")
    print("Total readings:", cursor.rowcount)

    cursor.close()
    connection.close()







if __name__ == "__main__":
    import_plants()
    import_production_lines()
    import_machines()
    import_sensors()
    import_shifts()
    import_technicians()
    import_parts()
    import_telemetry()