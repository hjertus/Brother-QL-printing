# Install

How to install in both Docker and in terminal. Under i state what info you need to change to make it work with other printers then the one I use (QL-1100) with the printing size (103x164 mm).

You need to change the printers VendorID and DeviceID evan if you use the same printer. 

## Requiered

***

```python
# Setting Printer Specifications
backend = 'pyusb'
model = 'QL-1100'
printer = 'usb://0x04F9:0x20A7/000/001'
label_size = '103x164'
# Define the desired fixed width and height
fixed_width = 1200
fixed_height = 1822
```

You will need to change these setting in the python file **printing_shit.py**
***
### Backend
| Backend      | Kind                                 | Linux | Mac OS | Windows |
| ----------- |--------------------------------------|-------|--------|---------|
| `network (1)	`      | TCP                                  | ✔| ✔|✔ |
| `linux_kernel`      | USB                                  | 	✔ (2)|✘ |✘ |
| `pyusb (3)`    | USB |	✔ (3.1) |✔ (3.2) |✔ (3.3) |

Change the **backend** to one of these (network, linux_kernal and pyusb)
***
### Model
QL-500 (✓), QL-550 (✓), QL-560 (✓), QL-570 (✓), QL-580N QL-600 (✓), QL-650TD QL-700 (✓), QL-710W (✓), QL-720NW (✓) QL-800 (✓), QL-810W (✓), QL-820NWB (✓) QL-1050 (✓), QL-1060N (✓), QL-1100 (✓), QL-1100NWB, QL-1115NWB.
Change the **model** to one of the above. 

***
### Printer

| Backend      | Printer                     |
| ----------- |-----------------------------| 
| `network`      | tcp//xx.xxx.xxx.xx          |
| `linux_kernel`| ?                           |
| `pyusb`    | usb://0xXXXX:0xXXXX/000/001 |

You can find this info under usbs or network settings. 

***
### Label Size

| Name  | Printable px                    | Description|
|-------|----------------------------| -|
| `12`  |106         |12mm endless |
| `29`  |306       | 29mm endless|
| `38`  | 413           | 38mm endless|
| `50`  | 554           |50mm endless |
| `54`  | 590           | 54mm endless|
| `62`  |696            |  62mm endless|
| `102` |1164 |102mm endless|
| `103` |1200  | 103mm endless|
| `104` | 1200      |104mm endless|
| ` 17x54 `    |165 x  566| 17mm x 54mm die-cut|
| ` 17x87`    |165 x  956|17mm x 87mm die-cut|
| `23x23 `    |202 x  202 |23mm x 23mm die-cut|
| ` 29x42 `    | 306 x  425 |  29mm x 42mm die-cut|
| ` 29x90`    | 306 x  991 |29mm x 90mm die-cut|
| ` 39x90 `    | 413 x  991 |38mm x 90mm die-cut|
| ` 39x48 `    |  425 x  495 | 39mm x 48mm die-cut|
| ` 52x29 `    | 578 x  271 |52mm x 29mm die-cut|
| ` 54x29`    |  598 x  271 | 54mm x 29mm die-cut|
| ` 62x29 `    | 696 x  271 |62mm x 29mm die-cut|
| ` 62x100`    |696 x 1109 |62mm x 100mm die-cut|
| ` 102x51`    |1164 x  526|102mm x 51mm die-cut|
| ` 102x152 `    | 1164 x 1660  |102mm x 153mm die-cut|
| ` 103x164`    | 1200 x 1822 |103mm x 164mm die-cut|
| `d12         `    |94 x   94 | 12mm round die-cut|
| ` d24`    | 236 x  236 |24mm round die-cut|
| ` d58  `    | 618 x  618    | 58mm round die-cut|


Use the (Name) from the list above of the label you have.

You will need to change the code under too to the (Printable px)


```python
# Define the desired fixed width and height
fixed_width = 1200
fixed_height = 1822
```

***
## Docker
***

Run the code under in the terminal. 

```shell
docker build -t printingbrother .
```

Update the BUS_NUMBER and DEVICE_NUMBER and run the code under in the terminal. 
```shell
docker run --privileged -p "5000:5000" --device=/dev/bus/usb/<BUS_NUMBER>/<DEVICE_NUMBER> printingbrother

```

***

## Terminal
***
Run the code under in the terminal.
```shell
git clone https://github.com/hjertus/Brother-QL-printing.git
```

Run the code under in the terminal.
```shell
pip install -r requirements.txt
```

To start the server run the code under in the terminal. 
```shell
python ./brother_ql_web.py
```

***
