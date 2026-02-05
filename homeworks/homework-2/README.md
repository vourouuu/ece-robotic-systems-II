# System: Planar Quadrotor (simulation)

---

# 1. Create virtual environment
```bash
cd ece-robotic-systems-II/homework-2/code
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
This folder contains the homework assignment and my final report.

---

## homework-2\code
There are 3 Jupyter Notebook files containing code.  
In each of them, the simulations are commented out within the code because they take 1-2 minutes to load.  
For convenience, a folder named ***simulations*** has been created with the corresponding .mp4 files.

### 1-modeling.ipynb  
If you want to run the simulation, you should uncomment the lines

```python
print("Wait for simulation...")
simulation(xs, x0, x_ref)
```

at the end of Cell 7.

### 2-LQR.ipynb  
If you want to run the simulation, you should uncomment the lines

```python
print("Wait for simulation...")
simulation(xs, x0, x_ref)
```

at the end of Cell 9. Similarly, you are able to test different ```x_ref```, ```u_ref``` and external forces ```F_ext1```, ```F_ext2``` in the same cell.  
Also, in Cell 11 you can modify ```x_target```, ```max_vel```, ```Fext1```, and ```Fext2``` to see how far the quadrotor can reach relative to the linearization point.

### 3-MPC.ipynb
If you want to run the simulation for **MPC without noise**, you should uncomment the lines

```python
print("Wait for simulation...")
simulation(xs, x0, x_ref)
```

at the end of Cell 12.  

If you want to run the simulation for **MPC with noise**, you should uncomment same lines at the end of Cell 14. Additionally, you need to run the code from Cell 1 up to Cell 11 first, then proceed to Cells 14 and 15 respectively.  

If you want to run the simulation for 2D trajectory tracking, you should uncomment the lines

```python
print("Wait for simulation...")
simulation(xs_track, x0, x0, traj=traj)
```

at the end of Cell 19. Additionally, you need to run the code from Cell 1 up to Cell 7 first, then proceed to Cells 16 through 23 respectively.

---

## homework-2\figures
Here are figures of the simulations corresponding to each part of the homework.  

---

## homework-2\simulations
Here are videos of the simulations corresponding to each part of the homework.  
In each video, the initial and desired state of the pendulum are indicated.