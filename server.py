import socket
import threading # ļauj izpildīt vairākas koda rindiņas vienlaicīgi

# Masīvs ar uzdevumiem
tasks = []

# Komunikācija ar savienotu client 
def handle_client(client_socket):
    try:
        # Saņem līdz 1024 baitu lielus datus no client
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            # Ja nesaņem, tad ver ciet savienojumu
            if not request:
                break
            
            # No client sūtītā ziņojuma piefiksē komandu un uzdevuma tekstu
            command, *args = request.split()

            # Ar komandu ADD masīvā tasks pievieno uzdevuma tekstu
            if command == 'ADD':
                task = ' '.join(args)
                tasks.append(task)
                response = f'Pievienotais uzdevums: {task}\n'
            
            # Ar komandu DELETE un uzdevuma numuru izdzēša uzdevumu no tasks masīva
            elif command == 'DELETE':
                try:
                    task_id = int(args[0])
                    task = tasks.pop(task_id)
                    response = f'Dzēstais uzdevums: {task}\n'
                except IndexError:
                    response = 'Nepareizs uzdevuma ID (Index Error)\n'
                except ValueError:
                    response = 'Nepareiza vērtība (ValueError)\n'
            
            # Ar komandu LIST izvada masīva tasks saturu
            elif command == 'LIST':
                response = '\n'.join(f'{i}: {task}' for i, task in enumerate(tasks)) + '\n'
            else:
                response = 'Nesaprotama komanda\n'

            #Nosūta atbildi client
            client_socket.send(response.encode('utf-8'))
    
    # Aizver client socket
    finally:
        client_socket.close()

def main():
    # Izveido jaunu TCP/IP socket ar Address Family IPv4 un TCP protokolu (Socket Kind - Stream)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Savienosies ar visām pieejamām IP adresēm uz 10101 porta
    server.bind(('0.0.0.0', 10101))
    # Uzklausa 5 ienākošos savienojumus
    server.listen(5)
    print('Serveris klausās uz 10101 porta')

    while True:
        # Gaida jaunu client savienojumu. Kad client pieslēdzas, atgriež jaunu Socket objektu komunikācijai un  tā adresi
        client_socket, addr = server.accept()
        print(f'Izveidots savienojums ar {addr}')
        
        # Izveido jaunu pavedienu un nodod cleint socket uz handle_client funkciju (kods augstāk)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()