
# **Performance Testing with Behave and Visualization**

## **Overview**
This project includes BDD tests for load and stress testing two endpoints:
1. **Client Registration** (`/client_registeration`)
2. **Client Login** (`/client_login`)

It also provides utilities to:
- Summarize test results.
- Visualize response times using matplotlib.

---

## **Setup**

### **1. Install Dependencies**
Ensure Python is installed. Then, install the required libraries:
```bash
pip install behave requests matplotlib pandas
```

---

## **Running Tests**

### **1. Registration Test**
Run the load test for `/client_registeration`:
```bash
behave features/client_registration.feature
```

### **2. Login Test**
Run the stress test for `/client_login`:
```bash
behave features/client_login.feature
```

---

## **Result Files**

### **1. Registration Results**
- **File**: `load_test_results.csv`
- **Details**:
  - Metrics like `responseTime(ms)`, `statusCode`, and `result`.

### **2. Login Results**
- **File**: `login_test_results.csv`
- **Details**:
  - Metrics like `responseTime(ms)`, `statusCode`, and `result`.

### **3. Summary**
Generate a test summary combining registration and login results:
```bash
python generate_test_summary.py
```
- **Output**: `test_summary.csv`

---

## **Visualizing Results**

### **Plot Response Times**
To plot response times, use:
```bash
python plot_response_times.py <file_name>
```

#### Example:
- For registration results:
  ```bash
  python plot_response_times.py load_test_results.csv
  ```
- For login results:
  ```bash
  python plot_response_times.py login_test_results.csv
  ```

---

## **File List**
1. **Features**:
   - `client_registration.feature`
   - `client_login.feature`

2. **Step Definitions**:
   - `client_registration_steps.py`
   - `client_login_steps.py`

3. **Scripts**:
   - `generate_test_summary.py`: Summarizes results into `test_summary.csv`.


Visualizing Results

Plot Response Times

To visualize response times from any result file, use the plot_response_times.py script. Ensure the result file (e.g., load_test_results.csv) is in the same directory as the script or provide the full path.

Steps:

	1.	Open a terminal or command prompt.
	2.	Navigate to the directory containing the plot_response_times.py script.
	3.	Run the script with the file name as an argument.

  - `python plot_response_times.py <file_name>`

  Dependencies

Ensure matplotlib is installed before running the script:
 - `pip install matplotlib`

---
