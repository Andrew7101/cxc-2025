# cxc-2025

## About the Project

### Inspiration
When our team first looked at the TouchBistro x UW Problem Set, we asked ourselves: “What do restaurant owners need the most?” The answer, unsurprisingly, was **actionable revenue insights**. Whether it’s planning for staff schedules, adjusting operational hours, or anticipating holiday rushes, restaurant owners live and breathe by their sales figures. That realization inspired us to focus our project on three core problem statements:

1. **Forecasting Sales Revenue (Problem #3)**  
2. **Effect of Operational Offsets on Sales (Problem #4)**  
3. **Holiday or Day-of-Week Impact on Sales (Problem #7)**  

### What We Learned
Throughout the process, we gained a deeper understanding of how different factors—like a restaurant’s concept, location, and operating hours—can influence daily or weekly sales. We also discovered that while certain intuitive theories (e.g., *“Opening earlier increases overall sales”*) can guide our hypotheses, they don’t always hold up against real data when you factor in labor costs and overhead.

### How We Built Our Project
1. **Data Exploration & Cleaning**  
   We began by exploring the provided dataset of bill-level transactions and venue details. We cleaned and transformed the data (e.g., handling missing values, converting time zones, categorizing venues by concept) to prepare it for modeling.

2. **Analyzing Operational Offsets (Problem #4)**  
   - **Hypothesis**: Venues that start their business day earlier would have higher daily revenue.  
   - **Method**: We plotted the start times against daily revenue across different concepts (e.g., quick-service vs. fine dining).  
   - **Finding**: While early-open venues did show slightly higher sales, it wasn’t a *significant* difference once we considered factors like labor and overhead costs. The incremental revenue gains often leveled out due to increased expenses.

3. **Holiday or Day-of-Week Impact (Problem #7)**  
   - **Hypothesis**: Holidays or weekends boost sales.  
   - **Method**: We segregated the dataset by **holiday vs. non-holiday** and **day-of-week** to check for sales variations.  
   - **Finding**: Venues that operated on holidays generally saw an uptick in revenue. Additionally, weekends tended to produce higher net sales and tips compared to weekdays.

4. **Forecasting Weekly Sales Revenue (Problem #3)**  
   - **Motivation**: Provide restaurant owners with a *forecast* for upcoming weekly sales so they can make more informed decisions regarding staffing, inventory, and promotions.  
   - **Model**: We built an LSTM model that predicts the **next week’s** revenue using the past 4 weeks of data.  
   - **Features** (selected from both the dataset and derived variables):  
     - **Numerical**:  
       \- `payment_total_tip`  
       \- `payment_count_box`  
       \- `order_duration_seconds_box`  
       \- `prev_week_sales`, `prev_2week_sales`, `prev_3week_sales`  
       \- `moving_avg_4weeks`  
       \- `is_holiday`  
     - **Categorical**:  
       \- `concept`  
       \- `city`  
       \- `venue_xref_id`  
   - **Performance**:  
     - **RMSE** ≈ 5131.13  
     - **R²** ≈ 0.89  

5. **Visualization & Dashboard**  
   Finally, we developed a small dashboard that takes the most recent 4 weeks of a venue’s data as input and visualizes the *predicted revenue trend* for the following week. This provides a quick, intuitive look at future sales expectations.

### Challenges Faced
- **Data Imbalance by Concept**: Some concepts (e.g., fast-food) had significantly more data than others (e.g., niche fine dining). This made it harder to generalize our findings across all venue types.  
- **Complex Interactions**: Operational hours, tip behaviors, and sales trends each have *overlapping* effects. Isolating each factor’s impact required careful data engineering and hypothesis testing.  
- **Time Series Complexity**: Building an LSTM-based forecast requires careful handling of time-lagged features. We had to iterate on various model architectures and hyperparameters to reach stable performance.

### Future Improvements
- **More Robust Data**: Incorporating additional external data (e.g., local events, more detailed weather patterns, inflation rates by region) could further refine the model’s accuracy.  
- **Enhanced Visualizations**: We aim to create more interactive dashboards so restaurant owners can drill down into specific factors (e.g., tip amounts, daily foot traffic) and get even more detailed insights.  
- **Granular Segmentation**: With more data, we could tailor separate forecasting models for each concept type, ensuring *precision* predictions for different dining categories.

---

We believe these findings not only validate the usefulness of advanced analytics in the restaurant space but also highlight the importance of domain-specific considerations—like operating hours and holiday promotions. Our hope is that the insights and tools we’ve built can help restaurant owners using TouchBistro make smarter, data-driven decisions every day.
