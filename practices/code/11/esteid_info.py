import sys

# Package 'pyscard'
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.CardType import CardType
from smartcard.util import toHexString

KNOWN_ATRS = {
    # IDEMIA cards, issued until 14.11.2025.
    (0x3B, 0xDB, 0x96, 0x00, 0x80, 0xB1, 0xFE, 0x45, 0x1F, 0x83, 0x00,
     0x12, 0x23, 0x3F, 0x53, 0x65, 0x49, 0x44, 0x0F, 0x90, 0x00, 0xF1): ("idemia", "EstEID 2018 CosmoV8"),
    (0x3B, 0xDC, 0x96, 0x00, 0x80, 0xB1, 0xFE, 0x45, 0x1F, 0x83, 0x00,
     0x12, 0x23, 0x3F, 0x54, 0x65, 0x49, 0x44, 0x32, 0x0F, 0x90, 0x00, 0xC3): ("idemia", "EstEID 2018 CosmoX"),
    # Thales cards, issued starting from 17.11.2025.
    (0x3B, 0xFF, 0x96, 0x00, 0x00, 0x80, 0x31, 0xFE, 0x43, 0x80, 0x31, 0xB8, 0x53,
     0x65, 0x49, 0x44, 0x64, 0xB0, 0x85, 0x05, 0x10, 0x12, 0x23, 0x3F, 0x1D): ("thales", "EstEID 2025 Thales"),
}


class EstEIDCardType(CardType):
    def matches(self, atr, reader=None):
        return tuple(atr) in KNOWN_ATRS


class CC:
    def __init__(self):
        # Wait until an EstEID card is inserted into any reader.
        self.service = CardRequest(timeout=100, cardType=EstEIDCardType()).waitforcard()
        print("Selected reader:", self.service.connection.getReader())

        # Use T=0 for compatibility and simplicity.
        try:
            self.service.connection.connect(CardConnection.T0_protocol)
        except:
            # Fallback to T=1 if the reader does not support T=0.
            self.service.connection.connect(CardConnection.T1_protocol)

        self.vendor = self._detect()

    def _detect(self) -> str:
        atr = tuple(self.service.connection.getATR())
        if atr not in KNOWN_ATRS:
            print("Unknown card:", toHexString(list(atr)))
            sys.exit(1)

        vendor, name = KNOWN_ATRS[atr]
        print("Detected card:", name)
        return vendor

    def send(self, apdu: list[int]):
        data, sw1, sw2 = self.service.connection.transmit(apdu)

        # Success.
        if [sw1, sw2] == [0x90, 0x00]:
            return data
        # Signals that there is more data to read.
        elif sw1 == 0x61:
            return self.send([0x00, 0xC0, 0x00, 0x00, sw2])  # GET RESPONSE of sw2 bytes
        elif sw1 == 0x6C:
            return self.send(apdu[0:4] + [sw2])  # resend APDU with Le = sw2
        elif sw1 == 0x63 and len(data) == 0:
            # PIN tries counter.
            return sw2
        # Probably an error condition.
        else:
            print("Error: %02x %02x, sending APDU: %s" % (sw1, sw2, toHexString(apdu)))
            sys.exit(1)


def read_binary(to_read: int = 0, offset: int = 0) -> list[int]:
    return [0x00, 0xB0] + list(offset.to_bytes(2, "big")) + [to_read]


def read_idemia(cc: CC):
    cmd_select = [0x00, 0xA4, 0x04, 0x00]
    aid = [0xa0, 0x00, 0x00, 0x00, 0x77, 0x01, 0x08, 0x00, 0x07, 0x00, 0x00, 0xFE, 0x00, 0x00, 0x01, 0x00]
    select_aid = cmd_select + [len(aid)] + aid
    cc.send(select_aid)

    cmd_select_mf = [0x00, 0xA4, 0x00, 0x0C]
    cc.send(cmd_select_mf)

    cmd_select_dat = [0x00, 0xA4, 0x02, 0x0C]

    print()

    cc.send(cmd_select_dat + [0x02, 0xD0, 0x03])
    r = cc.send(read_binary(9, 2))
    print(f"Document number: {bytes(r).decode()}")

    cmd_select_dir = [0x00, 0xA4, 0x01, 0x0C]
    cc.send(cmd_select_dir + [0x02, 0x50, 0x00])

    # EstEID2018 ID1-Developer-Guide V1.0 pages 80-81
    esteid18_map = {
        1: "Surname",
        2: "First name",
        3: "Sex",
        4: "Citizenship",
        5: "Date and place of birth",
        6: "Personal identification code",
        7: "Document number",
        8: "Expiry date",
        9: "Issuance date and authority",
        10: "Type of residence permit",
        11: "Notes line 1",
        12: "Notes line 2",
        13: "Notes line 3",
        14: "Notes line 4",
        15: "Notes line 5",
    }

    print()
    print("Personal data:")

    # Fetch the personal data file.
    for k, v in esteid18_map.items():
        cc.send(cmd_select_dat + [0x02, 0x50, k])
        r = bytes(cc.send(read_binary())).decode()

        if k == 9 and len(r.split()) < 4:
            v = "Date of issuance"

        print(f"\t{v}:", r)

    print()

    # Fetch PIN try counters.
    print("PIN try counters:")
    cc.send(cmd_select_mf)

    pin1 = cc.send([0x00, 0x20, 0x00, 0x01])
    puk = cc.send([0x00, 0x20, 0x00, 0x02])

    cc.send(cmd_select_dir + [0x02, 0xAD, 0xF2])
    pin2 = cc.send([0x00, 0x20, 0x00, 0x85])

    print("\tPIN1:", pin1 & 0x0F, "left")
    print("\tPIN2:", pin2 & 0x0F, "left")
    print("\tPUK :", puk & 0x0F, "left")


def read_thales(cc: CC):
    aid = list(b"\xA0\x00\x00\x00\x63PKCS-15")
    cc.send([0x00, 0xA4, 0x04, 0x0C, len(aid)] + aid)

    df_name = list(b"Document Data")
    cc.send([0x00, 0xA4, 0x04, 0x0C, len(df_name)] + df_name)

    # Thales EstEID developer guide, section 5.3.11.1.
    esteid25_map = {
        0x5001: "Surname",
        0x5002: "Given name",
        0x5003: "Sex",
        0x5004: "Citizenship",
        0x5005: "Date of birth",
        0x5006: "Personal identification code",
        0x5007: "Document number",
        0x5008: "Expiry date",
        0x5009: "Date of issuance",
        0x5010: "Issuing authority",
        0x5011: "Place of birth",
        0x5012: "Type of permit 1",
        0x5013: "Type of permit 2",
        0x5014: "Type of permit 3",
        0x5015: "Remarks front 1",
        0x5016: "Remarks front 2",
        0x5017: "Remarks front 3",
        0x5018: "Remarks back 1",
        0x5019: "Remarks back 2",
        0x5020: "Mission 1",
        0x5021: "Mission 2",
        0x5022: "Position 1",
        0x5023: "Position 2",
    }

    cmd_select_dat = [0x00, 0xA4, 0x02, 0x0C]

    print()
    print("Personal data:")

    for fid, v in esteid25_map.items():
        cc.send(cmd_select_dat + [0x02] + list(fid.to_bytes(2, "big")))
        r = bytes(cc.send(read_binary()))

        # Empty fields are not useful to us, and contain a single 0x00 byte.
        if r == b"\x00":
            continue

        print(f"\t{v}:", r.decode())

    print()

    print("PIN try counters:")
    cc.send([0x00, 0xA4, 0x04, 0x0C, len(aid)] + aid)

    pin1 = cc.send([0x00, 0x20, 0x00, 0x81])
    pin2 = cc.send([0x00, 0x20, 0x00, 0x82])
    puk = cc.send([0x00, 0x20, 0x00, 0x83])

    print("\tPIN1:", pin1 & 0x0F, "left")
    print("\tPIN2:", pin2 & 0x0F, "left")
    print("\tPUK :", puk & 0x0F, "left")


def main():
    cc = CC()

    if cc.vendor == "idemia":
        read_idemia(cc)
    else:
        read_thales(cc)


if __name__ == "__main__":
    main()
