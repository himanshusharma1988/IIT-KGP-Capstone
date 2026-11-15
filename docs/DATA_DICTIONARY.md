# Dataset and metric rules

## Public datasets

### Sample Superstore
Expected useful fields include Order Date, Region, State, Segment, Category, Sub-Category, Sales, Profit, Discount, Quantity, Order ID, Customer ID and Product ID. Verify actual names/types at ingestion. Profit is recorded profit in this dataset; do not call it a full accounting P&L.

### UCI Online Retail
Expected fields include InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID and Country. A leading `C` in InvoiceNo identifies cancellations. The source does not provide Profit, COGS or operating expenses. It is valid to calculate documented positive sales value under explicit filters; it is not valid to invent profit.

## Synthetic FinanceOps workbook

Required sheets:

- `Orders`: Order_ID, Order_Date, Product_ID, Region, Qty, Unit_Price, Sales. One row per order item; Sales = Qty × Unit_Price.
- `Product_Costs`: Product_ID, Effective_From, Unit_Cost. Select the most recent applicable effective cost for each product/order date.
- `Expenses`: Expense_ID, Expense_Date, Region, Expense_Type, Amount. Expense_ID is unique.
- `Returns`: Return_ID, Order_ID, Return_Date, Refund_Amount. Aggregate refunds by Order_ID before joining to Orders to avoid row multiplication.
- `Budget`: Quarter, Region, Budget_Profit. Budget is a target, separate from actual.
- `Definitions`: Metric, Formula, Currency, Fiscal_Year_Start, Data_Through.

Operating profit = net sales − cost of goods sold − operating expenses.
Net sales = gross Sales − Refund_Amount.
COGS = sum(Qty × applicable Unit_Cost), net of the explicitly documented return-cost treatment. Person 1 must document any simplification in the workbook README and data dictionary.

## Calculation conventions

- Profit: `sum(Profit)` only if documented in the source.
- Margin: `sum(Profit) / sum(Sales)`; do not average row-level margins. Guard zero denominator.
- Last completed quarter: explicit reporting-close/Data_Through metadata takes precedence; otherwise choose the quarter immediately before the quarter containing max observed transaction date and disclose the assumption.
- Growth: document the denominator convention for zero/negative prior values. The project example uses absolute prior-period magnitude for comparability; it is not a universal financial rule.
- Returns: declare treatment before aggregation and aggregate at the correct key before join.
- Online Retail sales: define filter policy explicitly. Example policy: positive Quantity and positive UnitPrice for positive sales value; cancellations (`InvoiceNo` starts with `C`) excluded where question asks excluding cancellations.
- Currency: do not add incompatible currencies without a valid exchange-rate source; ask for conversion context.
- Joins: establish key uniqueness, expected cardinality, pre/post row counts and relevant totals. Fail rather than produce inflated values.
