# cxc-2025
## About the Project

### Inspiration
When we first reviewed the TouchBistro x UW Problem Set, we asked a simple question: **What do restaurant owners care about the most?** We quickly realized it’s all about **actionable insights for increasing revenue.** With this in mind, our team decided to focus on:

1. **Forecasting Sales Revenue (Problem #3)**  
2. **Effect of Operational Offsets on Sales (Problem #4)**  
3. **Holiday or Day-of-Week Impact on Sales (Problem #7)**  

These three issues felt closely tied to a restaurant’s bottom line: understanding when to open, how holidays impact business, and how to predict future sales.

---

### What We Learned

#### Effect of Operational Offsets (Problem #4)
We hypothesized that venues starting earlier in the day would generate higher daily sales. Surprisingly, the data didn’t support this theory:
- **start_of_day_offset** data showed most restaurants opened between **4–6 AM**, which was unexpected since many restaurants typically open around lunchtime.  
- To measure sales, we used **bill_total_billed** because it best reflects customers’ spending.  
- The overall analysis revealed **no significant difference in sales** based on opening hour. While some restaurants did open earlier, they didn’t necessarily bring in more revenue on average.  
- We further broke down the data by venue concept (alcohol, brunch, fine dining, event dining, casual dining, and “no concept”). The findings generally remained consistent.  
- One anomaly emerged in **fine dining**, where median sales fluctuated between \$10 and \$130. Most notably, median sales jumped sharply between **9 AM** and **10 AM**, despite both time frames having over 5,000 samples each. This peculiar spike remains unexplained.

**Key Takeaway**: Simply opening earlier doesn’t guarantee higher sales. Factors like labor costs and overhead can offset any marginal revenue gains.

---

#### Holiday or Day-of-Week Impact (Problem #7)
Next, we analyzed how holidays affect venue sales:
- We integrated an **external dataset** listing holidays for Canada and the United States.  
- Our initial bar chart comparing mean holiday vs. non-holiday sales suggested **little to no difference**.  
- However, we conducted **t-tests** to statistically compare the two groups; these tests revealed significant differences for many venue types. Some categories indeed saw higher holiday sales, while others did not.  
- We performed this analysis both at an **overall level** and then broke it down by venue concept. Nine venue types showed meaningful differences, and five did not.  

**Key Takeaway**: Holidays can boost sales for certain venue types, but the effect is not universal. Venues that cater to holiday dining (e.g., brunch spots or fine dining) may see notable uplifts.

---

#### Forecasting Weekly Sales Revenue (Problem #3)
Given the insights above, we built an **LSTM model** to forecast **weekly** sales, primarily focusing on the `sales_revenue_with_tax_clip` field as our target. We used the previous **four weeks** of data to predict **the subsequent week**. Our features included:

```python
TARGET_COL = "sales_revenue_with_tax_clip"

num_cols = [
    "payment_total_tip",
    "payment_count_box",
    "order_duration_seconds_box",
    "prev_week_sales",
    "prev_2week_sales",
    "prev_3week_sales",
    "moving_avg_4weeks",
    "is_holiday"
]

cat_cols = [
    "concept",
    "city",
    "venue_xref_id"
]
```

- **Model Performance**:  
  - **RMSE** ≈ 5131.13  
  - **R²** ≈ 0.88  

We also developed a simple prototype application where a restaurant can input its past four weeks of data to get **a graph of predicted sales** for the upcoming week.

**Key Takeaway**: An LSTM-based model can provide solid revenue forecasts, helping restaurateurs anticipate staffing needs, optimize operational hours, and manage inventory.

---

### Challenges Faced
1. **Data Distribution**: Certain venue concepts had significantly more transactions than others, making it difficult to generalize across all segments.  
2. **Unexpected Opening Times**: Most restaurants opened earlier than anticipated (4–6 AM), which complicated our original hypothesis about lunch vs. breakfast sales.  
3. **Complex Interactions**: The interplay between operational hours, holiday effects, and day-of-week trends was non-trivial. It required careful data engineering to isolate each factor’s influence.  
4. **Time-Series Modeling**: Building an LSTM required thorough feature selection and tuning to achieve reasonable accuracy.

---

### Future Improvements
- **More Data Sources**: Incorporating additional factors (e.g., local events, detailed weather patterns, inflation rates) could further refine the sales model.  
- **Venue-Specific Modeling**: With enough data, each concept type could be modeled separately to account for unique dining patterns.  
- **Enhanced Visualizations**: We plan to improve the user interface for the forecast dashboard, making it more intuitive for restaurant owners to explore what-if scenarios and custom segments.

---

### Conclusion
By diving into **operational offsets**, **holiday influences**, and **sales forecasting**, we’ve gained valuable insights that restaurant owners can act upon. While some findings (like early opening hours) defied our initial intuition, others (like holiday-driven sales spikes for certain venue concepts) confirmed that context matters greatly in the restaurant industry.

**Our LSTM model** offers a promising avenue for predicting weekly sales, and with further data enrichment and experimentation, the accuracy and reliability of these forecasts can only improve. We hope these insights help TouchBistro users make more informed decisions on staffing, inventory, and strategic planning—ultimately elevating the guest experience and overall profitability.
