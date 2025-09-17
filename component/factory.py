from typing import List
from component.Component import Component
from component.Light import Light
from component.Battery import Battery
from component.Buzzer import Buzzer

K_WIRE         = "Wire"
K_BATTERY      = "Battery"
K_SOLAR_PANEL  = "Solar Panel"
K_LED_LIGHT    = "LED Light"
K_LIGHT_GLOBE  = "Light Globe"
K_SWITCH       = "Switch"
K_SENSOR       = "Sensor"
K_BUZZER       = "Buzzer"


def csv_to_component(kind: str, fields: List[str]) -> Component:
    """
    Convert CSV fields (excluding qty and kind) to a Component object.
    """
    k = kind.strip().lower()

    if k == "wire":
        # [length_mm, price]
        length_mm = float(fields[0])
        price = float(fields[1])
        name = str(int(length_mm)) + "mm Wire"
        return Component(name, price)

    if k == "battery":
        # [size, voltage, price]
        size = fields[0].upper()
        voltage = float(fields[1])
        price = float(fields[2])
        name = size + " Battery"
        return Battery(name, price, voltage)

    if k == "solar panel":
        # [voltage, current_A, price] 
        voltage = float(fields[0])
        current_A = float(fields[1])
        price = float(fields[2])
        return Light("Solar Panel", price, "", voltage, current_A)

    if k == "light globe":
        # [colour, voltage, current_mA, price]
        colour = fields[0]
        voltage = float(fields[1])
        current_mA = float(fields[2])
        price = float(fields[3])
        return Light("Light Globe", price, colour, voltage, current_mA / 1000.0)

    if k == "led light":
        # [colour, voltage, current_mA, price]
        colour = fields[0]
        voltage = float(fields[1])
        current_mA = float(fields[2])
        price = float(fields[3])
        return Light("LED Light", price, colour, voltage, current_mA / 1000.0)

    if k == "switch":
        # [type, voltage, price]
        swtype = fields[0]
        price = float(fields[2])
        name = swtype.capitalize() + " Switch"
        return Component(name, price)

    if k == "sensor":
        # [type, voltage, price]
        stype = fields[0]
        price = float(fields[2])
        name = stype.capitalize() + " Sensor"
        return Component(name, price)

    if k == "buzzer":
        # [freqHz, splDb, voltage, current_mA, price]
        freq = float(fields[0])
        spl  = float(fields[1])
        voltage = float(fields[2])
        current_mA = float(fields[3])
        price = float(fields[4])
        return Buzzer("Buzzer", price, voltage, current_mA / 1000.0, freq, spl)

    # Fallback
    return Component(kind, float(fields[-1]))


def component_to_csv_row(qty: int, comp: Component) -> List[str]:
    """
    Convert a Component object back to a CSV row: [qty, kind, ...fields...]
    """
    nm = comp.name
    price = comp.price
    low = nm.lower()

    # Wire
    if "mm wire" in low:
        try:
            length_mm = float(nm.split("mm")[0])
        except Exception:
            length_mm = 0.0
        return [str(qty), K_WIRE, str(int(length_mm)), format(price, ".2f")]

    # Battery
    if low.endswith(" battery") and hasattr(comp, "_voltage"):
        size = nm.split(" ")[0].upper()
        voltage = comp._voltage
        return [str(qty), K_BATTERY, size, format(voltage, ".1f"), format(price, ".2f")]

    # Light
    if isinstance(comp, Light):
        volt = comp.voltage
        currA = comp.current
        colour = getattr(comp, "colour", "")
        if low.startswith("solar panel"):
            # store A
            return [str(qty), K_SOLAR_PANEL, format(volt, ".1f"), format(currA, ".1f"), format(price, ".2f")]
        if low.startswith("led light"):
            return [str(qty), K_LED_LIGHT, colour.lower(), format(volt, ".1f"), format(currA * 1000.0, ".0f"), format(price, ".2f")]
        if low.startswith("light globe"):
            return [str(qty), K_LIGHT_GLOBE, colour.lower(), format(volt, ".1f"), format(currA * 1000.0, ".0f"), format(price, ".2f")]

    # Switch
    if low.endswith(" switch"):
        return [str(qty), K_SWITCH, "push", "4.5", format(price, ".2f")]

    # Sensor
    if low.endswith(" sensor"):
        return [str(qty), K_SENSOR, nm.split(" ")[0].lower(), "5.0", format(price, ".2f")]

    if isinstance(comp, Buzzer):
        return [str(qty), K_BUZZER,
                format(comp.frequency, ".1f"), format(comp.sound_pressure, ".0f"),
                format(comp.voltage, ".1f"), format(comp.current * 1000.0, ".0f"),
                format(price, ".2f")]

    # Fallback
    return [str(qty), nm, format(price, ".2f")]
