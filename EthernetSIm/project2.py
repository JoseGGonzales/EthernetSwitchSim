class Switch:
    def __init__(self):
        self.table = {port: set() for port in range(1, 9)}  # MAC address
        self.frames_out = {port: [] for port in range(1, 9)}  # Outgoing frames for each port

    def learn(self, port, source):
        self.table[port].add(source)  # Learn source address for the port

    def forward(self, id, in_port, source, destination):
        self.learn(in_port, source)  # Learn the source address

        if destination == 'X':
            for port in range(1, 9):
                if port != in_port:
                    self.frames_out[port].append(id)  
        else:
            found = False
            for port, addresses in self.table.items():
                if destination in addresses:
                    self.frames_out[port].append(id)  # Send frame to the destination port
                    found = True
            if not found:
                for port in range(1, 9):
                    if port != in_port:
                        self.frames_out[port].append(id) 

    def show_frames(self):
        output = []
        for port in range(1, 9):
            frames = ' '.join(self.frames_out[port])  # Format outgoing frames 
            output.append(f"P{port}: {frames}")
        return output


def main():
    my_switch = Switch()  # new switch

    try:
        with open('in.txt', 'r') as file:
            for line in file:
                line = line.strip()  # Remove extra whitespace
                parts = line.split()  # Split line
                
                if len(parts) == 3:
                    frame_id, port_str, addr = parts
                    port = int(port_str[1:])  #port number

                    source, destination = addr.split('--')  # Split addresses
                    
                    my_switch.forward(frame_id, port, source, destination)  # Forward the frame
                else:
                    print("Invalid line format:", line.strip())  
    except FileNotFoundError:
        print("Error: 'in.txt' file not found.")  
        return

    with open('out.txt', 'w') as file:
        output_frames = my_switch.show_frames()  # Get outgoing frames
        for line in output_frames:
            file.write(line + '\n')  # Write to output file

    print("Output is in the text file named 'out.txt'.")  


if __name__ == "__main__":
    main()
