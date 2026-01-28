# Robotic Systems II

---

## 1st exercise

---

## 2nd exercise

---

## 3rd exercise

---

## 4th exercise (Linux OS instructions)
### [Installing MDtool](https://github.com/mabrobotics/mdtool/tree/main)  
1. Download [mdtool-amd64-1.5.4-Linux.deb](https://github.com/mabrobotics/mdtool/releases) 

Open a terminal and follow the above steps:

2. ```bash
      cd Downloads/
   ```  
3. ```bash
      sudo adduser <current_username> dialout
   ```  
   * This adds your current user to the dialout group. In Linux, this is required to give your user permission to read and write to serial/USB ports (like the CANdle adapter) without needing sudo for every command.  
4. ```bash
      sudo apt install ./mdtool-amd64-1.5.4-Linux.deb
   ```  
   * This installs the MDtool console application.  
5. ```bash
      sudo apt install setserial
   ```  
   * This installs a utility that allows MDtool to configure the serial port for higher communication speeds and lower latency, which is critical for real-time motor control.  

### [CANdle (python) library installation](https://github.com/mabrobotics/candle/tree/main)  
Open a new terminal and follow the above steps:  
1. ```bash
      cd <your_path>
   ```  
2. ```bash
      python3 -m venv .venv
   ```  
   ```bash
      source .venv/bin/activate
   ```  
   * Create and activate a new vitual environment in <your_path>.
3. ```bash
      pip install pybind11
   ```  
4. ```bash
      pip install pyCandleMAB
   ```  

If you want to run examples from examples\_python folder follow these steps (stay at the same folder)
1. ```bash
      git clone https://github.com/mabrobotics/candle.git
   ```  
2. ```bash
      cd candle/examples_python
   ```  
3. ```bash
      examplei.py
   ```  

If you want to find drivers, run:  
1. ```bash
      mdtool ping all
   ```
