# mac-changer
Utility to change mac address easily on linux using cli


## Setup

```bash
git clone https://github.com/JamesPerisher/mac-changer.git
cd mac-changer
pip install -r requirements.txt
chmod +x changemac.py
```

## Usage

```bash
# Generate a random mac address
./changemac.py generate

# Generate a mac address that can usualy be asigned to non-specialised network cards
./changemac.py generate -s


# To set a specific mac address
./changemac.py set -i (interface) -m (mac address)

# To randomly assign a mac address to a specific interface
./changemac.py set -i (interface) -r
```
