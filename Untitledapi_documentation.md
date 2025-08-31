# API Documentation for Sustainable Farming AI System

## Base URL
All endpoints are prefixed with: `/api`

---

## 1. Create Farmer Profile
**POST** `/api/farmers`

Creates a new farmer profile in the system.

### Request Body:
```json
{
  "name": "John Smith",
  "location": "Karnataka",
  "land_size": 5.5,
  "soil_type": "Loam",
  "water_availability": "Medium",
  "preferred_crops": ["Rice", "Wheat"],
  "inputs": "Seeds, Fertilizer"
}
