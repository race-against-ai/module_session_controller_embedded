import serial
import json
import pynng


class SerialPublisher:
    def __init__(self, serial_port, serial_baud_rate, session_pub_address):
        self.serial_port = serial.Serial(serial_port, serial_baud_rate, timeout=1)
        self.pub_socket = pynng.Pub0()
        self.pub_socket.listen(session_pub_address)

    def run(self):
        while True:
            # Read data from the serial port
            data = self.serial_port.readline().decode('utf-8').strip()

            if data:
                self.process_data(data)

    def process_data(self, data):
        # Parse the received JSON string
        try:
            json_data = json.loads(data)
            print(json_data)

            topic = "session_status: "

            payload = topic + json.dumps(json_data)

            print("Sending data...")
            self.pub_socket.send(payload.encode())
            print("Data sent!")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)


if __name__ == "__main__":
    SESSION_PUB_ADDRESS = "ipc:///tmp/RAAI/session_status.ipc"
    SERIAL_PORT = '/dev/tty.usbmodem2101'
    SERIAL_BAUD_RATE = 9600

    serial_publisher = SerialPublisher(SERIAL_PORT, SERIAL_BAUD_RATE, SESSION_PUB_ADDRESS)
    serial_publisher.run()
