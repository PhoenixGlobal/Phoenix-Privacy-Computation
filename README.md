# Phoenix-Privacy-Computation
Phoenix-Privacy-Computation is based on `Rosetta`,which is a privacy-preserving framework based on TensorFlow.It integrates seamlessly off-chain privacy-preserving computation technologies and on-chain aggregation.

## System requirements

> Currently, Only Ubuntu 18.04 is supported. We will strive to support various systems in the near future after thorough testing.

- Ubuntu (18.04=)
- Python3 (3.6+)
- Pip3 (19.0+)
- Openssl (1.1.1+)
- TensorFlow (1.14.0=, cpu-only)
- CMake (3.10+)

## Installation

- **Python3 & Pip3 & Openssl & CMake**
  Check the version:   

  ```sh
  python3 --version     # e.g. Python 3.6.9
  pip3 --version        # e.g. pip 20.0.2
  apt show libssl-dev   # e.g. Version: 1.1.1-1ubuntu2.1~18.04.5
  cmake --version       # e.g. cmake version 3.15.2
  ```

  If the above software versions are not met, you may install or upgrade them as follows: 
  ```sh
  # install python3, pip3, openssl
  sudo apt update
  sudo apt install python3-dev python3-pip libssl-dev cmake
  # upgrade pip3 to latest 
  sudo pip3 install --upgrade pip
  ```

  ### TensorFlow
  The TensorFlow binary installation uses the binary `.whl` package that TensorFlow officially uploads to pypi.

    ```bash
    # Optional, to depress the warning of tensorflow
    pip3 install numpy==1.16.4 --user
    # install tensorflow
    pip3 install tensorflow==1.14.0 --user
    ````

    After installation, check TensorFlow availability.

    ```bash
    python3 -c 'import tensorflow as tf;print(tf.__version__)'
    ````

  Output: `v1.14.0` indicates successful installation.

  ### Web3.py
    ```bash
    # install web3.py
    pip3 install web3
    ````

  ### Rosetta

  ```bash
  # clone git repository
  git clone https://github.com/PhoenixGlobal/Phoenix-Privacy-Computation.git --recursive
  # compile, install.
  cd Phoenix-Privacy-Computation/Rosetta && ./rosetta.sh compile --enable-protocol-mpc-securenn && ./rosetta.sh install
  ```

  If you encounter some problems for installation,you can also build docker image by using the `Dockerfile`.

## Usage

Firstly,deploy a privacy computation contract ( the source file is in `contract/Privacy.sol` ) on PhoenixChain by using Remix，you can refer to ["How to Deploy Smart Contract on Phoenix using Remix"](https://phoenixglobal.medium.com/phoenix-global-layer-1-mainnet-launch-1290f751376f).

Then,change the contractAddress in `chain.py`.

Create separate directories for three computing nodes `P0`, `P1`, `P2`, e.g. `millionaire0`, `millionaire1`, `millionaire2`. 
```bash
mkdir millionaire0 millionaire1 millionaire2
```

then copy `chain.py`, `log.py`, `millionaire.py`,`log` to  `millionaire0`, `millionaire1`, `millionaire2`, and set three parties address in `chain.py`,then set three parties address to PhoenixChain by calling `setPartyAddresses` of the privacy computation contract.

- Generate server key and certificate

`P0`, `P1`, `P2` nodes need generate their separate ssl server certificate and private key respectively, execute the command below: 

```bash
mkdir certs
# generate private key
openssl genrsa -out certs/server-prikey 4096
# if ~/.rnd not exists, generate it with `openssl rand`
if [ ! -f "${HOME}/.rnd" ]; then openssl rand -writerand ${HOME}/.rnd; fi
# generate sign request
openssl req -new -subj '/C=BY/ST=Belarus/L=Minsk/O=Rosetta SSL IO server/OU=Rosetta server unit/CN=server' -key certs/server-prikey -out certs/cert.req
# sign certificate with cert.req
openssl x509 -req -days 365 -in certs/cert.req -signkey certs/server-prikey -out certs/server-nopass.cert
```

### Configuration

Write a configuration file `CONFIG.json` with the following template: 
```json
{
  "PARTY_ID": 0,
  "MPC": {
    "FLOAT_PRECISION": 16,
    "P0": {
      "NAME": "PartyA(P0)",
      "HOST": "127.0.0.1",
      "PORT": 11121
    },
    "P1": {
      "NAME": "PartyB(P1)",
      "HOST": "127.0.0.1",
      "PORT": 12144
    },
    "P2": {
      "NAME": "PartyC(P2)",
      "HOST": "127.0.0.1",
      "PORT": 13169
    },
    "SAVER_MODE": 7,
    "SERVER_CERT": "certs/server-nopass.cert",
    "SERVER_PRIKEY": "certs/server-prikey",
    "SERVER_PRIKEY_PASSWORD": ""
  }
}
```
Field Description: 
- `PARTY_ID`: role of Secure Multipart Computation, the valid values are 0,1,2, corresponding to `P0`, `P1`, `P2` respectively
- `MPC`: specify the protocol of Secure Multipart Computation
- `FLOAT_PRECISION`: the float-point precision of Secure Multipart Computation
- `P0`, `P1`, `P2`: `Three-Parties-MPC` players `P0`, `P1`, `P2`
- `NAME`: `MPC` player name tag
- `HOST`: host address
- `PORT`: communication port
- `SERVER_CERT`: server-side signature certificate
- `SERVER_PRIKEY`: server private key
- `SERVER_PRIKEY_PASSWORD`: server private key password (empty string if not set)
- `SAVER_MODE`: this indicates how the output checkpoint files are saved. Please refer to `MpcSaveV2` in our [API document](https://github.com/LatticeX-Foundation/Rosetta/blob/master/doc/API_DOC.md) for details.

### Run

#### Stand-alone MODE

Perform stand-alone mode in the Millionaire directory, Firstly, configure the configuration file using the template and save it as CONFIG.json.

Run the `Millionaire Problem` example:

> Note: The console will be prompted for your private inputs at the beginning.

- **`P2`node**

```bash
# MPC player 2
python3 millionaire.py --party_id=2
```

- **`P1`node**

```bash
# MPC player 1
python3 millionaire.py --party_id=1
```

- **`P0` node**

```bash
# MPC player 0
python3 millionaire.py --party_id=0
```

After execution, output should be like this: 
```bash
-------------------------------------------------
ret: [b'1.000000'] # or ret: [b'0.000000']
Transaction successful with hash: 0x81e727f0fe6c2f7aa03ed28f59c69efbeb35e779254e89fff21cfefbbd34e8ac
-------------------------------------------------
```

It means that it has run smoothly and the standalone deployment test has passed, otherwise the test has failed, and please check the above deployment steps.


#### Multi-machine MODE

Multi-machine MODE is similar to stand-alone mode, with the difference that the configuration file needs to be set to a different `HOST` field corresponding to the IP address.


### Query result on PhoenixChain
You can query the result of every round by querying the `getResult` of the privacy computation contract.