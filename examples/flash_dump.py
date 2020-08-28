from PSL import sciencelab

PAGESIZE = 2048


def dump_flash(device, output_file="flash_dump.bin"):
    flash = bytearray()
    for page in range(20):
        flash += device.read_bulk_flash(page, PAGESIZE)
    with open(output_file, "wb") as of:
        of.write(flash)


if __name__ == "__main__":
    pslab = sciencelab.connect()
    dump_flash(pslab)
