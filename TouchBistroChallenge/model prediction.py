#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 17:42:16 2025

@author: jeongwoohong
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import joblib

def grapher(user_input_df):
    if user_input_df.shape[0] != 4:
        raise ValueError("The input data must be 4 weeks worth of data (4 rows).")
    
    TARGET_COL = "sales_revenue_with_tax"
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
    cat_cols = ["concept", "city", "venue_xref_id"]
    window_size = 4
    X_num = user_input_df[num_cols].values.reshape(1, window_size, len(num_cols))
    X_cat = user_input_df[cat_cols].values.reshape(1, window_size, len(cat_cols))
    
    final_model = load_model("/Users/jeongwoohong/Desktop/hackathon 2025/final_model.h5")
    target_scaler = joblib.load("/Users/jeongwoohong/Desktop/hackathon 2025/target_scaler.pkl")
    
    test_sample = {
        "concept_input": X_cat[:, :, 0],
        "city_input": X_cat[:, :, 1],
        "venue_input": X_cat[:, :, 2],
        "num_input": X_num
    }
    
    y_pred_scaled = final_model.predict(test_sample).flatten()[0]
    y_pred_original = target_scaler.inverse_transform(np.array([y_pred_scaled]).reshape(-1, 1)).flatten()[0]
    
    print("Forecasted Week 5 Sales:", y_pred_original)
    
    weeks = np.arange(1, 6)
    actual_revenues = user_input_df[TARGET_COL].values.tolist()
    predicted_revenue = y_pred_original
    revenues = actual_revenues + [predicted_revenue]
    
    week4_revenue = revenues[3]
    week5_revenue = revenues[4]
    segment_color = 'blue' if week5_revenue >= week4_revenue else 'red'
    
    plt.figure(figsize=(10, 6))
    plt.plot(weeks[:4], revenues[:4], marker='o', linestyle='-', color='black', label='Actual (Weeks 1-4)')
    plt.plot([weeks[3], weeks[4]], [revenues[3], revenues[4]], marker='o', linestyle='--', color=segment_color, label='Predicted (Week 5)')
    
    for i in range(4):
        plt.text(weeks[i], revenues[i], f"{revenues[i]:.1f}", ha='center', va='bottom', fontsize=10, color='black')
    plt.text(weeks[4], revenues[4], f"{revenues[4]:.1f}\n(Predicted)", ha='center', va='bottom', fontsize=10, color=segment_color,
             bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))
    
    for i in range(1, len(revenues)):
        pct_change = (revenues[i] - revenues[i-1]) / revenues[i-1] * 100 if revenues[i-1] != 0 else 0
        x_mid = (weeks[i] + weeks[i-1]) / 2
        y_mid = (revenues[i] + revenues[i-1]) / 2
        pct_color = 'green' if pct_change >= 0 else 'red'
        plt.text(x_mid, y_mid, f"{pct_change:+.1f}%", ha='center', va='center', fontsize=9, color=pct_color,
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    plt.xlabel("Week")
    plt.ylabel("Sales Revenue")
    plt.title("4-Week Actual & 5th Week Predicted Sales Revenue")
    plt.xticks(weeks)
    plt.legend()
    plt.grid(True)
    plt.show()

    return week5_revenue

def grapher_compare(user_input_df, predicted_revenue, actual_week5):
    actual_revenues = user_input_df["sales_revenue_with_tax"].values.tolist()
    
    weeks_4 = np.array([1, 2, 3, 4])
    # 5주차의 실제 값과 예측 값이 겹치지 않도록 x좌표를 분리
    week5_actual_x = 4.7
    week5_pred_x   = 5.3
    
    # 1~4주 실제 + 5주차 실제
    revenues_actual = actual_revenues + [actual_week5]
    # 1~4주 실제 + 5주차 예측 (단, 1~4주는 동일 값이므로 그래프에서는 표시 안 함)
    revenues_pred = actual_revenues + [predicted_revenue]
    
    week4_revenue_actual = revenues_actual[3]
    week4_revenue_pred   = revenues_pred[3]  # 보통 동일 값(4주차)이지만 변수 분리

    # 5주차 선 색상 (실제, 예측)
    segment_color_actual = 'blue' if actual_week5 >= week4_revenue_actual else 'red'
    segment_color_pred   = 'blue' if predicted_revenue >= week4_revenue_pred else 'red'
    
    plt.figure(figsize=(10, 6))
    
    # 주 1~4: 실제 매출 라인
    plt.plot(weeks_4, revenues_actual[:4], marker='o', linestyle='-', color='black', label='Actual (Weeks 1-4)')
    
    # 4주차->5주차(실제)
    plt.plot([4, week5_actual_x],
             [week4_revenue_actual, actual_week5],
             marker='o', linestyle='-', color=segment_color_actual, label='Actual (Week 5)')
    
    # 4주차->5주차(예측)만 표시 (1~4주 예측 라인은 제거)
    plt.plot([4, week5_pred_x],
             [week4_revenue_pred, predicted_revenue],
             marker='o', linestyle='--', color=segment_color_pred, label='Predicted (Week 5)')
    
    # 1~4주 실제 값 라벨
    for i, val in enumerate(revenues_actual[:4]):
        plt.text(weeks_4[i], val, f"{val:.1f}", ha='center', va='bottom', fontsize=10, color='black')
    
    # 5주차 실제 값 라벨
    plt.text(week5_actual_x, actual_week5, f"{actual_week5:.1f}\n(Actual)",
             ha='center', va='bottom', fontsize=10, color=segment_color_actual,
             bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))
    
    # 5주차 예측 값 라벨
    plt.text(week5_pred_x, predicted_revenue, f"{predicted_revenue:.1f}\n(Predicted)",
             ha='center', va='bottom', fontsize=10, color=segment_color_pred,
             bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='none'))
    
    # 주 1~4 사이 증감율
    for i in range(1, 4):
        if revenues_actual[i-1] != 0:
            pct_change = (revenues_actual[i] - revenues_actual[i-1]) / revenues_actual[i-1] * 100
        else:
            pct_change = 0
        x_mid = (weeks_4[i] + weeks_4[i-1]) / 2
        y_mid = (revenues_actual[i] + revenues_actual[i-1]) / 2
        pct_color = 'green' if pct_change >= 0 else 'red'
        plt.text(x_mid, y_mid, f"{pct_change:+.1f}%", ha='center', va='center', fontsize=9, color=pct_color,
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    # 5주차 실제 대비 4주차 증감율
    if week4_revenue_actual != 0:
        pct_change_actual = (actual_week5 - week4_revenue_actual) / week4_revenue_actual * 100
    else:
        pct_change_actual = 0
    x_mid_actual = (4 + week5_actual_x) / 2
    y_mid_actual = (week4_revenue_actual + actual_week5) / 2
    pct_color_actual = 'green' if pct_change_actual >= 0 else 'red'
    plt.text(x_mid_actual + 0.1, y_mid_actual - 200,  
             f"{pct_change_actual:+.1f}% (Actual)",
             ha='center', va='center', fontsize=9, color=pct_color_actual,
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    # 5주차 예측 대비 4주차 증감율
    if week4_revenue_pred != 0:
        pct_change_pred = (predicted_revenue - week4_revenue_pred) / week4_revenue_pred * 100
    else:
        pct_change_pred = 0
    x_mid_pred = (4 + week5_pred_x) / 2
    y_mid_pred = (week4_revenue_pred + predicted_revenue) / 2
    pct_color_pred_line = 'green' if pct_change_pred >= 0 else 'red'
    plt.text(x_mid_pred - 0.05, y_mid_pred + 100,  
             f"{pct_change_pred:+.1f}% (Predicted)",
             ha='center', va='center', fontsize=9, color=pct_color_pred_line,
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    plt.xlim(0.5, 5.5)
    plt.ylim(min(revenues_actual + revenues_pred) * 0.95, max(revenues_actual + revenues_pred) * 1.05)
    plt.xticks([1, 2, 3, 4, 5], labels=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'])
    plt.xlabel("Week")
    plt.ylabel("Sales Revenue")
    plt.title("4-Week Actual & 5th Week: Actual vs Predicted")
    plt.legend()
    plt.grid(True)
    plt.show()



filepath = ('/Users/jeongwoohong/Desktop/hackathon 2025/dataset/')

input_1 = pd.read_csv(filepath+ 'input_1.csv')
predicted_revenue_1 = grapher(input_1)
grapher_compare(input_1,predicted_revenue_1,2458.6)

input_2 = pd.read_csv(filepath+ 'input_2.csv')
predicted_revenue_2 = grapher(input_2)

grapher_compare(input_2,predicted_revenue_2,10734.93)


