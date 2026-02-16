# TOPSIS Web Application with Custom PyPI Package

An end-to-end decision support system implementing the **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** method using a custom-built Python package and a Flask-based web interface.

This project allows users to upload decision datasets, define weights and impacts, and generate ranked alternatives based on multi-criteria decision-making.

The application is modular, reproducible, and deployment-ready.

---

## Project Overview

This project consists of:

- A **Flask web application** for user interaction
- A **custom-developed PyPI package** for TOPSIS computation
- CSV-based input and output handling
- Deployment-ready backend configuration

The system follows the standard TOPSIS mathematical workflow and produces transparent, reproducible rankings.

---

## Key Features

-  CSV file upload support
-  Custom weights and impact selection (`+` / `-`)
-  Automatic normalization and scoring
-  Ranking of alternatives
-  Downloadable result file
-  Custom PyPI package integration
-  Web deployment ready

---

##  Project Structure
    ├── templates/ # HTML templates for Flask UI
    ├── topsis_daksh_102497020/ # Custom TOPSIS PyPI package
    ├── app.py # Flask application entry point
    ├── requirements.txt # Python dependencies
    ├── setup.py # Package configuration
    └── .gitignore # Ignored files


## Methodology — TOPSIS Workflow

The application implements the standard **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** algorithm using the custom PyPI package `topsis-daksh-102497020`. The workflow follows the mathematical formulation of TOPSIS to ensure accurate and reproducible multi-criteria decision-making.

#### 1. Input Processing
The user uploads a CSV file through the Flask interface where:
- The first column represents alternatives.
- Remaining columns contain numeric criteria values.

The system validates numeric data types, matching weights and impacts, and proper formatting before execution.

#### 2. Weight & Impact Definition
Users provide:
- **Weights** → Importance of each criterion  
- **Impacts** → `+` (benefit) or `-` (cost)
  
Validation ensures the number of weights and impacts equals the number of criteria.

#### 3. Normalization
Vector normalization is applied to remove scale differences:
r_ij = x_ij / √(Σ x_ij²)

This converts criteria into comparable dimensionless values.

####  4. Weighted Normalized Matrix
Each normalized value is multiplied by its weight:
v_ij = w_j × r_ij

This incorporates criterion importance into the model.

#### 5. Ideal Best & Worst Solutions
For each criterion:
- If impact is `+`: Ideal Best = max, Ideal Worst = min  
- If impact is `-`: Ideal Best = min, Ideal Worst = max
  
These serve as benchmark reference points.

#### 6. Distance Calculation
Euclidean distances are computed:

S_i⁺ = √(Σ (v_ij − A_j⁺)²)  
S_i⁻ = √(Σ (v_ij − A_j⁻)²)

Where S_i⁺ is the distance from Ideal Best and S_i⁻ from Ideal Worst.

#### 7. TOPSIS Score
Relative closeness is calculated as:

TOPSIS Score = S_i⁻ / (S_i⁺ + S_i⁻)

Score ranges between 0 and 1. A higher value indicates a better alternative.

#### 8. Ranking
Alternatives are ranked in descending order of TOPSIS scores. Rank 1 represents the most preferred option. The final result is generated as a CSV file and delivered to the user via SendGrid email integration.
The computation logic is fully encapsulated within the PyPI package, while the Flask application handles input validation, execution, and email delivery. This separation ensures modularity, maintainability, and production readiness.

---

## Results and Output Explanation

After successfully executing the TOPSIS algorithm, the system generates an output CSV file containing the computed scores and the final rankings of all alternatives.
The generated result file is delivered **exclusively via email** using SendGrid integration. There is no direct download option from the web interface.

---

### Output File Structure

The generated CSV file contains the following columns:

| Column Name       | Description |
|------------------|-------------|
| Alternative      | Name of the alternative |
| Criteria Columns | Original numeric values provided in input |
| TOPSIS Score     | Relative closeness to the ideal solution |
| Rank             | Final ranking based on TOPSIS score |

---

### Interpretation of Results

- The **TOPSIS Score** ranges between 0 and 1.
- A score closer to **1** indicates that the alternative is closer to the ideal best solution.
- A score closer to **0** indicates that the alternative is closer to the ideal worst solution.
- The alternative with the highest score is assigned **Rank 1**.
- Ranking is performed in descending order of TOPSIS scores.

This ensures objective and mathematically grounded comparison across multiple criteria.

---

### Example Output Format

Example output table:

| Alternative | C1 | C2 | C3 | C4 | TOPSIS Score | Rank |
|------------|----|----|----|----|---------------|------|
| A1         | 250 | 16 | 12 | 5 | 0.72 | 2 |
| A2         | 200 | 20 | 10 | 4 | 0.81 | 1 |
| A3         | 300 | 18 | 15 | 3 | 0.55 | 3 |

In this example:
- Alternative A2 has the highest TOPSIS score.
- Therefore, A2 is ranked as the most preferred option.

---

### Result Delivery Workflow

1. User uploads dataset.
2. User provides weights and impacts.
3. The Flask application invokes the custom PyPI package `topsis-daksh-102497020`.
4. The output CSV file is generated on the server.
5. The result file is sent to the user's email address using SendGrid.

This email-based delivery ensures:

- Clean user experience
- No need for manual file download
- Secure and convenient access to results
- Production-ready workflow

---

###  Final Outcome

The result system demonstrates that the application:

- Produces mathematically correct rankings.
- Maintains transparency in computation.
- Ensures reproducible decision-making.
- Integrates algorithmic rigor with real-world usability.

The combination of a Flask backend, a custom PyPI package, Railway deployment, and SendGrid email integration creates a complete, production-ready decision support system.

### Website Link
The Topsis Live website is available here:  
[Topsis Live Website](https://topsis-daksh-102497020-production.up.railway.app/)

https://topsis-daksh-102497020-production.up.railway.app/
---

##  PyPI Package — `topsis-daksh-102497020`

The core TOPSIS computation engine used in this project is published as a standalone Python package on PyPI.

This allows the algorithm to be reused independently of the web application and integrated into any Python-based workflow.

---

###  Package Information

- **Package Name:** topsis-daksh-102497020  
- **Current Version:** 0.1.0  
- **PyPi Link:** https://pypi.org/project/topsis-daksh-102497020/

The package encapsulates the complete TOPSIS workflow including:

- Input validation  
- Decision matrix normalization  
- Weighted normalization  
- Ideal best and worst determination  
- Euclidean distance computation  
- Score calculation  
- Final ranking  

---

###  Installation

Install the package directly from PyPI using pip:

```
pip install topsis-daksh-102497020
```

After installation, the package can be used either as:

- A Command Line Tool  
- A Python Module  

---

##  Usage as Command Line Tool (CLI)

After installation, the `topsis` command becomes available in the terminal.

### Command Format:

```
topsis input.csv "1,1,1,1" "+,+,-,+" output.csv
```

### Arguments:

- `input.csv` → Input dataset file  
- `"1,1,1,1"` → Comma-separated weights  
- `"+,+,-,+"` → Comma-separated impacts (`+` for benefit, `-` for cost)  
- `output.csv` → Output file name  

### Example:

```
topsis data.csv "2,1,3,1" "+,+,-,+" result.csv
```

This command generates a new CSV file containing TOPSIS scores and rankings.

---

##  Usage as Python Module

The package can also be directly imported and used in Python programs.

### Example:

```python
from topsis import topsis

topsis(
    input_file="input.csv",
    weights=[1, 1, 1, 1],
    impacts=["+", "+", "-", "+"],
    output_file="output.csv"
)
```

### Parameters:

- `input_file` → Path to CSV dataset  
- `weights` → List of numeric weights  
- `impacts` → List of impacts (`+` or `-`)  
- `output_file` → Path to store output CSV  

The function generates an output file containing:

- Original dataset  
- Computed TOPSIS Score  
- Final Rank  

---
