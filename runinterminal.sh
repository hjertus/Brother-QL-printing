docker build -t printingbrother .
docker run --privileged -p "5000:5000" --device=/dev/bus/usb/<BUS_NUMBER>/<DEVICE_NUMBER> printingbrother

