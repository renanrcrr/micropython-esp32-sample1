import network
import machine
from microWebSrv import MicroWebSrv

# Set up WiFi connection
wifi_ssid = "your_wifi_ssid"
wifi_password = "your_wifi_password"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(wifi_ssid, wifi_password)
while not sta_if.isconnected():
    pass
print("Connected to WiFi")

# Callback function to handle the root path
def index(httpClient, httpResponse):
    content = """
    <html>
    <head><title>MicroPython ESP32 Web Server</title></head>
    <body>
        <h1>Hello, ESP32!</h1>
        <p>Welcome to the MicroPython ESP32 web server example.</p>
        <form method="POST" action="/submit">
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name">
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    httpResponse.WriteResponseOk(
        headers={"Content-Type": "text/html"},
        contentBytes=content.encode("utf-8")
    )

# Callback function to handle form submission
def submit(httpClient, httpResponse):
    form_data = httpClient.GetPostedURLEncodedForm()
    name = form_data.get("name", "")
    response_content = f"Hello, {name}!"
    content = f"""
    <html>
    <head><title>Submission Result</title></head>
    <body>
        <h1>Submission Result</h1>
        <p>{response_content}</p>
    </body>
    </html>
    """
    httpResponse.WriteResponseOk(
        headers={"Content-Type": "text/html"},
        contentBytes=content.encode("utf-8")
    )

# Set up the web server
web_server = MicroWebSrv(webPath="/")
web_server.SetNotFoundPageUrl("/")

# Route paths to appropriate callback functions
web_server.HandleFunc("/", "GET", index)
web_server.HandleFunc("/submit", "POST", submit)

# Start the web server
web_server.Start(threaded=True)

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    web_server.Stop()
    sta_if.disconnect()
    machine.reset()
