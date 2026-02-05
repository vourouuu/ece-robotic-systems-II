# ECE - Robotic Systems II
This course, taught by Associate Professor Konstantinos Chatzilygeroudis, is part of the 9th semester curriculum at the Department of Electrical and Computer Engineering, University of Patras.
Throughout the semester, we are assigned four practical exercises, which I have included in this Git repository.

---

## 1st exercise
There is a detailed README.md file in the exercise-1 folder.

---

## 2nd exercise
There is a detailed README.md file in the exercise-2 folder.

---

## 3rd exercise
There is a detailed README.md file in the exercise-3 folder.

---

## 4th exercise (Linux OS instructions)
There is a detailed README.md file in the exercise-4 folder. Additionally, an extra library is required for the physical system simulation of the double pendulum.

### [MAB Ecosystem](https://mabrobotics.github.io/MD80-x-CANdle-Documentation/intro.html)
### [Installing MDtool](https://github.com/mabrobotics/mdtool/tree/main)  
1. Download [mdtool-amd64-1.5.4-Linux.deb](https://github.com/mabrobotics/mdtool/releases)

Open a terminal and follow the above steps:

2. ```cd Downloads/```  
3. Add your current user to the dialout group. In Linux, this is required to give your user permission to read and write to serial/USB ports (like the CANdle adapter) without needing sudo for every command:  
```sudo adduser <current_username> dialout```  
4. Install the MDtool console application:  
```sudo apt install ./mdtool-amd64-1.5.4-Linux.deb```  
5. Install a utility that allows MDtool to configure the serial port for higher communication speeds and lower latency, which is critical for real-time motor control:  
```sudo apt install setserial```

### [CANdle (python) library installation](https://github.com/mabrobotics/candle/tree/main)  
Open a new terminal and follow the above steps:  
1. ```cd <your_path>```  
2. Create and activate a new vitual environment in <your_path>:  
   ```python3 -m venv .venv```  
   ```source .venv/bin/activate```  
4. ```pip install pybind11```  
5. ```pip install pyCandleMAB```  

If you want to run examples from examples\_python folder follow these steps (stay at the same folder)
1. ```git clone https://github.com/mabrobotics/candle.git```  
2. ```cd candle/examples_python```  
3. ```examplei.py```  

If you want to find drivers, run:  
1. ```mdtool ping all```
