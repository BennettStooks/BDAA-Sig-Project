# U.S. Coal Market Outlook
### Power-Sector Demand, Inventories, and Investment Opportunities

A Team Business Analytics Project for the BDAA x SIG Invitational at The Ohio State University examining the U.S. Coal Market using EIA Data from 2020 - 2025.

We turned raw coal data into an investment call. Cleaning the data in Python, making sense of it. 
Then used Tableau to visualize consumption, deliveries, stockpiles, and prices. 

## Research Question

How does demand from U.S. power plants shape investment opportunities
and risks in the coal industry?

## Key Findings

| Finding | Evidence |
|---|---|
| Electric power dominates domestic coal use | Accounted for 92.2% of U.S. coal consumption in 2025 |
| Power-sector consumption recovered | Increased 11.3% in 2025 to 415.4 million short tons |
| Deliveries lagged consumption | Power plants received 389.9 million short tons, approximately 25.5 million less than they consumed |
| Inventories declined | Electric power stockpiles fell 14.2% to 109.7 million short tons |

Despite the recovery, electric power coal consumption remained
17.2% below its 2021 peak.

## Investment Outlook

Our project recommendation was a selective overweight in coal suppliers
serving U.S. power plants over a 6–12 month horizon, based on the latest
observations in the provided dataset.

Recovering consumption and declining stockpiles could support additional
orders if power plants maintain demand and rebuild inventories.
The main risk is that demand weakens and those purchases do not materialize.

## Visualizations and Presentation

The Tableau analysis covers:

- **Consumption by sector:** The importance of electric power to domestic coal demand.
- **Consumption versus deliveries:** Whether purchases are keeping pace with coal use.
- **Stockpile trends:** Changes in year-end inventories.
- **Coal prices:** Differences in delivered prices across sectors and years.

Explore the project:

- [Final presentation](reports/Coal%20Presentation.pdf)
- [Exported Tableau charts](images/Tableau%20Graphs%20Images.pdf)
- [Packaged Tableau workbook](tableau/Tableau%20Graphs.twbx)

## Tools and Methods

| Tool | Purpose |
|---|---|
| Tableau | Primary visual analysis and calculated fields |
| Python and pandas | Data cleaning, inspection, and quality checks |
| NumPy and statsmodels | Exploratory OLS regression with state and year controls |

### Data Preparation

The dataset contains 1,750 records and 19 columns.

Our cleaning process:

1. Inspected the dataset and column types.
2. Trimmed whitespace from headers and text.
3. Standardized blank cells as missing values.
4. Clarified location column names.
5. Removed exact duplicate rows.
6. Reviewed units and potential outliers.

The original dataset is preserved. Missing measurements remain missing,
and flagged outliers are retained for investigation.

[View the cleaning script](src/clean_data.py)

## Data Scope and Limitations

- National charts use U.S. total records.
- Volume totals use non-overlapping sectors to avoid double-counting.
- Volumes are measured in short tons and displayed in millions where noted.
- Prices represent delivered dollars per short ton.
- Stocks represent year-end inventories.
- Electric Power and Electric Utility prices are unavailable for 2021.
- Heat-content unit labels require further verification.
- OLS results describe historical relationships and fitted values;
  they do not establish future investment returns.

## Repository Structure

```text
data/       Original data, cleaned data, and regression outputs
images/     Exported visualizations
reports/    Final presentation
src/        Python cleaning and regression scripts
tableau/    Packaged Tableau workbook
```

## Run the Cleaning Script

Clone the repository:

```bash
git clone https://github.com/BennettStooks/BDAA-Sig-Project.git
cd BDAA-Sig-Project
```

Install pandas and run the script:

```bash
python3 -m pip install pandas
python3 src/clean_data.py
```

The script reads the original CSV from `data/` and saves the cleaned
dataset as `data/coal_cleaned.csv`.

To explore the visualizations, open `tableau/Tableau Graphs.twbx` in Tableau.

## Team

Bennett Stooksbury, Jayden Bayuga, and Jeena Huynh.

## Data Source

Provided U.S. Coal Consumption and Quality dataset, 2020–2025,
attributed to the U.S. Energy Information Administration.

[EIA Coal Consumption and Quality](https://www.eia.gov/opendata/browser/coal/consumption-and-quality)
