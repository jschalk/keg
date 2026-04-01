# TODO rewrite this readme draft

# ETL Module Overview

This document describes how the ETL (Extract–Transform–Load) module organizes and processes data across multiple dimensions and transformation stages.
The design focuses on **traceability, auditability, and simplicity** — every step can be inspected and verified using only basic SQL or Excel skills.

---

## 1. Overview

Data in this system originates from **Excel sources**.
It goes through a series of **structured stages** that progressively clean, validate, and transform the data into consistent, meaningful tables.

The process starts in **Idea_bricks** tables and ends in **Sound** and **Heard** tables, where the data is finalized and ready for analysis or downstream logic.

---

## 2. Data Migration Summary

```mermaid
flowchart LR
    A[Excel Source] --> B[Idea Raw]
    B --> C[Idea Agg]
    C --> D[Idea Vld]
    D --> E[Sound Raw]
    E --> F[Sound Agg]
    F --> G[Sound Vld]
    G --> H[Heard Raw]
    H --> I[Heard Agg]
    I --> J[Heard Vld]
```

At a high level:

* **Idea_bricks** tables (`Idea Raw`, `Idea Agg`, `Idea Vld`) capture raw and aggregated source data.
* **Sound** tables interpret and translate that data into structured, meaningful forms.
* **Heard** tables finalize transformations involving numeric and time-based data.

---

## 3. Dimensions

All data is organized into **dimensions** — groups of tables that follow a uniform set of rules.
Each dimension has a specific focus but is treated identically in terms of ETL logic and structure.

### Current Dimensions

| Dimension          | Purpose                                                               |
| ------------------ | --------------------------------------------------------------------- |
| **translate**      | Raw translation data used to update translatable content.             |
| **translate_core** | Verified translation subset extracted from `translate`.               |
| **nabu**           | Core content or base entities that receive translated text.           |
| **moment**         | Event-based or temporal data derived from `nabu` content.             |
| **person**         | Higher-level interpretive or logical data derived from `moment` data. |

Each dimension advances through a fixed set of stages (Sound and Heard) with clearly defined insert/update rules.

---

## 4. Stages and Rules

### **General Stage Rules**

* Each **stage** is represented by a single table.
* Each table is populated by **one INSERT query** per ETL run.
* Each table may have **at most one UPDATE query** to transform data after insertion.
* Intermediate data is **never overwritten or hidden** — all transformations are explicit.
* Every stage can be **audited in Excel**, ensuring transparency.

---

## 5. Stage Definitions per Dimension

| Dimension          | Stage Tables                                                                 | Notes                                                       |
| ------------------ | ---------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **translate**      | `Sound Raw`, `Sound Agg`, `Sound Vld`                                        | Base translation data.                                      |
| **translate_core** | `Sound Raw`, `Sound Agg`, `Sound Vld`                                        | Extracted and verified subset of `translate`.               |
| **nabu**           | `Sound Raw`, `Sound Agg`, `Sound Vld`, `Heard Raw`, `Heard Agg`              | Text and translation applied here.                          |
| **moment**         | `Sound Raw`, `Sound Agg`, `Sound Vld`, `Heard Raw`, `Heard Agg`, `Heard Vld` | Includes both translation and numeric/time transformations. |
| **person**         | `Sound Raw`, `Sound Agg`, `Sound Vld`, `Heard Raw`, `Heard Agg`, `Heard Vld` | Logical or interpretive data based on `moment`.             |

---

## 6. Section Roles

### **Idea_bricks Section**

* Receives Excel data directly.
* Tables: `Idea Raw`, `Idea Agg`, `Idea Vld`.
* Focus: Collect, aggregate, and validate input with minimal transformation.

### **Sound Section**

* Converts `Idea_bricks` outputs into structured, interpretable data.
* Applies translation and text-based transformations.
* Uses `translate` and `translate_core` data to update all **nabu**, **moment**, and **person** tables that require translatable content.

### **Heard Section**

* Applies numeric and time-based transformations to the data from the **Sound** section.
* `Heard Vld` tables represent fully clean and verified numeric data.
* This stage ensures that final time values and quantitative metrics are accurate.

---

## 7. Verification and Audit

* Every stage can be exported as a CSV or opened in Excel for inspection.
* Each dimension’s changes can be traced end-to-end through consistent table names.
* Queries are limited to one insert and one update per stage, ensuring reproducible transformations.
* Validation stages (`Vld`) mark the points where data is confirmed to meet final schema and rule expectations.

---

## 8. Summary

| Property                  | Description                                     |
| ------------------------- | ----------------------------------------------- |
| **Source**                | Excel workbooks                                 |
| **Initial Landing Zone**  | Idea_bricks tables                              |
| **Core Processing Zones** | Sound and Heard                                 |
| **Auditable by**          | Any user with Excel/SQL skills                  |
| **ETL Constraints**       | 1 insert + 1 update per table per run           |
| **Primary Dimensions**    | translate, translate_core, nabu, moment, person |

---
