"""
Generates random IMEI numbers.

The user specifies the 8-digit TAC and up to 4-digits of the serial number.
The user also specifies the number of random IMEIs to generate.
"""

import sys
import random
import os


# Src: https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/luhn.py
def checksum(number, alphabet='0123456789'):
    """
    Calculate the Luhn checksum over the provided number.

    The checksum is returned as an int.
    Valid numbers should have a checksum of 0.
    """
    n = len(alphabet)
    number = tuple(alphabet.index(i)
                   for i in reversed(str(number)))
    return (sum(number[::2]) +
            sum(sum(divmod(i * 2, n))
                for i in number[1::2])) % n


def calc_check_digit(number, alphabet='0123456789'):
    """Calculate the extra digit."""
    check_digit = checksum(number + alphabet[0])
    return alphabet[-check_digit]

def get_new_filename(base_name="generated_imeis", extension="txt"):
    """Cari nama file berikutnya agar tidak menimpa."""
    index = 1
    while True:
        filename = f"{base_name}_{index}.{extension}"
        if not os.path.exists(filename):
            return filename
        index += 1


def main():
    """Loop utama program IMEI generator."""
    while True:
        # Step 1: Minta input dasar
        start = ''
        while True:
            try:
                start = str(input('Enter the first 8 - 12 digits: ')).strip()
            except KeyboardInterrupt:
                print('')
                sys.exit()

            if start.isdigit() and 8 <= len(start) <= 12:
                break
            print('*** Invalid input. Harus angka dan panjang antara 8 sampai 12 digit\n')

        # Step 2: Jumlah IMEI yang ingin digenerate
        count = 0
        while True:
            try:
                count_input = input('Enter the number of IMEI numbers to generate: ').strip()
            except KeyboardInterrupt:
                print('')
                sys.exit()

            if count_input.isdigit() and int(count_input) > 0:
                count = int(count_input)
                break
            print('*** Invalid input: masukkan angka lebih dari nol\n')

        # Step 3: Generate IMEI dan simpan
        print('\nGenerating IMEIs...\n')
        generated_imeis = []

        for _ in range(count):
            imei = start
            while len(imei) < 14:
                imei += str(random.randint(0, 9))
            imei += calc_check_digit(imei)
            print(imei)
            generated_imeis.append(imei)

        print('')

        # Step 4: Simpan ke file baru
        filename = get_new_filename()
        with open(filename, 'w') as f:
            for imei in generated_imeis:
                f.write(imei + '\n')

        print(f"{len(generated_imeis)} IMEI berhasil disimpan ke '{filename}'\n")

        # Step 5: Tanya user, mau lanjut atau keluar
        again = input("Generate lagi? (y/n): ").strip().lower()
        if again != 'y':
            print("Terima kasih! Program selesai.")
            break

    # Generate and print random IMEI numbers
    print('')
    generated_imeis = []

    for _ in range(count):
        imei = start

        # Randomly compute the remaining serial number digits
        while len(imei) < 14:
            imei += str(random.randint(0, 9))

        # Calculate the check digit with the Luhn algorithm
        imei += calc_check_digit(imei)
        print(imei)
        generated_imeis.append(imei)

    print('')

    # Simpan ke file
    with open('generated_imeis.txt', 'w') as f:
        for imei in generated_imeis:
            f.write(imei + '\n')

    print(f"{len(generated_imeis)} IMEI berhasil disimpan ke 'generated_imeis.txt'")


# Backwards compatibility (raw_input was renamed to input in Python 3.x)
try:
    # Using Python 2.x; calls to input will be treated as calls to raw_input
    input = raw_input
except NameError:
    # Using Python 3.x; no action required
    pass


if __name__ == '__main__':
    main()
