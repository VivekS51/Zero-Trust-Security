# Simulated Cruise Ship IT Environment

## Project Overview

This project simulates a modern cruise ship IT infrastructure secured using a Zero Trust Architecture (ZTA). Since access to a real cruise network is unavailable, this environment models realistic operational systems commonly found on passenger vessels.

The objective is to enforce Zero Trust security controls, monitor compliance, and detect suspicious activities across multiple trust zones.

---

# Network Zones

## 1. Bridge / Navigation

### Systems

- ECDIS
- Radar
- Autopilot Interfaces
- Navigation Consoles

### Trust Level

Highest Restriction

---

## 2. Engine / OT

### Systems

- Engine Control
- Fuel Monitoring
- HVAC
- Ship Sensors
- Telemetry Devices

### Trust Level

Highest Restriction

---

## 3. Crew Administration

### Systems

- Officer Laptops
- HR Portal
- Maintenance Systems
- Internal Email

### Trust Level

Medium-High

---

## 4. POS / Payment

### Systems

- Restaurants
- Bars
- Gift Shops
- Spa
- Casino POS Terminals

### Trust Level

PCI Restricted

---

## 5. Guest Wi-Fi

### Systems

- Passenger Phones
- Tablets
- Laptops
- Smart TVs

### Trust Level

Untrusted

---

## 6. Shore-side Cloud

### Systems

- Azure Tenant
- Microsoft Entra ID
- Fleet Reporting
- SIEM
- Azure Storage
- Azure Monitor

### Trust Level

Cloud Zero Trust

---

# User Roles

## Officer

- Full administrative access

---

## Engineer

- Access only to Engine OT

---

## Hospitality Staff

- POS applications only

---

## IT Administrator

- Azure
- Identity
- Security
- Monitoring

---

## Passenger

- Guest Wi-Fi only

---

# Connectivity

The simulated vessel communicates with Azure through a satellite link.

Characteristics

- High latency
- Temporary outages
- Offline policy cache
- Local decision making during cloud outages
- Automatic synchronization after connectivity returns