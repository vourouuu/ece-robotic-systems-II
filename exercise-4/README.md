# System: Double Pendulum

![1. Double Pendulum - Front view (motors only)](exercise-4/figures/double-pendulum/motors.jpg)
![2. Double Pendulum arrangement - Top view](exercise-4/figures/double-pendulum/arrangement-1-top-view.jpg)
![3. Double Pendulum - Front view](exercise-4/figures/double-pendulum/arrangement-1-front-side.jpg)
![4. Double Pendulum - Angled view](exercise-4/figures/double-pendulum/arrangement-1-angled-view.jpg)

---

# 1. Create virtual environment
```bash
cd ece-robotic-systems-II/exercise-4/code
```

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

--- 

# 3. Folders' organization
## assignment-report
This folder contains my final report. The assignment corresponds to exercise 3.

---

## exercise-4\candle
This folder contains example code in C++ and Python.  
Click [here](https://github.com/mabrobotics/candle) if you want to explore repository in GitHub.  

---

## exercise-4\code
There are 3 <code>.py</code> or <code>.ipynb</code> files:  

* 1-trajectory-optimization.ipynb
* 2-TVLQR.ipynb
* 3-hardware-implementation.py  

and 4 <code>.csv</code> files:

* results-tl-009.csv: it has optimized state and control input vectors (torque_limit=0.09)
* results-tl-015.csv: it has optimized state and control input vectors (torque_limit=0.15)
* gains-tl-009.csv: it has gain values Ks (torque_limit=0.09)
* gains-tl-015.csv: it has gain values Ks (torque_limit=0.15)

---

## exercise-4\figures\double-pendulum
Here are figures of the real system.

---

## exercise-4\figures\simulation-results
Here are the simulation result figures.

* optimal-trajectory-tl-009: optimal trajectory (torque_limit=0.09)
* optimal-trajectory-tl-015: optimal trajectory (torque_limit=0.15)
* optimal-trajectory-diagrams-tl-009: diagrams of angles and torques (torque_limit=0.09)
* optimal-trajectory-diagrams-tl-015: diagrams of angles and torques (torque_limit=0.15)

---

## exercise-4\motors-tests
This folder contains tests for:

* pyCandle.IMPEDANCE mode
* pyCandle.RAW_TORQUE mode
* pyCandle.VELOCITY_PROFILE mode

## exercise-4\videos
Here are videos of the real system demos:

* demo-tl-009: demo for torque_limit=0.09
* demo-tl-015: demo for torque_limit=0.15