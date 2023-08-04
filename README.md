# KPIs Dashboard

This project is a dashboard that shows the KPIs of a company. It is a web application that uses the [Dash](https://dash.plotly.com/) framework and [Flask](https://flask.palletsprojects.com/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### **Prerequisites**

What things you need to run the app

```
Docker
```

### **Running on a python virtual environment**

**Create a virtual environment**

```
python3 -m venv .
```
**Activate the virtual environment**

```
source bin/activate
```
**Install the dependencies**
```
pip install -r requirements.txt
```
**Run the app**
```
python3 dash-kpis.py
```
**Access the app**
```
http://120.0.0.1:8050/
```


### **Running on docker**

```
docker build -t kpi-dashboard .
docker run -p 8050:8050 kpi-dashboard
```

**Access the app**
```
http://localhost:8050/
```
