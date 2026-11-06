# Auto Cars GML

A full-stack Django web application built for a real car dealership.

The platform allows the dealership to manage its vehicle inventory, publish available, reserved and sold cars, receive custom vehicle requests, collect customer reviews, and communicate with customers through WhatsApp.

## Live Website

**https://autocarsgml.eu.pythonanywhere.com/**

## Features

- Vehicle inventory management
- Available, reserved and sold vehicle statuses
- Dedicated vehicle detail pages
- Multi-image vehicle galleries
- Full-screen image viewer
- Responsive vehicle carousels
- Fully clickable vehicle cards
- Custom car request form
- WhatsApp integration
- Customer review submission
- Admin approval system for reviews
- Editable historical review dates
- Django administration dashboard
- Interactive dealership map
- Responsive desktop and mobile interface
- Separate available and sold vehicle listings
- Mobile interface

## Tech Stack

**Backend**
- Python
- Django

**Frontend**
- HTML
- CSS
- JavaScript

**Database**
- SQLite

**Other**
- Leaflet
- OpenStreetMap / Esri map layers
- WhatsApp integration
- Git
- GitHub
- PythonAnywhere

## Project Structure

```text
Auto-Cars-GML/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── dealership/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```


### Vehicle Inventory

Vehicles can be managed through Django Admin and assigned one of three states:

- Available
- Reserved
- Sold

The public website automatically organizes vehicles according to their current status.

### Vehicle Details

Each vehicle has a dedicated page containing:

- Vehicle specifications
- Price
- Description
- Image gallery
- Full-screen image browsing
- WhatsApp contact
- Phone contact

### Custom Vehicle Requests

Customers who cannot find the vehicle they want can submit their requirements, including:

- Brand
- Model
- Maximum budget
- Minimum year
- Fuel type
- Transmission
- Maximum mileage
- Additional preferences

The request is stored in the administration system and prepared as a WhatsApp message for direct communication with the dealership.

### Customer Reviews

Customers can submit reviews directly through the website.

Submitted reviews remain hidden until approved through Django Admin.

Reviews support:

- 1–5 star ratings
- Customer name
- Vehicle purchased
- Written review
- Original review date
- Administrative approval

### Administration

The Django administration interface allows dealership staff to manage:

- Vehicles
- Vehicle images
- Vehicle status
- Customer car requests
- Customer reviews
- Review approval
- Historical review dates

## Responsive Design

The website was designed to work across:

- Desktop
- Tablet
- Mobile

Vehicle and review sections use responsive horizontal carousels with touch scrolling and navigation controls.

## Deployment

The production application is hosted using PythonAnywhere.

Source control and deployment updates are managed using Git and GitHub.

## Author

**Dumitru Alexandru Adrian**

Bachelor's student in Robotics & Artificial Intelligence at the University of Klagenfurt.

This project was designed and developed as a real-world web application for an automotive dealership.