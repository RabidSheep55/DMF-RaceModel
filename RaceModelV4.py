import matplotlib.pyplot as plt
'''
NOTE: Whenever the word speed is used, it denotes angular velocity, in rad/s

Version Details:
    - Attempts to model Losses
        - friction
        - air resistance
    - Displays Current draw graph
    - Attemts to model Voltage different
'''

### Known Constants
trackLength = 25 #in m
airDensity = 1.2 #in kg/m^3
gearBoxRatio = 1/30
stallTorque = 0.05259 #in Nm     Nominal: 0.0662
noLoadSpeed = 628.32 #in rad/s   Nominal: 785.4
wheelRadius = 0.0325 #in m

### Chosen/Estimated Constants
carWeight = 0.9 #in kg
dt = 0.01 #Small timestep in s
chosenRatio = 9
crossSectArea = 0.17*0.15 #Used for air resistance calculations in m^2

### Losses
gearBoxEff = 0.75
transmissionEff = 0.6
dragCoefficient = 0.34 #Based on Lightning McQueen's drag coefficient

### Variables
distTravelled = 0 #in m
t = 0 # time passed in s
i = 0 #Used to keep track of number of iterations
motorTorque = stallTorque #At t=0, the motor is not rotating, therefore delivers max torque
motorSpeed = 0
carVel = 0

### Lists - for graphs
times = [0]
carVels = [0]
carAccs = []
dists = [0]
currDraws = []

#For reference
# print("Theoretical top speed (no loading):", noLoadSpeed * gearBoxRatio * chosenRatio * wheelRadius)

#Iterate until the car has crossed the finish line
while distTravelled <= trackLength and distTravelled >= 0:
    #For debugging
    # print("Currently at time:", round(t, 3), "velocity:", round(motorSpeed, 2), "distTravelled:", round(distTravelled, 2))

    # Calculate the current draw based on torque
    instCurrDraw = 117.67 * motorTorque + 0.45
    currDraws += [instCurrDraw]

    #Simple gear ratio calculations
    gearBoxTorque = (motorTorque / gearBoxRatio) * gearBoxEff
    gearBoxSpeed = motorSpeed * gearBoxRatio

    wheelTorque = (gearBoxTorque / chosenRatio) * transmissionEff
    wheelSpeed = gearBoxSpeed * chosenRatio

    #Calculate instantaneous acceleration of the car using F=ma and lever rule
    #also taking into account air resistance
    airResistance = 0.5 * airDensity * crossSectArea * dragCoefficient * carVel * carVel
    force = (wheelTorque / wheelRadius) - airResistance
    carAcc = force / carWeight
    carAccs += [carAcc]

    ### TIME ADVANCES BY dt
    t += dt
    i += 1

    #For graph later
    times += [t]

    #Acceleration caused the car to speed up during dt
    carVel += dt * carAcc
    carVels += [carVel]

    #carVel has changed, therefore motorSpeed has also changed (through our tranmission and the gearbox)
    wheelSpeed = carVel / wheelRadius
    gearBoxSpeed = wheelSpeed / chosenRatio
    motorSpeed = gearBoxSpeed / gearBoxRatio

    #The motor operates on a specific torque/speed relationship (brief graph)
    motorTorque = ((-stallTorque / noLoadSpeed) * motorSpeed) + stallTorque

    #Car also moved during dt - calculated using average of velocity from prevous time step and current velocity
    distTravelled += ((carVels[i] + carVels[i-1]) / 2) * dt
    dists += [distTravelled]

print("Actual top speed:", carVels[i])
print("Race completed in:", round(times[i], 2), "s")

#Plot the race characteristics
currDraws += [currDraws[i-1]]
carAccs += [carAccs[i-1]]
plt.plot(times, carVels, c='blue', label="Velocity (m/s)")
plt.plot(times, carAccs, c='r', label="Acceleration (m/s/s)")
plt.plot(times, dists, c='black', label="Distance Travelled (m)")
plt.plot(times, currDraws, c="orange", label="Current draw (A)")

#Graph settings
plt.ylim(bottom=0)
plt.xlim(left=0)

plt.legend()
plt.xlabel("Time (s)")

plt.show()
