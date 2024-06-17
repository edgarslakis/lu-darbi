import socket

def main():
    # Izveido jaunu TCP/IP socket ar Address Family IPv4 un TCP protokolu (Socket Kind - Stream)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Savienojas ar serveri caur "loopback" adresi uz 10101 portu
    client.connect(('127.0.0.1', 10101))

    while True:
        # Jautā lietotājam ievadīt komandu un uzdevumu
        command = input('Dod komandu (ADD <uzdevumus>, DELETE <uzdevuma_id>, LIST): ')
        client.send(command.encode('utf-8'))
        
        # Saņem līdz 4096 baitu lielus datus no server un izvada uz ekrāna
        response = client.recv(4096).decode('utf-8')
        print(response)

if __name__ == '__main__':
    main()
