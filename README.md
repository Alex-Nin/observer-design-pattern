# Stock Observer System

This Python project simulates a stock monitoring system using the Observer design pattern. The program monitors a set of stocks and notifies registered observers of updates. Observers, such as report generators, are alerted whenever new stock data snapshots are available.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Project Overview](#project-overview)
4. [Key Features](#key-features)
5. [Purpose and Lessons Learned](#purpose-and-lessons-learned)

## Installation

To set up and run this project locally:

1. **Clone the Repository**  
```bash
git clone https://github.com/alex-nin/observer-design-pattern.git
cd observer-design-pattern
```

2. **Install Dependencies:** Ensure you have Python 3.x installed.

## Usage

To run the program, execute the following command in your terminal in the program directory:

```bash
python observer.py
```
or
```bash
python3 observer.py
```

## Project Overview

The main components of this system include:
- **Subjects (`LocalStocks`)**: This class manages stock data and maintains a list of observers that need to be notified on updates.
- **Observers**: Each observer subscribes to `LocalStocks` and defines specific actions to take when new stock data is available.
- **Stock Data Parsing**: Stock data entries are parsed from an input file and encapsulated within a `StockData` class.

## Key Features

1. **Add and Remove Observers**: Observers can subscribe to or unsubscribe from updates at any time.
2. **Real-time Notifications**: Whenever stock data updates, all active observers receive the new data.
3. **Modular Observer Types**: Observers can be customized to respond to stock data changes in various ways (e.g., generating specific reports).

## Purpose and Lessons Learned

This project helped me understand the practical applications of the Observer design pattern, particularly in scenarios requiring modular notifications across multiple components. Implementing this design pattern showed me how decoupling allows flexibility—by registering and deregistering observers dynamically, I can manage complex dependencies cleanly and efficiently. Working with the Observer pattern in this context highlighted its utility in building scalable systems where changes to one part of the system should automatically trigger updates across other parts.
