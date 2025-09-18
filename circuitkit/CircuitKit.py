import json
from typing import List, Tuple


class CircuitKit:
    def __init__(self, name: str, price: float, items: List[Tuple[int, str]]) -> None:
        self.__name = name
        self.__price = price
        self.__items = items

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        self.__price = value

    @property
    def items(self) -> List[Tuple[int, str]]:
        return self.__items

    @items.setter
    def items(self, value: List[Tuple[int, str]]) -> None:
        self.__items = value


    def items_to_json(self) -> str:
        data = []
        for pair in self.__items:
            data.append({"qty": int(pair[0]), "row": str(pair[1])})
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def items_from_json(items_json: str) -> List[Tuple[int, str]]:
        if items_json is None or items_json.strip() == "":
            return []
        raw = json.loads(items_json)
        rebuilt: List[Tuple[int, str]] = []
        for obj in raw:
            rebuilt.append((int(obj["qty"]), str(obj["row"])))
        return rebuilt


    def heading_caps(self) -> str:
        return self.__build_heading(True)

    def heading_pretty(self) -> str:
        return self.__build_heading(False)


    def __build_heading(self, caps: bool) -> str:
        base = self.__name
        if caps:
            base = base.upper()
        else:
            base = self.__to_title_with_connectors(self.__name)
        parts = []
        for qty, row in self.__items:
            qty_s = str(qty)
            title = self.__component_row_to_title(row, caps)
            price_s = self.__extract_price_string(row)
            block = qty_s + " x " + title + " $" + price_s
            if caps:
                block = block.upper()
            parts.append(block)

        if len(parts) > 0:
            base = base + " " + " ".join(parts)

        return base

    def __to_title_with_connectors(self, s: str) -> str:
        if s is None or s == "":
            return ""
        lowers = set(["with", "and", "or", "of", "the", "a", "an", "x"])
        tokens = s.split(" ")
        out = []
        for t in tokens:
            if t.lower() in lowers:
                out.append(t.lower())
            else:
                if len(t) > 0:
                    out.append(t[0:1].upper() + t[1:].lower())
                else:
                    out.append(t)
        return " ".join(out)

    def __component_row_to_title(self, row_without_qty: str, caps: bool) -> str:
        try:
            cols = [c.strip() for c in row_without_qty.split(",")]
            ctype = cols[0]
            title = ""

            if ctype == "Wire" and len(cols) >= 3:
                length = cols[1]
                title = length + "mm Wire"

            elif ctype == "Battery" and len(cols) >= 4:
                size = cols[1]
                volt = cols[2]
                title = volt + "V " + size + " Battery"

            elif ctype == "Solar Panel" and len(cols) >= 4:
                volt = cols[1]
                curr = cols[2]
                title = volt + "V " + curr + "mA Solar Panel"

            elif ctype == "Light Globe" and len(cols) >= 5:
                colour = cols[1]
                volt = cols[2]
                curr = cols[3]
                title = volt + "V " + self.__format_float(curr) + "mA " + self.__to_title_with_connectors(colour) + " Light Globe"

            elif ctype == "LED Light" and len(cols) >= 5:
                colour = cols[1]
                volt = cols[2]
                curr = cols[3]
                title = volt + "V " + self.__format_float(curr) + "mA " + self.__to_title_with_connectors(colour) + " LED Light"

            elif ctype == "Switch" and len(cols) >= 3:
                stype = cols[1]
                volt = cols[2]
                title = volt + "V " + self.__to_title_with_connectors(stype) + " Switch"

            elif ctype == "Sensor" and len(cols) >= 3:
                stype = cols[1]
                volt = cols[2]
                title = volt + "V " + self.__to_title_with_connectors(stype) + " Sensor"

            elif ctype == "Buzzer" and len(cols) >= 6:
                freq = cols[1]
                spl = cols[2]
                volt = cols[3]
                curr = cols[4]
                title = volt + "V " + self.__format_float(curr) + "mA " + self.__format_float(freq) + "Hz " + spl + "dB Buzzer"

            else:
                title = ctype

            if caps:
                return title.upper()
            return title

        except Exception:
            if caps:
                return row_without_qty.upper()
            return row_without_qty

    def __extract_price_string(self, row_without_qty: str) -> str:
        cols = [c.strip() for c in row_without_qty.split(",")]
        if len(cols) == 0:
            return "0.00"
        return cols[-1]

    def __format_float(self, s: str) -> str:
        try:
            v = float(s)
            return str(round(v, 1))
        except Exception:
            return s
